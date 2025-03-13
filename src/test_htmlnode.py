import unittest
from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_leaf_no_value(self):
        # Use assertRaises to check that LeafNode raises ValueError when value is None
        with self.assertRaises(ValueError):
            node = LeafNode("div", None)
    
    def test_props_to_html_empty(self):
        # Test with no props
        node = HTMLNode("div", "hello", None, {})
        self.assertEqual(node.props_to_html(), "")
        
    def test_props_to_html_with_props(self):
        # Test with some props
        node = HTMLNode("a", "Click me", None, {"href": "https://example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com"')
        
    def test_something_else(self):
        # Add another test for different functionality
        pass
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
   #test for ValueError
    def test_leaf_no_value(self):
        node = LeafNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()
    #test for no Tags
    def test_leaf_no_tag(self):
        node = LeafNode(None, "Just some text")
        self.assertEqual(node.to_html(), "Just some text")
    #test for a node with props 
    def test_leaf_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.example.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.example.com">Click me!</a>')
if __name__ == "__main__":
    unittest.main()