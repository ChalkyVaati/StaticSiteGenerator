import unittest
from gencontent import extract_title  # import from the right module

class TestExtractTitle(unittest.TestCase):
    def test_extract_simple_title(self):
        md = "# Simple Title"
        self.assertEqual(extract_title(md), "Simple Title")
    
    def test_extract_title_with_formatting(self):
        md = "# Title with **bold** and *italic*"
        self.assertEqual(extract_title(md), "Title with **bold** and *italic*")
    
    def test_extract_title_with_leading_trailing_spaces(self):
        md = "#    Spaced Title    "
        self.assertEqual(extract_title(md), "Spaced Title")
    
    def test_no_title_raises_exception(self):
        md = "This markdown has no title"
        with self.assertRaises(ValueError):
            extract_title(md)
    
    def test_title_not_first_line(self):
        md = "Some text\n# Title on second line"
        self.assertEqual(extract_title(md), "Title on second line")

if __name__ == "__main__":
    unittest.main()
# run Test extract py.