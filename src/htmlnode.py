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
        return " ".join(attributes_list)

    def __repr__(self):
        return f"TAG: {self.tag} | VALUE: {self.value} | CHILDREN: {self.children} | PROPS: {self.props}"