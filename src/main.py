import os
import shutil
import sys
from page_generator import generate_page

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    """Recursively generate HTML pages for all markdown files in the content directory."""
    
    print(f"Starting recursive generation from {dir_path_content} to {dest_dir_path} with basepath {basepath}")
    
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith(".md"):  # Process only markdown files
                md_path = os.path.join(root, file)  # Full path to markdown file
                relative_path = os.path.relpath(root, dir_path_content)  # Get relative path
                
                # Determine the destination HTML path
                if file == "index.md":
                    if relative_path == ".":
                        html_path = os.path.join(dest_dir_path, "index.html")
                    else:
                        html_path = os.path.join(dest_dir_path, relative_path, "index.html")
                else:
                    filename_without_ext = os.path.splitext(file)[0]
                    if relative_path == ".":
                        html_path = os.path.join(dest_dir_path, filename_without_ext + ".html")
                    else:
                        html_path = os.path.join(dest_dir_path, relative_path, filename_without_ext + ".html")
                
                # Ensure the directory exists
                os.makedirs(os.path.dirname(html_path), exist_ok=True)
                
                # Generate the HTML file with basepath
                generate_page(md_path, template_path, html_path, basepath)
                
                print(f"Generated {html_path} from {md_path}")
                
def main():
    # Grab the first CLI argument as the basepath
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    print(f"Using basepath: {basepath}")

    # Create public directory if it doesn't exist
    os.makedirs("public", exist_ok=True)
    
    # Delete anything in the public directory
    for item in os.listdir("public"):
        item_path = os.path.join("public", item)
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)
        else:
            os.remove(item_path)
    
    # Copy static files to public directory
    if os.path.exists("static"):
        for item in os.listdir("static"):
            source = os.path.join("static", item)
            destination = os.path.join("public", item)
            if os.path.isdir(source):
                shutil.copytree(source, destination)
            else:
                shutil.copy2(source, destination)
    
    # Call generate_pages_recursive with basepath
    generate_pages_recursive(
        "content",
        "template.html",
        "docs",
        basepath
    )

if __name__ == "__main__":
    main()