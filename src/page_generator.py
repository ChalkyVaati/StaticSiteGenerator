import os
from markdown_blocks import markdown_to_html_node

def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No H1 title found in markdown")

def generate_page(from_path, template_path, dest_path, basepath):
    """Generate an HTML page from a markdown file, using a template."""
    
    print(f"Generating page from {from_path} to {dest_path} using {template_path} with basepath {basepath}.")
    
    # Read markdown content
    with open(from_path, 'r', encoding="utf-8") as f:
        markdown_content = f.read()

    # Read template content
    with open(template_path, 'r', encoding="utf-8") as f:
        template_content = f.read()

    # Convert Markdown to HTML
    html_content = markdown_to_html_node(markdown_content).to_html()
    
    # Extract title from markdown
    title = extract_title(markdown_content)

    # Replace template placeholders
    full_html = (
        template_content
        .replace("{{ Title }}", title)
        .replace("{{ Content }}", html_content)
        .replace('href="/', f'href="{basepath}')
        .replace('src="/', f'src="{basepath}')
    )

    # Ensure the destination directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Write the generated HTML content to the destination
    with open(dest_path, 'w', encoding="utf-8") as f:
        f.write(full_html)

    print(f"Generated: {dest_path}")
