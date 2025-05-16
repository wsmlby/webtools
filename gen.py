import datetime
import os
TAGS = {
    "{{GA_TAG}}": "docs/_includes/head-custom-google-analytics.html",
    "{{SIDEBAR_STYLE}}": "includes/sidebar_style.html",
    "{{SIDEBAR_HTML}}":"includes/sidebar.html",
    "{{INCONTENT_ADS}}": "includes/content_ads.html",
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
    },
    "epoch.html": {
         "TITLE":"Epoch Conversion Online Tools",
          "DESCRIPTION" : 'Use our online tools to convert timestamps into local and UTC time formats', 
          "KEYWORDS": 'epoch converter, epoch utc, epoch time, epoch time converter, timestamp conversion',
    },
    "qrcode.html": {   # QR Code Generator Online Tools Section... (Complete) "qrcodegen-online" and more..",    },
        "TITLE":"OpenCV WeChat QRCode Reader",
        "DESCRIPTION" : 'Use our online tools to read QR code from entire image or a crop of it',
        "KEYWORDS": 'qrcode, qr code, qrcode reader, qr reader, qr read, opencv qrcode, opencv qrcode reader wechat'
    },
    "grid.html": {
        "TITLE":"Grid scratchpad",
        "DESCRIPTION" : 'Use our free online tools to get a grid scratchpad for drawing, sketching, and design projects.',
        "KEYWORDS": 'grid, online, tool, scratchpad'
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

BASE_PATH = "https://wsmlby.github.io/webtools/"
def create_sitemap(src_fn, dst_fn, sitemap):
    maps = []
    TIME = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S+00:00')
    for k in sitemap:
         URL = BASE_PATH + k
         maps.append(f"""<url>
  <loc>{URL}</loc>
  <lastmod>{TIME}</lastmod>
  <priority>1.00</priority>
</url>""")
    
    with open (dst_fn,'w') as f:   # write to the file specified by dst_filepath name in destination directory with same names of source files.
        with open(src_fn,'r') as src:
            content = src.read()
            content = content.replace("{{SITEMAP_LINKS}}", "\n".join(maps))
            f.write(content)


def main():
    SRC_DIR = "src"
    DESC_DIR = "docs"
    sitemap = set(["", "privacy-policy.html"])
    for fn in os.listdir(SRC_DIR):
        if fn.endswith("sitemap.xml"):
            continue
        template_fill(os.path.join(SRC_DIR, fn), os.path.join(DESC_DIR, fn), fn)
        if fn.endswith(".html"):
            sitemap.add(fn)
    create_sitemap(os.path.join(SRC_DIR, "sitemap.xml"), os.path.join("../wsmlby.github.io/", "sitemap.xml"), sitemap)



if __name__ == '__main__':
    main()