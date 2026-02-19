def extract_title_md(markdown):
    for line in markdown:
        if line.startswith("# "):
            return line.strip("#").strip()
    raise Exception("no h1 header found")