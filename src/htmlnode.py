
from textnode import TextNode, TextType

class HTMLNode():

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props==None:
            return None
        prop_string = ""
        for key,item in self.props.items():
            prop_string = prop_string + f" {key}={item}"
        return prop_string

    def __eq__(self,other):
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props

    def __repr__(self):
        return f"HTMLNode(TAG: {self.tag} VALUE: {self.value} CHILDREN:{self.children} PROPS:{self.props})"



class LEAFNode(HTMLNode):

    def __init__(self, tag, value, props=None):
        super().__init__(tag, value,None, props)
        
    def to_html(self):
        if self.value==None:
            raise ValueError()
        elif self.tag == None:
            return self.value
        elif self.props==None:
            print(f"<{self.tag}>{self.value}</{self.tag}>")
            return f"<{self.tag}>{self.value}</{self.tag}>"
        else: return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"




class ParentNode(HTMLNode):
    def __init__(self,tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise valueError("missing tag")
        elif self.children is None:
            raise valueError("missing children")
        starttag = f"<{self.tag}>"
        for child in self.children:
            starttag += child.to_html()
        starttag += f"</{self.tag}>"
        return starttag
            

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LEAFNode(None,text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LEAFNode('b',text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LEAFNode('i',text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LEAFNode('code',text_node.text)
    elif text_node.text_type == TextType.LINKS:
        return LEAFNode('a',text_node.text,{'href':text_node.url})
    elif text_node.text_type == TextType.IMAGES:
        return LEAFNode('img',"",{'src':text_node.url,'alt':'alt'})
    else:
        return TextType.BOLD
