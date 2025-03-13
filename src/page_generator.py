import os
from markdown_blocks import markdown_to_html_node

def extract_title(markdown):
    """
    Extracts the h1 header from a markdown string.
    
    Args:
        markdown: A string containing markdown text
    
    Returns:
        The text of the h1 header without the # and whitespace
    
    Raises:
        Exception: If no h1 header is found
    """
    # Split the markdown by lines and look for a line starting with #
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            # Strip the # and any leading/trailing whitespace
            return line[2:].strip()
    
    # If we didn't find an h1 header, raise an exception
    raise Exception("No h1 header found in markdown")

def generate_page(from_path, template_path, dest_path):
    print(f"Current working directory: {os.getcwd()}")
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Check if input files exist with absolute paths
    from_path_abs = os.path.abspath(from_path)
    template_path_abs = os.path.abspath(template_path)
    
    print(f"Absolute path to markdown file: {from_path_abs}")
    print(f"Does {from_path_abs} exist? {os.path.exists(from_path_abs)}")
    
    print(f"Absolute path to template file: {template_path_abs}")
    print(f"Does {template_path_abs} exist? {os.path.exists(template_path_abs)}")
    
    # Read the markdown file
    with open(from_path, "r") as f:
        markdown_content = f.read()
    print(f"Markdown content length: {len(markdown_content)}")
    
    # Read the template file
    try:
        with open(template_path, "r") as f:
            template_content = f.read()
        print(f"Template content length: {len(template_content)}")
        print(f"Template content preview: {template_content[:50]}...")
    except Exception as e:
        print(f"Error reading template file: {e}")
        template_content = ""
    # After loading the template, add this debugging
    print("Converting markdown to HTML...")
    html_content = markdown_to_html_node(markdown_content).to_html()
    print(f"HTML content length: {len(html_content)}")
    print(f"HTML content preview: {html_content[:50]}...")

    print("Extracting title...")
    title = extract_title(markdown_content)
    print(f"Extracted title: {title}")

    print("Replacing placeholders in template...")
    final_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
    print(f"Final HTML length: {len(final_html)}")
    print(f"Final HTML preview: {final_html[:50]}...")

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    print(f"Writing to {dest_path}...")
    # Write the final HTML to the destination file
    with open(dest_path, "w") as f:
        f.write(final_html)
    print("File written successfully!")

    # Verify the file was written correctly
    print(f"After writing, does {dest_path} exist? {os.path.exists(dest_path)}")
    file_size = os.path.getsize(dest_path)
    print(f"File size of {dest_path}: {file_size} bytes")