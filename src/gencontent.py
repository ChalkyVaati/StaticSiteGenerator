import os
from markdown_blocks import markdown_to_html_node


def generate_page(from_path, template_path, dest_path):
    """
    Generate an HTML page from markdown using a template
    
    Args:
        from_path: Path to the markdown file
        template_path: Path to the HTML template
        dest_path: Path to write the generated HTML
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Read markdown content
    with open(from_path, 'r') as f:
        markdown_content = f.read()
    
    # Read template content
    with open(template_path, 'r') as f:
        template_content = f.read()
    
    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    
    # Extract title
    title = extract_title(markdown_content)
    
    # Replace placeholders in template
    final_html = template_content.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_content)
    
    # Ensure destination directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    # Write to destination file
    with open(dest_path, 'w') as f:
        f.write(final_html)
    
    # At the end of generate_page after writing the file
    print(f"Successfully wrote HTML to {dest_path}")
    print(f"File exists: {os.path.exists(dest_path)}")
    
def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("no title found")


    