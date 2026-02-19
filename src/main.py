from textnode import TextNode, TextType
from copy_static import purge_public, copy_static
from generate_page import generate_page

def main():
    node = TextNode("Dummy text", TextType.LINK, "www.placek.com")
    print(node)

    if purge_public():
        copy_static()

    generate_page("./content/index.md", "./template.html", "./public/index.html")

main()