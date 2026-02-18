from textnode import TextNode, TextType
from copy_contents import purge_public, copy_content

def main():
    node = TextNode("Dummy text", TextType.LINK, "www.placek.com")
    print(node)

    if purge_public():
        copy_content()

main()