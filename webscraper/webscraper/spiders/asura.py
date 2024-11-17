import scrapy
import re
from webscraper.items import MangaItem
from scrapy_playwright.page import PageMethod


class AsuraSpider(scrapy.Spider):
    name = "asura"
    allowed_domains = ["asuracomic.net"]
    start_urls = ["https://asuracomic.net"]
    
    # CSS selectors
    manga_selector = (
        "div.w-full.p-1.pt-1.pb-3.border-b-\\[1px\\].border-b-\\[\\#312f40\\]"
    )
    cover_art_selector = "img::attr(src)"
    latest_chapter_selector = "div.flex.gap-1 p::text"
    url_selector = (
        "span.text-\\[15px\\].font-medium.hover\\:text-themecolor.hover\\:cursor-pointer a::attr(href)"
    )
    next_page_selector = (
        "a.flex.items-center.bg-themecolor.text-white.px-8.py-1\\.5.rounded-\\[2px\\].text-\\[13px\\].w-\\[110px\\].text-center::attr(href)"
    )
    
    # Regular expression patterns
    # For /series/Title-of-Manga-xxxxx, extract Title-of-Manga
    title_pattern = re.compile(r"/series/(.+)-[^/]+$")
    # Extract any floating point number
    latest_chapter_pattern = re.compile(r"\d+(\.\d+)?")

    def parse(self, response):
        mangas = response.css(self.manga_selector)

        for manga in mangas:
            manga_item = MangaItem()

            # Parse cover art
            manga_item["cover_art"] = manga.css(self.cover_art_selector).get()

            # Parse title
            url = manga.css(self.url_selector).get()
            match = self.title_pattern.search(url)
            if match:
                title = match.group(1).replace("-", " ").title()
                manga_item["title"] = title
            else:
                manga_item["title"] = "Unknown"

            # Parse latest chapter
            latest_chapter = manga.css(self.latest_chapter_selector).get()
            match = self.latest_chapter_pattern.search(latest_chapter)
            if match:
                manga_item["latest_chapter"] = float(match.group())
            else:
                manga_item["latest_chapter"] = 0.0

            # Parse url
            if not url.startswith("https://asuracomic.net"):
                url = f"https://asuracomic.net{url}"
            manga_item["url"] = url
            
            yield manga_item
        
        # Pagination
        next_page = response.css(self.next_page_selector).get()
        if next_page:
            if not next_page.startswith("https://asuracomic.net"):
                next_page = f"https://asuracomic.net{next_page}"
            yield scrapy.Request(next_page, meta=dict(
                playwright = True,
                playwright_page_methods = [
                    PageMethod('wait_for_selector', self.manga_selector)
                ],
                handle_httpstatus_list = [500]
            ))
