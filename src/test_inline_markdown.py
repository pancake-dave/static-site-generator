import unittest
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes
)

from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )


class TestExtract(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_multiple_images(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([('to boot dev', 'https://www.boot.dev')], matches)

    def test_extract_markdown_multiple_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([('to boot dev', 'https://www.boot.dev'), ('to youtube', 'https://www.youtube.com/@bootdotdev')], matches)

class TestSplitURLLink(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )


class TestSplitEdgeCases(unittest.TestCase):
    def test_no_images(self):
        node = TextNode("no pics here", TextType.TEXT)
        self.assertEqual(split_nodes_image([node]), [node])

    def test_no_links(self):
        node = TextNode("no links here", TextType.TEXT)
        self.assertEqual(split_nodes_link([node]), [node])

    def test_non_text_node_passthrough(self):
        node = TextNode("already link", TextType.LINK, "http://x")
        self.assertEqual(split_nodes_link([node]), [node])

    def test_image_at_start(self):
        node = TextNode("![alt](u) end", TextType.TEXT)
        out = split_nodes_image([node])
        self.assertEqual(out, [
            TextNode("alt", TextType.IMAGE, "u"),
            TextNode(" end", TextType.TEXT),
        ])

    def test_image_at_end(self):
        node = TextNode("begin ![alt](u)", TextType.TEXT)
        out = split_nodes_image([node])
        self.assertEqual(out, [
            TextNode("begin ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "u"),
        ])

    def test_link_at_start(self):
        node = TextNode("[a](u) end", TextType.TEXT)
        out = split_nodes_link([node])
        self.assertEqual(out, [
            TextNode("a", TextType.LINK, "u"),
            TextNode(" end", TextType.TEXT),
        ])

    def test_link_at_end(self):
        node = TextNode("begin [a](u)", TextType.TEXT)
        out = split_nodes_link([node])
        self.assertEqual(out, [
            TextNode("begin ", TextType.TEXT),
            TextNode("a", TextType.LINK, "u"),
        ])

    def test_multiple_images(self):
        node = TextNode(
            "a ![x](u1) b ![y](u2) c", TextType.TEXT
        )
        out = split_nodes_image([node])
        self.assertEqual(out, [
            TextNode("a ", TextType.TEXT),
            TextNode("x", TextType.IMAGE, "u1"),
            TextNode(" b ", TextType.TEXT),
            TextNode("y", TextType.IMAGE, "u2"),
            TextNode(" c", TextType.TEXT),
        ])

    def test_multiple_links(self):
        node = TextNode(
            "a [x](u1) b [y](u2) c", TextType.TEXT
        )
        out = split_nodes_link([node])
        self.assertEqual(out, [
            TextNode("a ", TextType.TEXT),
            TextNode("x", TextType.LINK, "u1"),
            TextNode(" b ", TextType.TEXT),
            TextNode("y", TextType.LINK, "u2"),
            TextNode(" c", TextType.TEXT),
        ])

    def test_adjacent_images(self):
        node = TextNode("![x](u1)![y](u2)", TextType.TEXT)
        out = split_nodes_image([node])
        self.assertEqual(out, [
            TextNode("x", TextType.IMAGE, "u1"),
            TextNode("y", TextType.IMAGE, "u2"),
        ])

    def test_adjacent_links(self):
        node = TextNode("[x](u1)[y](u2)", TextType.TEXT)
        out = split_nodes_link([node])
        self.assertEqual(out, [
            TextNode("x", TextType.LINK, "u1"),
            TextNode("y", TextType.LINK, "u2"),
        ])

    def test_trailing_text_after_last_match(self):
        node = TextNode("[x](u1) tail", TextType.TEXT)
        out = split_nodes_link([node])
        self.assertEqual(out, [
            TextNode("x", TextType.LINK, "u1"),
            TextNode(" tail", TextType.TEXT),
        ])

    def test_leading_text_before_first_match(self):
        node = TextNode("lead ![x](u1)", TextType.TEXT)
        out = split_nodes_image([node])
        self.assertEqual(out, [
            TextNode("lead ", TextType.TEXT),
            TextNode("x", TextType.IMAGE, "u1"),
        ])

    def test_mixed_images_and_links_separate_passes(self):
        node = TextNode("a ![x](u1) b [y](u2) c", TextType.TEXT)
        mid = split_nodes_image([node])
        out = split_nodes_link(mid)
        self.assertEqual(out, [
            TextNode("a ", TextType.TEXT),
            TextNode("x", TextType.IMAGE, "u1"),
            TextNode(" b ", TextType.TEXT),
            TextNode("y", TextType.LINK, "u2"),
            TextNode(" c", TextType.TEXT),
        ])

    # python
    def test_link_label_with_spaces_and_punct(self):
        node = TextNode("[click here!](https://ex.com)", TextType.TEXT)
        out = split_nodes_link([node])
        self.assertEqual(out, [
            TextNode("click here!", TextType.LINK, "https://ex.com"),
        ])

    def test_empty_label(self):
        node = TextNode("[](/u)", TextType.TEXT)
        out = split_nodes_link([node])
        self.assertEqual(out, [
            TextNode("", TextType.LINK, "/u"),
        ])

    def test_empty_url(self):
        node = TextNode("[x]()", TextType.TEXT)
        out = split_nodes_link([node])
        self.assertEqual(out, [
            TextNode("x", TextType.LINK, ""),
        ])

    def test_not_markdown_like_text(self):
        # parentheses in URL and brackets in label prevent matches by your regex
        node1 = TextNode("![alt](https://ex.com/img(1).png)", TextType.TEXT)
        node2 = TextNode("[text [inner]](u)", TextType.TEXT)
        self.assertEqual(split_nodes_image([node1]), [node1])
        self.assertEqual(split_nodes_link([node2]), [node2])

    def test_adjacent_mixed_supported(self):
        node = TextNode("![a b](u1)[c d](u2)", TextType.TEXT)
        out = split_nodes_link(split_nodes_image([node]))
        self.assertEqual(out, [
            TextNode("a b", TextType.IMAGE, "u1"),
            TextNode("c d", TextType.LINK, "u2"),
        ])

class TestTextToTextNodes(unittest.TestCase):
    def test_all_functions(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        result = [
                    TextNode("This is ", TextType.TEXT),
                    TextNode("text", TextType.BOLD),
                    TextNode(" with an ", TextType.TEXT),
                    TextNode("italic", TextType.ITALIC),
                    TextNode(" word and a ", TextType.TEXT),
                    TextNode("code block", TextType.CODE),
                    TextNode(" and an ", TextType.TEXT),
                    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                    TextNode(" and a ", TextType.TEXT),
                    TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(nodes, result)


if __name__ == "__main__":
    unittest.main()
