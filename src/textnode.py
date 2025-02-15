import re
from enum import Enum
class TextType(Enum): 
    TEXT = "Normal" 
    BOLD = "Bold"
    ITALIC = "Italic"
    CODE = "Code" 
    LINKS = "Links"
    IMAGES = "Images"


class TextNode():

    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
       return self.text == other.text and self.text_type==other.text_type and self.url == other.url 

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"




def split_nodes_delimiter(old_nodes, delimiter, text_type):
    node_collection = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            node_collection.append(node)
            continue
        text_content = node.text
        delimiter_count = text_content.count(delimiter)
        if delimiter_count%2 != 0:
            raise Exception("missing closing or opening delimiter")
        new_nodes = []
        text_parts = text_content.split(delimiter)
        for i, part in enumerate(text_parts):
            if (i+1)%2 == 0:
                new_nodes.append(TextNode(part,text_type))
            else:
                new_nodes.append(TextNode(part,TextType.TEXT))
        node_collection.extend(new_nodes)
    return node_collection
        



def extract_markdown_images(text):
    images_text = re.findall(r"!\[.*?\]\(http.*?\)",text)
    if not images_text:
        return None
    images = []
    for image in images_text:
        alt = re.findall(r"(?<=\[)(.*)(?=\])",image)
        url = re.findall(r"http.*[^\)]",image)
        images.append((alt[0],url[0]))
    return images


def extract_markdown_links(text):
    links_text = re.findall(r"(?<!!)\[.*?\]\(http.*?\)",text)
    if not links_text:
        return None
    links = []
    for link in links_text:
        alt = re.findall(r"(?<=\[)(.*)(?=\])",link)
        url = re.findall(r"http.*[^\)]",link)
        links.append((alt[0],url[0]))
    return links



def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        text = node.text
        print(text)
        images = extract_markdown_images(text)
        if not images:
            new_nodes.append(node)
            continue
        print(images)
        for image in images:
            parts = re.split(r"!\[.*?\]\(http.*?\)", text, maxsplit=1)
            print(parts)
            if parts[0] != "":
                new_nodes.append(TextNode(parts[0],TextType.TEXT))
            new_nodes.append(TextNode(image[0],TextType.IMAGES,image[1]))
            text = parts[1]
        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        text = node.text
        print(text)
        links = extract_markdown_links(text)
        if not links:
            new_nodes.append(node)
            continue
        print(links)
        for link in links:
            parts = re.split(r"(?<!!)\[.*?\]\(http.*?\)", text, maxsplit=1)
            print(parts)
            if parts[0] !="":
                new_nodes.append(TextNode(parts[0],TextType.TEXT))
            new_nodes.append(TextNode(link[0],TextType.LINKS, link[1]))
            text = parts[1]
        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes


def rec_node_list(text):
    parts = re.split(r"!\[.*?\]\(http.*?\)",text, maxsplit=1)
    if (len(parts) == 1) and (parts[0] != " "):
        return [TextNode(parts[0],TextType.TEXT)]
    elif (len(parts) == 1) and (parts[0] == " "):
        return
    
    
    nodes_list = []
    if parts[0] != " ":
        nodes_list.append(TextNode(parts[0],TextType.TEXT))
        
        nodes_list.extend(rec_node_list(parts[1]))

    return nodes_list



def text_to_textnodes(text):
    print(text)
    bold_nodes = split_nodes_delimiter([TextNode(text,TextType.TEXT)],"**",TextType.BOLD)
    print("Bold nodes: ", bold_nodes)
    bold_italic_nodes = split_nodes_delimiter(bold_nodes,"*",TextType.ITALIC)
    print("bold and italic: ", bold_italic_nodes)
    code_bold_italic_nodes = split_nodes_delimiter(bold_italic_nodes, "'",TextType.CODE)
    print("code: ", code_bold_italic_nodes)
    and_images = split_nodes_image(code_bold_italic_nodes)
    print("images: ", and_images)
    and_links = split_nodes_link(and_images)
    print("links: ", and_links)
    fully_formatted = and_links
    print(fully_formatted)
    return fully_formatted
    

