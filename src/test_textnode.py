import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    # This is a new test method
    def test_text_property(self):
        node = TextNode("Hello, world!", TextType.TEXT)
        self.assertEqual(node.text, "Hello, world!")
    
    # Another test method
    def test_different_types_not_equal(self):
        node1 = TextNode("Same text", TextType.BOLD)
        node2 = TextNode("Same text", TextType.ITALIC)
        self.assertNotEqual(node1, node2)

if __name__ == "__main__":
    unittest.main()