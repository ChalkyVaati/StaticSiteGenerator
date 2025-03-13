from enum import Enum
from htmlnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node, text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    OLIST = "ordered_list"
    ULIST = "unordered_list"

def markdown_to_blocks(markdown):
    """Splits markdown into logical blocks, ignoring empty lines."""
    blocks = markdown.strip().split("\n\n")
    return [block.strip() for block in blocks if block.strip()]

def block_to_block_type(block):
    """Determines the block type based on its content."""
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.lstrip().startswith("- ") for line in lines):
        return BlockType.ULIST
    if all(line.lstrip().split(". ", 1)[0].isdigit() for line in lines):
        return BlockType.OLIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    """Converts markdown text into an HTML node tree."""
    blocks = markdown_to_blocks(markdown)
    children = [block_to_html_node(block) for block in blocks]
    return ParentNode("div", children)

def block_to_html_node(block):
    """Converts a markdown block into its respective HTML node."""
    block_type = block_to_block_type(block)

    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.OLIST:
        return olist_to_html_node(block)
    if block_type == BlockType.ULIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    
    raise ValueError(f"Invalid block type: {block_type}")


def text_to_children(text):
    """Converts plain text into a list of HTML nodes with inline formatting."""
    nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in nodes]

def paragraph_to_html_node(block):
    """Converts a paragraph block to an HTML node."""
    text = " ".join(block.split("\n"))  # Join broken lines into a single paragraph
    return ParentNode("p", text_to_children(text))

def heading_to_html_node(block):
    """Converts a markdown heading to an HTML node."""
    level = block.count("#", 0, block.find(" "))  # Count the leading #
    if level < 1 or level > 6:
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1:].strip()
    return ParentNode(f"h{level}", text_to_children(text))

def code_to_html_node(block):
    """Converts a code block to an HTML node."""
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block syntax")
    
    code_text = "\n".join(block.split("\n")[1:-1]).strip()  # Remove opening & closing ```
    return ParentNode("pre", [ParentNode("code", [TextNode(code_text, TextType.CODE)])])

def olist_to_html_node(block):
    """Converts an ordered list markdown block to an HTML node."""
    items = block.split("\n")
    html_items = []
    for item in items:
        if ". " not in item:
            raise ValueError("Invalid ordered list syntax")
        text = item.split(". ", 1)[1].strip()
        html_items.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ol", html_items)

def ulist_to_html_node(block):
    """Converts an unordered list markdown block to an HTML node."""
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item.lstrip().lstrip("- ").strip()  # For items that start with "- "
        html_items.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ul", html_items)

def quote_to_html_node(block):
    """Converts a blockquote markdown block to an HTML node."""
    lines = [line.lstrip("> ").strip() for line in block.split("\n")]
    return ParentNode("blockquote", text_to_children(" ".join(lines)))