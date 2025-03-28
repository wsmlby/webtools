import os
TAGS = {
    "{{GA_TAG}}": "pages/_includes/head-custom-google-analytics.html"
}


def template_fill(src_file, dest_file):
    """
    Fill the template with the actual content.
    :param src_file: Source file path containing template tags
    :param dest_file: Destination file path to save the filled content
    """
    with open(src_file, 'r') as f:
        content = f.read()

    # Replace each tag with its corresponding content
    for tag, replacement in TAGS.items():
        with open(replacement, 'r') as tag_file:
            tag_content = tag_file.read()
            content = content.replace(tag, tag_content)

    # Write the filled content to the destination file
    with open(dest_file, 'w') as f:
        f.write(content)

def main():
    SRC_DIR = "src"
    DESC_DIR = "pages"
    for fn in os.listdir(SRC_DIR):
        template_fill(os.path.join(SRC_DIR, fn), os.path.join(DESC_DIR, fn))


if __name__ == '__main__':
    main()