from textnode import TextNode, TextType
from htmlnode import extract_markdown_images, extract_markdown_links

def split_nodes_image(old_nodes):
    result = [] #store list of Text nodes
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            print("Old node.text type data")
            print(old_node.text_type)
            print(TextType.TEXT)
            result.append(old_node)
            continue
            
        # Find images in the node's text
        images = extract_markdown_images(old_node.text)
        
        if not images:
            result.append(old_node)
            continue
        
        # Process the text, splitting around each image
        current_text = old_node.text
        
        
        for image_alt, image_url in images:
            print(image_alt)
            print(image_url)
            # Split around the image markdown
            image_markdown = f"![{image_alt}]({image_url})"
            parts = current_text.split(image_markdown, 1)
            
            # Add a node for the text before the image if not empty
            if parts[0]:
                print(f"This is parts 0 {parts[0]}")
                result.append(TextNode(parts[0], TextType.TEXT))
                
            # Add the image node
            result.append(TextNode(image_alt, TextType.IMAGE, image_url))
            
            # Update current_text to the remaining part after the image
            if len(parts) > 1:
                current_text = parts[1]
            else:
                current_text = ""
        if current_text:
            result.append(TextNode(current_text, TextType.TEXT))

    print(result)
    return result

def split_nodes_link(old_nodes):
    result = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:             
            result.append(old_node)
            continue

        links = extract_markdown_links(old_node.text)

        if not links:
            result.append(old_node)
            continue

        # Process the text, splitting around each link
        current_text = old_node.text
        
        for link_text, link_url in links:
            # Split around the link markdown
            link_markdown = f"[{link_text}]({link_url})"
            parts = current_text.split(link_markdown, 1)
            
            # Add a node for the text before the link if not empty
            if parts[0]:
                result.append(TextNode(parts[0], TextType.TEXT))
                
            # Add the link node
            result.append(TextNode(link_text, TextType.LINK, link_url))
            # Update current_text to the remaining part after the image
            if len(parts) > 1:
                current_text = parts[1]
            else:
                current_text = ""
        if current_text:
            result.append(TextNode(current_text, TextType.TEXT))

    print(result)
    return result

node = TextNode(
    "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
    TextType.TEXT,
)

split_nodes_link([node])
split_nodes_image([node])