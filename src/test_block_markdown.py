import unittest
from block_markdown import markdown_to_blocks, block_to_blocktype, markdown_to_html_node



class TestSplitText(unittest.TestCase):
    def splitintoTwo(self):
        text = "Paragraf 1\n\n Parafgrafandra \n \n  paragraf tredje"
        parts = markdown_to_blocks(text)
        match = ["Paragraf 1","Parafgrafandra", "paragraf tredje"]
        self.assertEqual(parts,match)


class TestClassifyBlock(unittest.TestCase):

    def test_heading(self):
        block = "### detta är en heading"
        block_type = block_to_blocktype(block)
        match = "heading"
        self.assertEqual(block_type, match)
        
    def test_codeblock(self):
        block = "´´´detta är ett code block´´´"
        block_type = block_to_blocktype(block)
        match = "code"
        self.assertEqual(block_type, match)

    def test_quote(self):
        block =">Om du är i helvetet\n>fortsätt gå"
        block_type = block_to_blocktype(block)
        match = "quote" 
        self.assertEqual(block_type,match)

    def test_unord_list(self):
        block = "- item1\n- item 2\n- item3"
        block_type = block_to_blocktype(block)
        match = "unorderd list"
        self.assertEqual(block_type,match)

    def test_order_list(self):
        block = "1. item1\n2. item3\n3. item3"
        block_type = block_to_blocktype(block)
        match = "ordered list"
        self.assertEqual(block_type, match)

    def test_normal(self):
        block = "detta är en norml paragraf"
        block_type = block_to_blocktype(block)
        match = "normal"
        self.assertEqual(block_type, match)



class TestMarkdownToHtml(unittest.TestCase):

    def test_heading_and_quote(self):
        markdown = "### Title of my first markdown\n\n>To be or not to be\n>that is the question."
        html = markdown_to_html_node(markdown)
        match = "<div><h3>Title of my first markdown</h3><blockquote>To be or not to be\nthat is the question.</blockquote></div>"
        self.assertEqual(html.to_html(), match)

    def test_heading_and_quote_with_bold(self):
        markdown = "### Title of my **first** markdown\n\n>To be or not to be\n>that is the question."
        html = markdown_to_html_node(markdown)
        print(html.to_html())
        match = "<div><h3>Title of my <b>first</b> markdown</h3><blockquote>To be or not to be\nthat is the question.</blockquote></div>"
        self.assertEqual(html.to_html(), match)

    def test_code_and_ul(self):
        markdown = "´´´This code page is my first code page´´´\n\n- item1\n- item2"
        html = markdown_to_html_node(markdown)
        match = "<div><pre><code>This code page is my first code page</code></pre><ul><li>item1</li><li>item2</li></ul></div>"
        self.assertEqual(html.to_html(),match)

    def test_code_and_ul(self):
        markdown = "´´´This code page is my *first code* page´´´\n\n- item1\n- item2"
        html = markdown_to_html_node(markdown)
        match = "<div><pre><code>This code page is my <i>first code</i> page</code></pre><ul><li>item1</li><li>item2</li></ul></div>"
        self.assertEqual(html.to_html(),match)

    def test_ol_and_p(self):
        markdown = "1. first item\n2. second item\n\nThis is a normal paragraph"
        html = markdown_to_html_node(markdown)
        match = "<div><ol><li>first item</li><li>second item</li></ol><p>This is a normal paragraph</p></div>"
        self.assertEqual(html.to_html(),match)
