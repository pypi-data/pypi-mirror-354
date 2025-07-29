import os
import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup, Tag, NavigableString
from openai import AzureOpenAI
from dotenv import load_dotenv
import re
import urllib.parse
import argparse # Import argparse
import json

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = AzureOpenAI(
    azure_endpoint=os.getenv("ENDPOINT_URL"),  # No default, must be set in env
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2025-01-01-preview",
)

def get_provider_from_url(url):
    """Extract provider name from URL (e.g., 'azurerm' from '.../providers/hashicorp/azurerm/...' or 'azapi' from Azure REST API URLs)"""
    parsed_url = urllib.parse.urlparse(url)
    path_segments = parsed_url.path.split('/')
    
    # Check if this is an Azure REST API URL
    if 'learn.microsoft.com' in parsed_url.netloc and '/rest/api/' in parsed_url.path:
        return 'azapi'
    
    # Handle regular Terraform provider URLs
    try:
        provider_index = path_segments.index('providers')
        if provider_index + 2 < len(path_segments):
            return path_segments[provider_index + 2]  # Skip 'hashicorp' and get provider name
    except ValueError:
        pass
    return None

def get_module_path(url):
    """Get the module path based on URL structure"""
    provider = get_provider_from_url(url)
    if not provider:
        raise ValueError("Could not determine provider from URL")

    parsed_url = urllib.parse.urlparse(url)
    path_segments = parsed_url.path.split('/')
    
    # Handle Azure REST API URLs
    if provider == 'azapi':
        # Extract resource type from URL (e.g., 'containerregistry/registries' from the path)
        resource_type = None
        for i, segment in enumerate(path_segments):
            if segment == 'api' and i + 1 < len(path_segments):
                # Get the next segment which should be the resource type
                resource_type = path_segments[i + 1]
                break
        
        if not resource_type:
            raise ValueError("Could not extract resource type from Azure REST API URL")
            
        # Convert to PascalCase
        pascal_case_name = ''.join(word.capitalize() for word in resource_type.split('/'))
        module_name = f"Azure.{pascal_case_name}"
        return os.path.join('modules', provider, module_name)
    
    # Handle regular Terraform provider URLs
    resource_name_snake_case = None
    for i, segment in enumerate(path_segments):
        if segment == 'resources' and i + 1 < len(path_segments):
            resource_name_snake_case = path_segments[i+1]
            break
    
    if not resource_name_snake_case:
        raise ValueError("Could not extract resource name from URL")

    # Convert to PascalCase and prepend "Azure." for Azure resources
    pascal_case_name = ''.join(word.capitalize() for word in resource_name_snake_case.split('_'))
    if provider == 'azurerm':
        module_name = f"Azure.{pascal_case_name}"
    else:
        module_name = pascal_case_name

    return os.path.join('modules', provider, module_name)

def check_existing_module(module_path):
    """Check if module exists and return its documentation if available"""
    doc_path = os.path.join(module_path, 'argument_reference.md')
    if os.path.exists(doc_path):
        print(f"📖 Found existing module documentation at {doc_path}")
        with open(doc_path, 'r', encoding='utf-8') as f:
            return f.read()
    return None

async def download_documentation(url):
    provider = get_provider_from_url(url)
    if provider == "azapi":
        return await download_azapi_doc(url)
    return await download_terraform_doc(url)

async def download_azapi_doc(url: str) -> str:
    from playwright.async_api import async_playwright

    print(f"\nFetching AzAPI REST documentation from: {url}")
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        await page.wait_for_load_state("load")
        html = await page.content()
        soup = BeautifulSoup(html, "html.parser")

        # Extract msDocs.data.restAPIData JSON
        rest_data_script = await page.evaluate("""
            () => {
                const scripts = Array.from(document.querySelectorAll('script'));
                for (const script of scripts) {
                    const text = script.textContent;
                    if (text.includes('msDocs.data.restAPIData')) {
                        const jsonText = text.split('msDocs.data.restAPIData = ')[1].split(';')[0];
                        return jsonText;
                    }
                }
                return null;
            }
        """)
        await browser.close()

        md_lines = ["## URI Parameters\n"]
        if not rest_data_script:
            raise Exception("Failed to extract msDocs REST data.")

        rest_data = json.loads(rest_data_script)
        for param in rest_data.get("uriParameters", []):
            name = param["name"]
            required = "required" if param.get("isRequired") else "optional"
            typ = param.get("type", "string")
            md_lines.append(f"- **`{name}`** *(type: {typ}, {required})*")

        # Request Body
        md_lines.append("\n## Request Body\n")
        body_section = soup.find("h2", {"id": "request-body"})
        table = body_section.find_next("table") if body_section else None
        if not table:
            md_lines.append("- *(Request body section not found)*")
        else:
            rows = table.find_all("tr")
            for row in rows[1:]:  # Skip header row
                cols = row.find_all("td")
                if len(cols) >= 4:
                    name = cols[0].get_text(strip=True).replace("\n", "").replace("\xa0", " ")
                    required = "required" if "true" in cols[1].get_text(strip=True).lower() else "optional"
                    typ = cols[2].get_text(strip=True)
                    desc = cols[3].get_text(strip=True).replace("\n", " ")
                    md_lines.append(f"- **`{name}`** *(type: {typ}, {required})* – {desc}")

        return "\n".join(md_lines)

async def download_terraform_doc(url):
    """Download and parse regular Terraform documentation."""
    try:
        print(f"\nFetching Terraform documentation from: {url}")
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(url)
            
            await page.wait_for_selector('div.markdown', timeout=10000)
            content = await page.content()
            await browser.close()

            soup = BeautifulSoup(content, 'html.parser')
            main_content = soup.find('div', {'class': 'markdown'})
            if not main_content:
                print("Warning: Could not find main content div with class 'markdown'")
                main_content = soup.find('main')
            if not main_content:
                print("Warning: Could not find main content, using entire body")
                main_content = soup.body
            if not main_content:
                raise Exception("Could not find any content in the HTML")

            # Find the Argument Reference section
            arg_ref_h2 = None
            h2_found_list = [] # Store all H2s in order of appearance
            for h2 in main_content.find_all(['h2']):
                h2_text = h2.get_text(strip=True).lower()
                h2_found_list.append(h2)
                if 'argument' in h2_text and 'reference' in h2_text:
                    arg_ref_h2 = h2
                    break

            if not arg_ref_h2:
                raise Exception("Could not find 'Argument Reference' section header")

            # Find the next major H2 to set the end boundary
            end_section_h2 = None
            try:
                arg_ref_index = h2_found_list.index(arg_ref_h2)
                for h2 in h2_found_list[arg_ref_index + 1:]:
                    # Check both the text and the ID of the H2
                    h2_text = h2.get_text(strip=True).lower()
                    h2_id = h2.get('id', '').lower()
                    if 'timeouts' in h2_text or 'timeouts' in h2_id:
                        end_section_h2 = h2
                        break
            except ValueError:
                pass

            # Collect all elements between arg_ref_h2 and end_section_h2
            md_lines = [f"## {arg_ref_h2.get_text(strip=True)}\n"]
            current_elem = arg_ref_h2.next_sibling
            while current_elem and current_elem != end_section_h2:
                if isinstance(current_elem, Tag):
                    # Skip if this is the Timeouts section
                    if current_elem.name == 'h2' and ('timeouts' in current_elem.get_text(strip=True).lower() or 'timeouts' in current_elem.get('id', '').lower()):
                        break
                    md = html_to_markdown(current_elem)
                    if md.strip():
                        md_lines.append(md)
                        # Add a blank line after block-level elements for better readability
                        if current_elem.name in ['p', 'ul', 'ol', 'div', 'hr', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                            md_lines.append('')
                elif isinstance(current_elem, NavigableString):
                    s = str(current_elem).strip()
                    if s:
                        md_lines.append(s)
                        md_lines.append('') # Add a blank line for standalone text
                
                current_elem = current_elem.next_sibling

            markdown = '\n'.join(md_lines)
            # Remove excessive blank lines (3 or more become 2)
            markdown = re.sub(r'\n{3,}', '\n\n', markdown)
            return markdown
    except Exception as e:
        raise Exception(f"Failed to download Terraform documentation: {str(e)}")

def html_to_markdown(elem):
    # Convert HTML element to Markdown recursively with improved formatting
    if elem.name in ['ul', 'ol']:
        return list_to_md(elem)
    if elem.name == 'li':
        return li_to_md(elem)
    if elem.name in ['h3', 'h4', 'h5', 'h6']:
        level = int(elem.name[1])
        return f"{'#' * level} {elem.get_text(strip=True)}"
    if elem.name == 'pre':
        code = elem.get_text('\n', strip=True)
        return f"\n```hcl\n{code}\n```\n"
    if elem.name == 'code':
        return f"`{elem.get_text(strip=True)}`"
    if elem.name == 'p':
        return p_to_md(elem)
    if elem.name == 'div' and 'alert' in elem.get('class', []):
        # Note or warning block - flatten to a single paragraph
        note_type = 'Note' if 'alert-info' in elem.get('class', []) else 'Warning'
        text = flatten_alert(elem)
        return f"> **{note_type}:** {text}"
    if elem.name == 'hr':
        return '\n---\n'
    if elem.name == 'a':
        # Remove anchor references from links but keep brackets for internal links
        href = elem.get('href', '')
        if href.startswith('#'):
            return f"[{elem.get_text(strip=True)}]"
        return f"[{elem.get_text(strip=True)}]({href})"
    # Generic recursive conversion for other tags
    content_parts = []
    for child in elem.children:
        if isinstance(child, Tag):
            content_parts.append(html_to_markdown(child))
        elif isinstance(child, NavigableString):
            s = str(child).strip()
            if s:
                content_parts.append(s)
    return ' '.join(content_parts).strip()

def flatten_alert(alert_elem):
    # Flatten all text and inline code in the alert into a single paragraph
    parts = []
    for child in alert_elem.descendants:
        if isinstance(child, Tag) and child.name == 'code':
            parts.append(f'`{child.get_text(strip=True)}`')
        elif isinstance(child, Tag) and child.name == 'br':
            parts.append(' ')
        elif isinstance(child, NavigableString):
            s = str(child).replace('\n', ' ').strip()
            if s:
                parts.append(s)
    # Remove extra spaces and join
    text = ' '.join(parts)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def list_to_md(ul_elem):
    items = []
    for li in ul_elem.find_all('li', recursive=False):
        items.append(li_to_md(li))
    return '\n'.join(items)

def li_to_md(li_elem):
    # Try to bold and code the argument name and process children recursively
    text_parts = []
    for child in li_elem.children:
        if isinstance(child, Tag) and child.name == 'a' and child.code:
            arg = child.get_text(strip=True)
            href = child.get('href', '')
            if href and not href.startswith('#'):  # Only keep non-anchor links
                text_parts.append(f'**[`{arg}`]({href})**')
            else:
                text_parts.append(f'**[{arg}]**')  # Keep square brackets but remove anchor
        elif isinstance(child, Tag) and child.name == 'code':
            text_parts.append(f'**`{child.get_text(strip=True)}`**')
        elif isinstance(child, NavigableString):
            s = str(child)
            dash_idx = s.find('-')
            if dash_idx > 0:
                arg_part = s[:dash_idx].strip()
                desc_part = s[dash_idx+1:].strip()
                if arg_part:
                    text_parts.append(f'**[{arg_part}]** – {desc_part}')
                else:
                    text_parts.append(desc_part)
            else:
                text_parts.append(s)
        elif isinstance(child, Tag):
            # Recursively convert nested tags within <li>
            text_parts.append(html_to_markdown(child))

    return f'- {' '.join(text_parts).strip()}'

def p_to_md(p_elem):
    # Convert <p> with possible <code> and <a> children recursively
    out_parts = []
    for child in p_elem.children:
        if isinstance(child, Tag) and child.name == 'code':
            out_parts.append(f'`{child.get_text(strip=True)}`')
        elif isinstance(child, Tag) and child.name == 'a':
            label = child.get_text(strip=True)
            href = child.get('href', '')
            if href and not href.startswith('#'):  # Only keep non-anchor links
                out_parts.append(f'[{label}]({href})')
            else:
                out_parts.append(label)
        elif isinstance(child, Tag):
            # Recursively convert nested tags within <p>
            out_parts.append(html_to_markdown(child))
        else:
            out_parts.append(str(child))
    return ' '.join(out_parts).strip()

def generate_module_with_gpt(doc_text, azapi_mode=False):
    # Use Azure OpenAI to generate a Terraform module from the documentation
    try:
        endpoint = os.getenv("ENDPOINT_URL")
        deployment = "gpt-4.1"
        # Use API key from environment
        subscription_key = os.getenv("AZURE_OPENAI_API_KEY")

        # Initialize Azure OpenAI client
        client = AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=subscription_key,
            api_version="2025-01-01-preview",
        )

        if azapi_mode:
            system_prompt = (
                "Carefully read the documentation below. Generate a Terraform module using the azapi_resource resource type. "
                "You must use the correct type field (e.g., 'Microsoft.ContainerRegistry/registries@2025-04-01'). "
                "All request body parameters must be mapped into the body block, following the REST API structure. "
                "Include all required and optional parameters, including nested and complex types, as described in the documentation. "
                "For variables.tf, create variables for all request body parameters and top-level resource arguments. "
                "For main.tf, use azapi_resource and map all parameters into the body block. "
                "ALWAYS include a terraform block with required_providers inside it in main.tf, with azapi source set to azure/azapi. Do NOT put required_providers at the top level. "
                "DO NOT generate an outputs.tf section or any outputs. "
                "Output each file as a section with a header like:\n"
                "### main.tf\n...code...\n### variables.tf\n...code...\n\n"
                "Each section will be saved to a separate file with the corresponding name. "
                "Do not use any code block markers (such as triple backticks or ```hcl). Only output plain Terraform code, no explanations.\n\n"
                "RECHECK IF YOU ADDED ANY ARGUMENTS, ATTRIBUTES, OR BLOCKS THAT ARE NOT PRESENT IN THE DOCUMENTATION. IF YOU DID, REMOVE THEM. CHECK IF EVERY PARAMETER HAS ITS VARIABLES IN VARIABLES.TF. "
            )
        else:
            system_prompt = (
                "Carefully read the documentation below. For main.tf, add ALL parameters described in the documentation—do NOT add or miss any parameters. If you miss any, add them; if you add something not in the documentation, remove it. "
                "For variables.tf, create ALL variables for the resource, and ensure they MATCH main.tf exactly. "
                "Do not invent, assume, or add any parameters, arguments, or blocks that are not described in the documentation. If you are unsure, leave it out.\n\n"
                "Before outputting each file, double-check that every argument or block you use is present in the documentation. If it is not, do not include it.\n\n"
                "Be comprehensive: include ALL required and optional arguments, attributes, and blocks that are present in the documentation, including those in nested blocks. For each argument or block, generate a corresponding variable if appropriate. Do not omit any argument or block that is described in the documentation.\n\n"
                "Output each file as a section with a header like:\n"
                "### main.tf\n...code...\n### variables.tf\n...code...\n### outputs.tf\n...code...\n\n"
                "Each section will be saved to a separate file with the corresponding name. "
                "Do not use any code block markers (such as triple backticks or ```hcl). Only output plain Terraform code, no explanations.\n\n"
                "RECHECK IF YOU ADDED ANY ARGUMENTS, ATTRIBUTES, OR BLOCKS THAT ARE NOT PRESENT IN THE DOCUMENTATION. IF YOU DID, REMOVE THEM. CHECK IF EVERY PARAMETER HAS ITS VARIABLES IN VARIABLES.TF, AN OUTPUT IF APPROPRIATE. "
                "FOR DYNAMIC BLOCKS DO LIKE THIS for_each = VARHERE != null ? [VARHERE] : [] "
            )

        chat_prompt = [
            {
                "role": "system",
                "content": [
                    {"type": "text", "text": system_prompt}
                ]
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": doc_text}
                ]
            }
        ]

        #print("DEBUG: messages =", chat_prompt)

        # Generate the completion
        completion = client.chat.completions.create(
            model=deployment,
            messages=chat_prompt,
            max_tokens=20000,
            temperature=1,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
            stream=False
        )

        #print(completion.to_json())
        return completion.choices[0].message.content.strip() if completion.choices else None
    except Exception as e:
        print(f"Error generating module with Azure OpenAI: {e}")
        return None

def split_and_save_outputs(gpt_output, module_dir):
    # Split the GPT output into main.tf, variables.tf, and optionally outputs.tf using section headers
    sections = {
        'main.tf': '',
        'variables.tf': '',
        'outputs.tf': ''
    }
    current_section = None
    code_lines = []
    for line in gpt_output.splitlines():
        header_match = re.match(r'^#+\s*(main|variables|outputs)\.tf', line.strip().lower())
        if header_match:
            # Save previous section
            if current_section and code_lines:
                content = '\n'.join(code_lines).strip()
                content = re.sub(r'^```hcl', '', content, flags=re.IGNORECASE).strip()
                content = re.sub(r'^```', '', content, flags=re.IGNORECASE).strip()
                content = re.sub(r'```$', '', content, flags=re.IGNORECASE).strip()
                sections[current_section] = content
            # Start new section
            section_name = header_match.group(1) + '.tf'
            current_section = section_name
            code_lines = []
        elif current_section:
            code_lines.append(line)
    # Save the last section
    if current_section and code_lines:
        content = '\n'.join(code_lines).strip()
        content = re.sub(r'^```hcl', '', content, flags=re.IGNORECASE).strip()
        content = re.sub(r'^```', '', content, flags=re.IGNORECASE).strip()
        content = re.sub(r'```$', '', content, flags=re.IGNORECASE).strip()
        sections[current_section] = content

    # Create module directory if it doesn't exist
    os.makedirs(module_dir, exist_ok=True)
    print(f"\n💾 Saving generated files to {module_dir}/...\n")
    for fname, content in sections.items():
        file_path = os.path.join(module_dir, fname)
        if content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'✅ Saved {file_path} ({len(content)} characters)')
        else:
            print(f'Warning: {file_path} is empty or missing in GPT output')
    print('✅ Done!')

async def compare_files_with_reference(module_path):
    """Compares generated .tf files with argument_reference.md for missing parameters."""
    arg_ref_path = os.path.join(module_path, 'argument_reference.md')
    variables_tf_path = os.path.join(module_path, 'variables.tf')
    main_tf_path = os.path.join(module_path, 'main.tf')
    outputs_tf_path = os.path.join(module_path, 'outputs.tf')

    # Define regex patterns as variables, manually corrected for Python string literal parsing.
    # Each backslash that should be a literal backslash for the regex engine needs to be doubled (\\).
    # Literal double quotes inside the pattern need to be escaped (\").
    PLAIN_ARG_REGEX = "^- ([a-zA-Z0-9_.]+)\\s+-" # To match arguments like '- name - (Required)'
    BRACKETED_ARG_REGEX = "^- \\[\\s*([a-zA-Z0-9_.]+)\\s*\\]" # To match arguments like '- [account_tier] (Required)'
    BLOCK_DOC_REGEX = "A `([^`]+)` block supports the following:"
    VAR_DECL_REGEX = "variable\\s+\"([a-zA-Z0-9_.]+)\""
    PARAM_ASSIGN_REGEX = "^\\s*([a-zA-Z0-9_]+)\\s*="
    BLOCK_DECL_REGEX = "^\\s*([a-zA-Z0-9_]+)\\s*\\{"
    OUTPUT_DECL_REGEX = "output\\s+\"([a-zA-Z0-9_.]+)\""

    if not os.path.exists(arg_ref_path):
        print(f"🚫 Error: {arg_ref_path} not found. Cannot perform comparison.")
        return
    if not os.path.exists(variables_tf_path):
        print(f"🚫 Error: {variables_tf_path} not found. Cannot perform comparison.")
        return

    # 1. Extract arguments from argument_reference.md
    documented_args = set()
    with open(arg_ref_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
        # Match plain arguments like '- name - (Required)'
        plain_arg_matches = re.findall(PLAIN_ARG_REGEX, content, re.MULTILINE)
        for match in plain_arg_matches:
            documented_args.add(match.strip())

        # Match arguments within brackets like '- [account_tier] (Required)'
        bracketed_arg_matches = re.findall(BRACKETED_ARG_REGEX, content, re.MULTILINE)
        for match in bracketed_arg_matches:
            documented_args.add(match.strip())
        
        # Also extract block names from lines like 'A `block_name` block supports the following:'
        block_matches = re.findall(BLOCK_DOC_REGEX, content)
        for match in block_matches:
            documented_args.add(match.strip())

    print(f"Found {len(documented_args)} documented arguments/blocks in {arg_ref_path}.")

    # 2. Extract variables from variables.tf
    defined_variables = set()
    with open(variables_tf_path, 'r', encoding='utf-8') as f:
        content = f.read()
        var_matches = re.findall(VAR_DECL_REGEX, content)
        for match in var_matches:
            defined_variables.add(match.strip())
    
    print(f"Found {len(defined_variables)} variables defined in {variables_tf_path}.")

    # 3. Compare and report
    missing_variables_in_tf = documented_args - defined_variables
    extra_variables_in_tf = defined_variables - documented_args

    if missing_variables_in_tf:
        print("\n🔴 Missing variables in variables.tf that are documented in argument_reference.md:")
        for var in sorted(list(missing_variables_in_tf)):
            print(f"  - {var}")
    else:
        print("\n🟢 All documented arguments have corresponding variables in variables.tf.")

    if extra_variables_in_tf:
        print("\n🟡 Extra variables in variables.tf that are NOT documented in argument_reference.md:")
        for var in sorted(list(extra_variables_in_tf)):
            print(f"  - {var}")
    else:
        print("🟢 No extra variables found in variables.tf that are not documented.")

    # 4. Extract arguments from main.tf and compare
    if os.path.exists(main_tf_path):
        used_main_tf_params = set()
        with open(main_tf_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Regex to find arguments: `  key = value` or `key {` for blocks
            param_matches = re.findall(PARAM_ASSIGN_REGEX, content, re.MULTILINE)
            for match in param_matches:
                used_main_tf_params.add(match.strip())
            
            block_matches = re.findall(BLOCK_DECL_REGEX, content, re.MULTILINE)
            for match in block_matches:
                used_main_tf_params.add(match.strip())
        
        missing_in_main_tf = used_main_tf_params - documented_args
        extra_in_main_tf = documented_args - used_main_tf_params # Documented args not used in main.tf

        if missing_in_main_tf:
            print("\n🔴 Missing parameters/blocks in main.tf that are NOT documented in argument_reference.md:")
            for param in sorted(list(missing_in_main_tf)):
                print(f"  - {param}")
        else:
            print("🟢 All parameters/blocks in main.tf are documented in argument_reference.md.")
        
    else:
        print(f"🚫 Error: {main_tf_path} not found. Cannot compare main.tf.")

    # 5. Extract outputs from outputs.tf and compare
    if os.path.exists(outputs_tf_path):
        defined_outputs = set()
        with open(outputs_tf_path, 'r', encoding='utf-8') as f:
            content = f.read()
            output_matches = re.findall(OUTPUT_DECL_REGEX, content)
            for match in output_matches:
                defined_outputs.add(match.strip())

        # For outputs, we primarily care that they align with attributes or derived values.
        # Since we removed 'Attributes Reference', we'll just check if they are in general documented args
        # or if they are entirely custom (which might be okay for outputs)

        missing_outputs_in_doc = defined_outputs - documented_args

        if missing_outputs_in_doc:
            print("\n🟡 Outputs in outputs.tf that are NOT explicitly documented in argument_reference.md:")
            for output in sorted(list(missing_outputs_in_doc)):
                print(f"  - {output} (might be an attribute or derived output)")
        else:
            print("🟢 All outputs in outputs.tf are either documented or custom.")

    else:
        print(f"🚫 Error: {outputs_tf_path} not found. Cannot compare outputs.tf.")

async def main():
    try:
        # Setup argument parser
        parser = argparse.ArgumentParser(description="Generate Terraform modules from documentation.")
        parser.add_argument('--url', type=str, help='Direct URL to the Terraform resource documentation.')
        parser.add_argument('--generate', action='store_true', help='Generate Terraform files using AI after downloading documentation.')
        args = parser.parse_args()

        if args.url:
            url = args.url
        else:
            url = input("🔗 Enter Terraform resource URL: ").strip()

        if not url:
            raise ValueError("URL cannot be empty")
        
        # Get module path and check for existing documentation
        module_path = get_module_path(url)
        existing_doc = check_existing_module(module_path)
        
        doc_text = None

        if existing_doc:
            use_cached = input("📚 Found existing module documentation. Use cached version? (y/n): ").lower().strip() == 'y'
            if use_cached:
                doc_text = existing_doc
                print("Using cached documentation...")
            else:
                print("Downloading fresh documentation...")
                doc_text = await download_documentation(url)
                # Save the new documentation
                os.makedirs(module_path, exist_ok=True)
                with open(os.path.join(module_path, 'argument_reference.md'), 'w', encoding='utf-8') as f:
                    f.write(doc_text)
        else:
            print("Downloading documentation...")
            doc_text = await download_documentation(url)
            # Save the documentation
            os.makedirs(module_path, exist_ok=True)
            with open(os.path.join(module_path, 'argument_reference.md'), 'w', encoding='utf-8') as f:
                f.write(doc_text)

        print("\n✅ Documentation parsing complete!")
        print(f"📄 Documentation saved to: {os.path.join(module_path, 'argument_reference.md')}")

        if args.generate:
            print("\n⚡ Generating Terraform files with AI...\n")
            azapi_mode = get_provider_from_url(url) == "azapi"
            gpt_output = generate_module_with_gpt(doc_text, azapi_mode=azapi_mode)
            if gpt_output:
                split_and_save_outputs(gpt_output, module_path)
                print("\n🎉 Terraform files generated and saved!")
            else:
                print("❌ AI did not return any output.")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        exit(1)

if __name__ == "__main__":
    asyncio.run(main())