import unittest
from textnode import TextNode,TextType
from htmlnode import HTMLNode,LEAFNode,ParentNode, text_node_to_html_node

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "This is a test", ["child1"], {"src":"https://localhost880", "href":"images/cool.jpg"})
        node2 = HTMLNode("p", "This is a test", ["child1"], {"src":"https://localhost880", "href":"images/cool.jpg"})

        self.assertEqual(node, node2)

    def test_normal(self):
        node = HTMLNode("p")
        node2 = HTMLNode("p")

        self.assertEqual(node, node2)


    def test_url(self):
        node = HTMLNode("p", "his is a test",  {"src":"https://localhost880", "href":"images/cool.jpg"})
        node2 = HTMLNode("p",  {"src":"https://localhost880", "href":"images/cool.jpg"})

        self.assertEqual(node.props_to_html(),node2.props_to_html())





class testLeafNode(unittest.TestCase):
    def test_with_children(self):
        node1 = LEAFNode("p","I am here", ["child1"]) 
        node2 = LEAFNode("p","I am here", ["child1"]) 

        self.assertEqual(node1,node2)

    def test_normal(self):
        node1 = LEAFNode("a","click me", {"href":"https://fake-site.com"})
        node2 = LEAFNode("a","click me", {"href":"https://fake-site.com"})
        self.assertEqual(node1,node2)

class testParentNode(unittest.TestCase):
    def test_just_leaf(self):
        node = ParentNode(
             "p",
       [
            LEAFNode("b", "Bold text"),
            LEAFNode(None, "Normal text"),
            LEAFNode("i", "italic text"),
            LEAFNode(None, "Normal text"),
        ])
        
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_parent_as_child(self):
        node = ParentNode("p",
                         [LEAFNode("b","Bold text"),
                          LEAFNode(None,"Normal text"),
                          LEAFNode("i","italic text"),
                          LEAFNode(None,"Normal text"),])

        node2 = ParentNode("p", [LEAFNode("b","Bold text"),node])

        self.assertEqual(node2.to_html(), "<p><b>Bold text</b><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></p>")



    def test_parent_with_no_children(self):
        node = ParentNode("p",[])

        self.assertEqual(node.to_html(), "<p></p>")



class testTextToHtmlNode(unittest.TestCase):
    def testText(self):
        node = text_node_to_html_node(TextNode("This is a text node",TextType.TEXT))
        print(node)
        self.assertEqual(node, LEAFNode(None,'This is a text node'))

    def testBold(self):
        node = text_node_to_html_node(TextNode("This is a text node", TextType.BOLD))
        self.assertEqual(node,LEAFNode('b','This is a text node'))

    def testLINK(self):
        node = text_node_to_html_node(TextNode("This is a text node", TextType.LINKS,"https://site.com"))
        self.assertEqual(node, LEAFNode("a","This is a text node",{"href":"https://site.com"}))

if __name__ == "__main__":
    unittest.main(verbosity=2)
