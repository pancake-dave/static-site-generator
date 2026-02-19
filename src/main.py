import sys

from copy_static import purge_public, copy_static
from generate_pages_recursive import generate_pages_recursive

def main():
    static_path = "./static/"
    public_path = "./docs"
    content_path = "./content"
    template_path = "./template.html"


    if len(sys.argv) < 2:
        basepath = "/"
    else:
        basepath = sys.argv[1]
    print(f"Base path: '{basepath}'")

    print("Purging public directory...")
    if purge_public(public_path):
        print("Copying static files to public directory...")
        copy_static(public_dir=public_path, static_dir=static_path)

    generate_pages_recursive(content_path, template_path, public_path, basepath)

main()