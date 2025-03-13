import os
import shutil
from page_generator import generate_page

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    """Recursively generate HTML pages for all markdown files in the content directory."""
    
    print(f"Starting recursive generation from {dir_path_content} to {dest_dir_path}")
    
    # Use os.walk to traverse directories
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith(".md"):  # Process only markdown files
                # Get full path to the markdown file
                md_path = os.path.join(root, file)
                
                # Get relative path from content directory
                relative_path = os.path.relpath(root, dir_path_content)
                
                # Determine the destination HTML path
                if file == "index.md":
                    if relative_path == ".":
                        # Root index.md becomes public/index.html
                        html_path = os.path.join(dest_dir_path, "index.html")
                    else:
                        # Subdirectory index.md becomes public/subdir/index.html
                        html_path = os.path.join(dest_dir_path, relative_path, "index.html")
                else:
                    # Other .md files become public/subdir/filename.html
                    filename_without_ext = os.path.splitext(file)[0]
                    if relative_path == ".":
                        html_path = os.path.join(dest_dir_path, filename_without_ext + ".html")
                    else:
                        html_path = os.path.join(dest_dir_path, relative_path, filename_without_ext + ".html")
                
                # Ensure the directory exists
                os.makedirs(os.path.dirname(html_path), exist_ok=True)
                
                # Generate the HTML file using the existing generate_page function
                generate_page(md_path, template_path, html_path)
                
                print(f"Generated {html_path} from {md_path}")
                
def main():
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
    
    # Replace the single generate_page call with generate_pages_recursive
    generate_pages_recursive(
        "content",        # dir_path_content - the directory containing markdown files
        "template.html",  # template_path - the template to use
        "public"          # dest_dir_path - where to write the generated HTML files
    )

if __name__ == "__main__":
    main()