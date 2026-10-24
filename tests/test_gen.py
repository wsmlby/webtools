import os
from pathlib import Path
import shutil
import tempfile
import unittest
import xml.etree.ElementTree as ET

import gen


ROOT = Path(__file__).resolve().parents[1]


class GeneratorTests(unittest.TestCase):
    def test_generation_in_standalone_checkout(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ("src", "includes"):
                shutil.copytree(ROOT / name, root / name)
            shutil.copytree(ROOT / "docs" / "_includes", root / "docs" / "_includes")
            previous_directory = Path.cwd()
            try:
                os.chdir(root)
                gen.main()
            finally:
                os.chdir(previous_directory)

            for template in (root / "src").glob("*.html"):
                with self.subTest(page=template.name):
                    page = (root / "docs" / template.name).read_text()
                    self.assertNotIn("{{", page)
                    self.assertIn('href="qr-camera.html"', page)

            camera_page = (root / "docs" / "qr-camera.html").read_text()
            self.assertIn("<title>Camera QR Code Scanner</title>", camera_page)
            self.assertIn('src="statics/camera-qr.js"', camera_page)
            self.assertIn('playsinline', camera_page)
            self.assertIn('width=device-width, initial-scale=1.0', camera_page)
            sitemap = ET.parse(root / "docs" / "sitemap.xml")
            locations = {
                element.text
                for element in sitemap.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
            }
            self.assertIn(gen.BASE_PATH + "qr-camera.html", locations)
            for template in (root / "src").glob("*.html"):
                self.assertIn(gen.BASE_PATH + template.name, locations)

    def test_scanner_assets_exist_without_a_build_step(self):
        static = ROOT / "docs" / "statics"
        for filename in (
            "camera-qr.js",
            "qr-scanner-1.4.2/qr-scanner.min.js",
            "qr-scanner-1.4.2/qr-scanner-worker.min.js",
            "qr-scanner-1.4.2/LICENSE",
        ):
            with self.subTest(asset=filename):
                self.assertTrue((static / filename).is_file())
                self.assertGreater((static / filename).stat().st_size, 0)


if __name__ == "__main__":
    unittest.main()
