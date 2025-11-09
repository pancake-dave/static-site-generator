class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return ""
        attributes_list = []
        for attr, val in self.props.items():
            attributes_list.append(attr + '="' + val + '"')
        return " " + " ".join(attributes_list)

    def __repr__(self):
        return f"TAG: {self.tag} | VALUE: {self.value} | CHILDREN: {self.children} | PROPS: {self.props}"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value == None:
            raise ValueError("invalid HTML: no value")
        if self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("invalid HTML: no tag")
        if not self.children:
            raise ValueError("invalid HTML: parent element has to have at least one child")
        children_list = []
        for child in self.children:
            children_list.append(child.to_html())
        return f"<{self.tag}{self.props_to_html()}>{"".join(children_list)}</{self.tag}>"
