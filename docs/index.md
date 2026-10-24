# Welcome to my Web Tools for Engineers

This is a collection of tools and resources for engineers to enhance productivity and streamline workflows.


## Image Tools

1. [Bounding Box Annotation](/bbox.html)
2. [Polygon Annotation](/polygon.html)
3. [Camera QR Code Scanner](/webtools/qr-camera.html)

## Time Tools

1. [Epoch Converter Online Tool (UTC to Local and vice versa)](/epoch.html)

## Privacy Policy
You can find our privacy policy [here.](/privacy-policy.md)

## Local development

Edit page templates in `src/` and shared navigation in `includes/`, then run
`python gen.py` to rebuild `docs/` and `docs/sitemap.xml`. Static JavaScript
dependencies live in `docs/statics/` and are served unchanged.

Preview with `python -m http.server 8000 --directory docs` and open
`http://localhost:8000/qr-camera.html`. Camera access requires HTTPS in production;
localhost is allowed for development.

Run generator checks with `python -m unittest discover -s tests`.
