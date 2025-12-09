from block_markdown import markdown_to_blocks, block_to_block_type, BlockType
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType
from htmlnode import LeafNode, ParentNode

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

def block_to_html_node(block):
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
    raise ValueError("invalid block type")


def paragraph_to_html_node(block):
    lines = block.splitlines()
    stripped_lines = [line.strip() for line in lines]
    normalized_block =  " ".join(stripped_lines)
    return ParentNode(tag="p", children=text_to_children(normalized_block))

def heading_to_html_node(block):
    heading_size = 0
    for char in block:
        if char == "#":
            heading_size += 1
        else:
            break
    block = block[heading_size:]
    block = block.lstrip()
    return ParentNode(tag=f"h{heading_size}", children=text_to_children(block))

def code_to_html_node(block):
    node = TextNode(block.strip("```").lstrip(), TextType.CODE)
    processed_node = text_node_to_html_node(node)
    return ParentNode(tag="pre", children=[processed_node])

def olist_to_html_node(block):
    lines = block.splitlines()
    stripped_lines = []
    for i in range(len(lines)):
        stripped_lines.append(lines[i].lstrip(f"{i + 1}. "))
    elements = parse_list_elements(stripped_lines)
    return ParentNode(tag="ol", children=elements)

def ulist_to_html_node(block):
    lines = block.splitlines()
    stripped_lines = [line.lstrip("- ") for line in lines]
    elements = parse_list_elements(stripped_lines)
    return ParentNode(tag="ul", children=elements)

def quote_to_html_node(block):
    lines = block.splitlines()
    stripped_lines = [line.lstrip("> ") for line in lines]
    filtered_block = " ".join(stripped_lines)
    return ParentNode(tag="blockquote", children=text_to_children(filtered_block))

# santa lil helpers
def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes

def parse_list_elements(elements):
    result = []
    for list_element in elements:
        parsed_element = text_to_children(list_element)
        result.append(ParentNode("li", parsed_element))
    return result