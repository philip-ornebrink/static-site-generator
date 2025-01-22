import unittest

from textnode import TextNode, TextType, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, rec_node_list, split_nodes_image, split_nodes_link


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_normal(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node,node2)

    def test_url(self):
        node = TextNode("This is a text node", TextType.TEXT, None)
        node2 = TextNode("This is a text node", TextType.TEXT, None)
        self.assertEqual(node,node2)



class TestSplitFunktion(unittest.TestCase):
    def testBold(self):
        old_node = TextNode("This is *bold* node", TextType.TEXT)
        new_nodes = split_nodes_delimiter([old_node],"*",TextType.BOLD)
        match = [TextNode("This is ", TextType.TEXT),TextNode("bold", TextType.BOLD),TextNode(" node",TextType.TEXT)]
        self.assertEqual(new_nodes,match)

    def testItalic(self):
        old_node1 = TextNode("Make this 'word' italic please", TextType.TEXT)
        old_node2 = TextNode("Make the next 'word' bold 'please'",TextType.TEXT)
        old_node3 = TextNode("This is already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([old_node1,old_node2,old_node3],"'", TextType.ITALIC)
        match=[TextNode("Make this ", TextType.TEXT),TextNode("word",TextType.ITALIC),TextNode(" italic please", TextType.TEXT), TextNode("Make the next ", TextType.TEXT),TextNode("word", TextType.ITALIC), TextNode(" bold ", TextType.TEXT),TextNode("please",TextType.ITALIC),TextNode("",TextType.TEXT),TextNode("This is already bold",TextType.BOLD)]
        self.assertEqual(new_nodes,match)

class TestExtractFunctions(unittest.TestCase):
    def testExtractImages(self):
        extracted = extract_markdown_images("detta är ![test image](https://minsida.com) hoppas den fungerar")
        self.assertEqual(extracted,[("test image","https://minsida.com")])

    def testExtractLinks(self):
        extracted = extract_markdown_links("detta är [test link](https://minsida.com) hoppas den fungerar")
        self.assertEqual(extracted,[("test link","https://minsida.com")])

    def testExtractMany(self):
        extracted = extract_markdown_links("this contains [första](https://test1.com) hoppas den fungerar, här är [andra](https://andra.com) hoppas denna fungerar också")
        self.assertEqual(extracted, [("första","https://test1.com"),("andra","https://andra.com")])                 

    def testExtractRight(self):
        extracted = extract_markdown_images("this is an ![image](https://image.com) this is a link [link](https://link.com) test")
        self.assertEqual(extracted, [("image","https://image.com")])




class TestSplitNodes(unittest.TestCase):

    def testSplitOne(self):
        nodes = rec_node_list("detta är en ![image](https://image.com) hoppas den fungerar")
        match = [TextNode("detta är en ", TextType.TEXT),TextNode(" hoppas den fungerar", TextType.TEXT)]
        self.assertEqual(nodes,match)

    def testSplitTwo(self):
        nodes = rec_node_list("detta är en ![image](https://image.com) hoppas den fungerar, detta är nästa ![image2](https://image2.com) den borde fungerar")
        match = [TextNode("detta är en ", TextType.TEXT),TextNode(" hoppas den fungerar, detta är nästa ", TextType.TEXT), TextNode(" den borde fungerar", TextType.TEXT)]
        self.assertEqual(nodes,match)

    def testSplitThree(self):
        nodes = rec_node_list("detta är en ![image](https://image.com) hoppas den fungerar, detta är nästa ![image2](https://image2.com) den borde fungerar. den sista blilden ![image3](https://image3.com) är grym!")
        match = [TextNode("detta är en ", TextType.TEXT),TextNode(" hoppas den fungerar, detta är nästa ", TextType.TEXT), TextNode(" den borde fungerar. den sista blilden ", TextType.TEXT),TextNode(" är grym!",TextType.TEXT)]
        self.assertEqual(nodes, match)


class TestSplitNodes2(unittest.TestCase):
    
    def testSplitOneImage(self):
        nodes = split_nodes_image([TextNode("This is ![image1](https://image1.com) it looks nice",TextType.TEXT)])
        match = [TextNode("This is ", TextType.TEXT),TextNode("image1",TextType.IMAGES,"https://image1.com"),TextNode(" it looks nice",TextType.TEXT)]
        self.assertEqual(nodes, match)

    def testSplitOneLink(self):
        nodes = split_nodes_link([TextNode("This is [image1](https://image1.com) it looks nice",TextType.TEXT)])
        match = [TextNode("This is ", TextType.TEXT),TextNode("image1",TextType.LINKS,"https://image1.com"),TextNode(" it looks nice",TextType.TEXT)]
        self.assertEqual(nodes, match)

    def testSplitThreeLinksTwoNodes(self):
        nodes = split_nodes_link([TextNode("this is [link1](https://link1.com) and this is [link2](https://link2.com)", TextType.TEXT),TextNode("[link3](https://link3.com) is the best",TextType.TEXT)]) 
        match = [TextNode("this is ", TextType.TEXT),TextNode("link1",TextType.LINKS,"https://link1.com"),TextNode(" and this is ",TextType.TEXT),TextNode("link2",TextType.LINKS,"https://link2.com"),TextNode("link3",TextType.LINKS,"https://link3.com"),TextNode(" is the best",TextType.TEXT)]
        self.assertEqual(nodes, match)

if __name__ == "__main__":
    unittest.main()
