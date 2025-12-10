from textnode import TextNode, TextType

def main():
    node = TextNode("Dummy text", TextType.LINK, "www.placek.com")
    print(node)
# just this line
main()