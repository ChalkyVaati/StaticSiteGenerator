from textnode import TextNode, TextType, split_nodes_delimiter
from Split_image_and_links import split_nodes_image, split_nodes_link

def text_to_textnodes(text):

    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD) #For Bold
    nodes = split_nodes_delimiter(nodes, "_",  TextType.ITALIC) #For Italic
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)  # Process inline code
    nodes = split_nodes_image(nodes) #Handle images
    nodes = split_nodes_link(nodes) #Handle Links

    return nodes
