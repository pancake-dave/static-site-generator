from textnode import TextNode, TextType
from copy_static import purge_public, copy_static
from generate_page import generate_page
from generate_pages_recursive import generate_pages_recursive

def main():
    print("Purging public directory...")
    if purge_public():
        print("Copying static files to public directory...")
        copy_static()

    generate_pages_recursive("./content", "./template.html", "./public")

main()