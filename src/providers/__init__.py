from os import rename
import shutil
import typing
from src.core.provider_base import ProviderBase


class ProviderFactory:
    MODULES = {}

    def __init__(self, module_name: str) -> None:
        self.module: typing.Union[ProviderBase, None] = None
        if module_name in self.MODULES:
            self.module = self.MODULES[module_name]

        if not self.module:
            print(f"⛔️ Module {module_name} not found!")

    def download(self, query: str):
        response = self._search(query=query)
        chapters = self._crawl_chapters(response.get("html_url"))
        manga_name = response.get("title").lower().replace(" ", "_")
        chapter_response = []
        for chapter in chapters.get("data", []):
            title = chapter.get("title")
            chapter_response.append(
                self._download_chapter(chapter.get("html_url"), f"{manga_name}/{title}")
            )
        cbz_file = self._zip(manga_name)
        return {**response, "chapters": chapter_response, "cbz_file": cbz_file}

    def _zip(self, folder: str):
        shutil.make_archive(
            f"./downloaded/{folder}.cbz", "zip", f"./downloaded/{folder}"
        )
        rename(f"./downloaded/{folder}.cbz.zip", f"./downloaded/{folder}.cbz")
        return f"./downloaded/{folder}.cbz"

    def _search(self, query: str):
        return self.module.search(query)

    def _crawl_chapters(self, html_url: str):
        return self.module.crawl_chapters(html_url)

    def _download_chapter(
        self, html_url: str, folder: str, need_optimize: bool = False
    ):
        return self.module.download_chapter(html_url, folder, need_optimize)
