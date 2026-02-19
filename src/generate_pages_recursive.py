import os, shutil
from generate_page import generate_page

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        if os.path.isfile(os.path.join(dir_path_content, item)):
            page_name = item.split(".")[0] + ".html"
            generate_page(os.path.join(dir_path_content, item), template_path, os.path.join(dest_dir_path, page_name))
        else:
            if os.path.isdir(os.path.join(dir_path_content, item)):
                generate_pages_recursive(os.path.join(dir_path_content, item), template_path, os.path.join(dest_dir_path, item))