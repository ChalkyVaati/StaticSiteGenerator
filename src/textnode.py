from enum import Enum
import re
class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type=None, url=None):
        self.text = text
        self.text_type = text_type  # This will be None for simple TextNodes
        self.url = url  # For link nodes
    
    def to_html(self):
        # For a TextNode, just return the text itself
        # If it's a link, wrap it in an <a> tag
        if hasattr(self, 'text_type') and self.text_type == TextType.LINK and hasattr(self, 'url'):
            return f'<a href="{self.url}">{self.text}</a>'
        return self.text
def text_node_to_html_node(text_node):
    # Import here to avoid circular dependency
    from htmlnode import LeafNode
    
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        split_text = old_node.text.split(delimiter)
        if len(split_text) == 1:  # No delimiter found
            new_nodes.append(old_node)
            continue
            
        for i, text in enumerate(split_text):
            if text == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(text, TextType.TEXT))
            else:
                new_nodes.append(TextNode(text, text_type))
    
    return new_nodes  

# Add new functions for links and images
def split_nodes_link(old_nodes):
    """Processes markdown links [text](url) and converts them into LINK TextNodes."""
    new_nodes = []
    
    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')  # Matches [text](url)
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue  # Skip non-text nodes

        current_text = node.text
        match = link_pattern.search(current_text)
        
        while match:
            before = current_text[:match.start()]  # Text before the link
            link_text = match.group(1)  # Extracted link text
            link_url = match.group(2)  # Extracted link URL
            after = current_text[match.end():]  # Text after the link
            
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))  # Create LINK node
            
            current_text = after  # Update current_text to remaining portion
            match = link_pattern.search(current_text)  # Search for next link
        
        if current_text:  # Add remaining text if any
            new_nodes.append(TextNode(current_text, TextType.TEXT))

    return new_nodes


def split_nodes_image(old_nodes):
    """Processes markdown images ![alt](src) and converts them into IMAGE TextNodes."""
    new_nodes = []
    
    image_pattern = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')  # Matches ![alt](src)

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue  # Skip non-text nodes

        current_text = node.text
        match = image_pattern.search(current_text)

        while match:
            before = current_text[:match.start()]  # Text before the image
            alt_text = match.group(1)  # Extracted alt text
            image_src = match.group(2)  # Extracted image URL
            after = current_text[match.end():]  # Text after the image
            
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, image_src))  # Create IMAGE node
            
            current_text = after  # Update current_text to remaining portion
            match = image_pattern.search(current_text)  # Search for next image

        if current_text:  # Add remaining text if any
            new_nodes.append(TextNode(current_text, TextType.TEXT))

    return new_nodes




def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    
    # Use simple delimiter for bold, italic, code
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "__", TextType.BOLD)  # Add this line
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC) 
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)
    
    return nodes
