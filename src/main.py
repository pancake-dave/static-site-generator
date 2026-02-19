from textnode import TextNode, TextType
from copy_static import purge_public, copy_static

def main():
    node = TextNode("Dummy text", TextType.LINK, "www.placek.com")
    print(node)

    if purge_public():
        copy_static()

main()