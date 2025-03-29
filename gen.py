import os
TAGS = {
    "{{GA_TAG}}": "docs/_includes/head-custom-google-analytics.html",
    "{{SIDEBAR_STYLE}}": "includes/sidebar_style.html",
    "{{SIDEBAR_HTML}}":"includes/sidebar.html"
}

SEO= {
    "bbox.html": {
        "TITLE": "Online Image BBox Overlay & Measure",
        "DESCRIPTION": "Use our free online tools to annotate images with bounding boxes for machine learning, computer vision, and design projects.",
        "KEYWORDS": "bounding box, bbox, marker, overlay, image, online, tool, image annotation, online tools"
    },
    "polygon.html": {
        "TITLE": "Online Image Polygon Overlay & Measure",
        "DESCRIPTION": "Use our free online tools to annotate images with polygons for machine learning, computer vision, and design projects.",
        "KEYWORDS": "polygon, marker, overlay, image, online, tool, image annotation, online tools"
    }
}

def get_seo_tags(cfg):
    with open("includes/seo.html", 'r') as tag_file:
        tag_content = tag_file.read()
        for key, value in cfg.items():
            tag_content = tag_content.replace(f"{{{{{key}}}}}", value)
        return tag_content

def template_fill(src_file, dest_file, page):
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

    cfg = SEO.get(page)
    if cfg:
        cfg['PAGE'] = page
        content = content.replace("{{SEO_TAG}}", get_seo_tags(cfg))


    # Write the filled content to the destination file
    with open(dest_file, 'w') as f:
        f.write(content)

def main():
    SRC_DIR = "src"
    DESC_DIR = "docs"
    for fn in os.listdir(SRC_DIR):
        template_fill(os.path.join(SRC_DIR, fn), os.path.join(DESC_DIR, fn), fn)


if __name__ == '__main__':
    main()