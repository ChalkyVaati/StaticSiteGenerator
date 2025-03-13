import unittest
from block_to_block_type import block_to_block_type, BlockType  

class TestBlockToBlockType(unittest.TestCase):

    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Subheading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Smallest Heading"), BlockType.HEADING)

    def test_code_block(self):
        self.assertEqual(block_to_block_type("```\nCode block\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```\nMultiple lines\nInside code\n```"), BlockType.CODE)

    def test_quote_block(self):
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("> Line 1\n> Line 2"), BlockType.QUOTE)

    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("- Item 1\n- Item 2\n- Item 3"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("- First\n- Second\n- Third"), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. First item\n2. Second item\n3. Third item"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("1. Apple\n2. Banana\n3. Cherry"), BlockType.ORDERED_LIST)

    def test_paragraph(self):
        self.assertEqual(block_to_block_type("This is just a paragraph."), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("No special characters at the start."), BlockType.PARAGRAPH)

    def test_mixed_content(self):
        """ Ensure function correctly identifies standalone blocks """
        self.assertEqual(block_to_block_type("> Quote line\nRegular text"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("- List item\nNormal paragraph"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("1. Ordered item\n- Unordered item"), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()