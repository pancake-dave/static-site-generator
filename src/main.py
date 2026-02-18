import shutil, os

from textnode import TextNode, TextType

def main():
    node = TextNode("Dummy text", TextType.LINK, "www.placek.com")
    # print(node)

def delete_public(path_public):
    shutil.rmtree(path_public)
    os.mkdir(path_public)

def copy_content(path_public, path_static):
    for item in os.listdir(path_static):
        if os.path.isfile(path_static + item):
            print(path_static + item + " is a file")
        else:
            print(path_static + item + " is a dir")
            copy_content(path_public, path_static + item + "/")


main()
copy_content("../public/", "../static/")


# print(os.path.exists("../static/"))