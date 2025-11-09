import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_nested_parents(self):
        child_two = ParentNode(tag="span", props={"class":"two"}, children=[LeafNode("span", "last child")])
        child_one = ParentNode(tag="span",props={"class":"one"}, children=[child_two])
        parent = ParentNode("div", [child_one])
        self.assertEqual(parent.to_html(), '<div><span class="one"><span class="two"><span>last child</span></span></span></div>')

    def test_to_html_with_multiple_nodes(self):
        parent_node = ParentNode(
    "p",
    [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        ParentNode("a",
    [
                LeafNode("span", "span text"),
                LeafNode(None, "Normal text"),
                LeafNode("button", "button text"),
                LeafNode(None, "Normal text"),
            ],),
        LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(parent_node.to_html(), '<p><b>Bold text</b>Normal text<i>italic text</i><a><span>span text</span>Normal text<button>button text</button>Normal text</a>Normal text</p>')

    def test_to_html_with_no_children_raises(self):
        with self.assertRaises(ValueError):
            ParentNode("div", []).to_html()

    def test_to_html_with_no_tag_raises(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode("span", "x")]).to_html()

    def test_props_are_rendered(self):
        parent = ParentNode("div", [LeafNode(None, "x")], {"id": "root", "data-x": "1"})
        html = parent.to_html()
        self.assertTrue(html.startswith('<div id="root" data-x="1">'))
        self.assertTrue(html.endswith("</div>"))


if __name__ == "__main__":
    unittest.main()