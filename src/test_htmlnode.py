import unittest

from htmlnode import HTMLNode, LeafNode

class TestHtmlNode(unittest.TestCase):
    def test_props_to_html(self):
        tag, value, children, props = "a", "placek", None, {"href":"www.placek.pl", "target":"blank"}
        node = HTMLNode(tag, value, children, props)
        props_str = ' href="www.placek.pl" target="blank"'
        self.assertEqual(node.props_to_html(), props_str)
    def test_props_to_html_none(self):
        node = HTMLNode()
        props_str = ""
        self.assertEqual(node.props_to_html(), props_str)
    def test_repr(self):
        tag, value, children, props = "a", "placek", None, {"href":"www.placek.pl", "target":"blank"}
        node = HTMLNode(tag, value, children, props)
        repr_str = f"TAG: {tag} | VALUE: {value} | CHILDREN: {children} | PROPS: {props}"
        self.assertEqual(node.__repr__(), repr_str)

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
    def test_leaf_to_html_value_error(self):
        node = LeafNode("a", None, {"href": "https://www.google.com"})
        self.assertRaises(ValueError)
    def test_leaf_to_html_plain(self):
        node = LeafNode(None, "this is plain text")
        self.assertEqual(node.to_html(), "this is plain text")


if __name__ == "__main__":
    unittest.main()