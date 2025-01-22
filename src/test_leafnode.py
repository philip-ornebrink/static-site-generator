import unittest

from leafnode import LEAFNode


class testLeafNode(unittest.TestCase):
    def test_with_children(self):
        node1 = LEAFNode("p","I am here", ["child1"]) 
        node2 = LEAFNode("p","I am here", ["child1"]) 

        self.assertEqual(node1,node2)

    def test_normal(self):
        node1 = LEAFNode("a","click me", {"href":"https://fake-site.com"})
        node2 = LEAFNode("a","click me", {"href":"https://fake-site.com"})
        self.assertEqual(node1,node2)
