import unittest
from gencontent import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_simple_title(self):
        markdown = "# Simple Title\nSome content"
        self.assertEqual(extract_title(markdown), "Simple Title")
    
    def test_extract_title_with_markdown(self):
        markdown = "# Title with **bold** and *italic*\nContent"
        self.assertEqual(extract_title(markdown), "Title with **bold** and *italic*")
    
    def test_title_with_whitespace(self):
        markdown = "#    Lots of spaces    \nContent"
        self.assertEqual(extract_title(markdown), "Lots of spaces")
    
    def test_no_title_throws_exception(self):
        markdown = "No title here\nJust content"
        with self.assertRaises(Exception):
            extract_title(markdown)

if __name__ == "__main__":
    unittest.main()