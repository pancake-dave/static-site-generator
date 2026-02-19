import os

from markdown_to_html import markdown_to_html_node
from extract_title_md import extract_title_md

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as md:
        content = md.read()
        lines = content.split("\n")
    with open(template_path, "r") as tp:
        template = tp.read()
    html_content = markdown_to_html_node(content).to_html()
    title = extract_title_md(lines)
    generated_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)

    with open(dest_path, "w") as new_page:
        new_page.write(generated_html)