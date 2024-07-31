from os import makedirs, path, remove
import urllib.error
from PIL import Image

import urllib.request


class ProviderBase:
    def __init__(self) -> None:
        pass

    def search(self, query: str):
        pass

    def crawl_chapters(self, html_url: str):
        pass

    def download_chapter(self, html_url: str, folder: str, need_optimize: bool = False):
        pass

    def convert_webp_to_jpg(self, pic_dict: dict):
        pic_folder = pic_dict.get("folder")
        pic_name = pic_dict.get("name")
        im = Image.open(pic_dict.get("path")).convert("RGB")
        im.save(f"{pic_folder}/{pic_name}.jpg", "jpeg")
        remove(pic_dict.get("path"))
        return {**pic_dict, "path": f"{pic_folder}/{pic_name}.jpg"}

    def optimize_lossless_jpeg(self, pic_dict: dict):
        pic_folder = pic_dict.get("folder")
        pic_name = pic_dict.get("name")
        im = Image.open(pic_dict.get("path")).convert("RGB")
        remove(pic_dict.get("path"))
        im.save(f"{pic_folder}/{pic_name}.jpg", "jpeg", quality=90, optimize=True)
        return {**pic_dict, "path": f"{pic_folder}/{pic_name}.jpg"}

    def download(self, pic_url: str, folder: str, new_name: str = None):
        folder = f"downloaded/{folder}"
        status = "processing"
        pic_lts = pic_url.split("/")
        pic_name_with_ext = pic_lts[-1]
        pic_name_with_ext_lts = pic_name_with_ext.split(".")

        # Data
        pic_name = new_name if new_name else pic_name_with_ext_lts[0]
        pic_ext = pic_name_with_ext_lts[1]

        # Store name
        new_name = f"{pic_name}.{pic_ext}"

        if not path.isdir(folder):
            makedirs(folder)

        if path.isfile(f"{folder}/{new_name}") or path.isfile(
            f"{folder}/{pic_name}.jpg"
        ):
            status = "existed"
            if path.isfile(f"{folder}/{pic_name}.jpg"):
                new_name = f"{pic_name}.jpg"
                pic_ext = "jpg"
            return {
                "status": status,
                "path": f"{folder}/{new_name}",
                "folder": folder,
                "name": pic_name,
                "ext": pic_ext,
            }

        opener = urllib.request.build_opener()
        opener.addheaders = [("User-Agent", "Chrome")]
        urllib.request.install_opener(opener)

        for _ in range(3):
            try:
                urllib.request.urlretrieve(pic_url, f"{folder}/{new_name}")
                status = "created"
                break
            except Exception as e:
                if isinstance(e, urllib.error.URLError):
                    status = "error"
                    print("⛓️‍💥 Broken link...!")
                    break
                if e.code == 522:
                    print("⛔️ Retrying...")
                    continue

        return {
            "status": status,
            "path": f"{folder}/{new_name}",
            "folder": folder,
            "name": pic_name,
            "ext": pic_ext,
        }
