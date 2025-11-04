import unittest

from htmlnode import HTMLNode

class TestHtmlNode(unittest.TestCase):
    def test_props_to_html(self):
        tag, value, children, props = "a", "placek", None, {"href":"www.placek.pl", "target":"blank"}
        node = HTMLNode(tag, value, children, props)
        props_str = 'href="www.placek.pl" target="blank"'
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


if __name__ == "__main__":
    unittest.main()