import re
from htmlnode import HTMLNode,LEAFNode,ParentNode, text_node_to_html_node
from textnode import text_to_textnodes

def markdown_to_blocks(markdown):
    blocks = re.split(r"\n\s*\n", markdown)
    trimmed = []
    for block in blocks:
        trimmed.append(block.strip())
    return trimmed
    

def block_to_blocktype(block):
    if re.search(r"^\#{1,6}\s", block):
        return "heading"
    if re.search(r"^(\´{3})(.+)(\´{3})$",block):
        return "code"
    
    if all([line.startswith('>') for line in block.splitlines()]):
        return "quote"

    if all([line.startswith('- ') for line in block.splitlines()]) or all([line.startswith('* ') for line in block.splitlines()]):
        return "unorderd list"

    if all([line.startswith(f'{index+1}. ') for index,line in enumerate(block.splitlines())]):
        return "ordered list"

    return "normal"
    

def text_to_children(text):
    textnodes = text_to_textnodes(text)
    leaf_nodes_list = []
    for node in textnodes:
        leaf_nodes_list.append(text_node_to_html_node(node))
    return leaf_nodes_list


def block_to_quote(block):
    cleaned_block = block.lstrip("> ")
    child_nodes = text_to_children(cleaned_block)
    blockNode = ParentNode("blockquote", child_nodes)
    return blockNode

def block_to_ul_list(block):
    lines = block.splitlines()
    list_items = []
    for line in lines:
        clean_line = re.sub(r"[\-\*]\s","", line)
        child_nodes = text_to_children(clean_line)
        item_node = ParentNode("li", child_nodes)
        list_items.append(item_node)
    blockNode = ParentNode("ul", list_items)
    return blockNode

def block_to_ol_list(block):
    lines = block.splitlines()
    list_items = []
    for index,line in enumerate(lines):
        line_1 = line.strip(f"{index+1}. ")
        child_nodes = text_to_children(line_1)
        item_node = ParentNode("li", child_nodes)
        list_items.append(item_node)
    blockNode = ParentNode("ol", list_items)
    return blockNode

def block_to_code(block):
    cleaned_block = block.strip("´´´")
    child_nodes = text_to_children(cleaned_block)
    code_node = ParentNode("code", child_nodes)
    blockNode = ParentNode("pre", [code_node])
    return blockNode

def block_to_heading(block):
    heading_type = block.count("#")
    cleaned_block = block.split(" ", 1)[1]
    child_nodes = text_to_children(cleaned_block)
    blockNode = ParentNode(f"h{heading_type}",child_nodes)
    return blockNode

def block_to_paragraph(block):
    child_nodes = text_to_children(block)
    blockNode = ParentNode("p",child_nodes)
    return blockNode



def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        block_type = block_to_blocktype(block)
        if block_type == "heading":
            blockNode = block_to_heading(block)
            block_nodes.append(blockNode)

        elif block_type == "code":
            blockNode = block_to_code(block)
            block_nodes.append(blockNode)

        elif block_type == "quote":
            blockNode = block_to_quote(block)
            block_nodes.append(blockNode)

        elif block_type == "unorderd list":
            blockNode = block_to_ul_list(block)
            block_nodes.append(blockNode)

        elif block_type == "ordered list":
            blockNode = block_to_ol_list(block)
            block_nodes.append(blockNode)

        elif block_type == "normal":
            blockNode = block_to_paragraph(block)
            block_nodes.append(blockNode)

    page_node = ParentNode("div", block_nodes)
    return page_node

        
def extract_title(markdown):
    title_1 = re.search(r"^\#{1} .*", markdown)
    title_2 = title_1.group().strip("# ")
    return title_2.strip()
