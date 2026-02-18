import os, shutil

def purge_public():
    public_path = "./public/"
    try:
        if not os.path.exists(public_path):
            os.mkdir(public_path)
            return True
        shutil.rmtree(public_path)
        os.mkdir(public_path)
        return True
    except Exception as e:
        print(f"Fatal error: failed to purge '{public_path}' due to: {e}")

def copy_content(path_public="", path_static=""):
    current_public_path = "./public/" + path_public
    current_static_path = "./static/" + path_static
    try:
        for item in os.listdir(current_static_path):
            if os.path.isfile(os.path.join(current_static_path, item)):
                shutil.copy(os.path.join(current_static_path, item), os.path.join(current_public_path, item))
            else:
                if not os.path.exists(os.path.join(current_public_path, item)):
                    os.mkdir(os.path.join(current_public_path, item))
                copy_content(os.path.join(path_public, item), os.path.join(path_static, item))
    except Exception as e:
        print(f"Fatal error: failed to generate content due to: {e}")