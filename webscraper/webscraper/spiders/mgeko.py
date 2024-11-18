import scrapy
import re
from webscraper.items import MangaItem


class MgekoSpider(scrapy.Spider):
    name = "mgeko"
    allowed_domains = ["mgeko.cc"]
    start_urls = ["https://www.mgeko.cc/jumbo/manga/"]
    
    # CSS selectors
    manga_selector = 'li[class="novel-item"]'
    cover_art_selector = "img.lazy::attr(data-src)"
    title_selector = "h4::text"
    latest_chapter_selector = "h5::text"
    url_selector = "a.list-body::attr(href)"
    next_page_selector = (
        "a.mg-pagination-chev:has(i.fa-chevron-right)::attr(href)"
    )
    
    # Regular expression patterns
    # Extract any non-alphanumeric character
    alphanum_pattern = re.compile(r'[^a-zA-Z0-9\s]')
    # Extract any number, optionally followed by a hyphen, then another number
    latest_chapter_pattern = re.compile(r"(\d+)(?:-(\d+))?")

    def parse(self, response):
        mangas = response.css(self.manga_selector)

        for manga in mangas:
            manga_item = MangaItem()
            
            # Parse cover art
            manga_item["cover_art"] = manga.css(self.cover_art_selector).get()
            
            # Parse title
            title = manga.css(self.title_selector).get()
            title = title.strip()
            manga_item["title"] = self.alphanum_pattern.sub("", title)

            # Parse latest chapter
            latest_chapter = manga.css(self.latest_chapter_selector).get()
            latest_chapter = latest_chapter.strip()
            match = self.latest_chapter_pattern.search(latest_chapter)
            if match:
                chapter_number = match.group(1)
                if match.group(2):
                    chapter_number += f".{match.group(2)}"
                manga_item["latest_chapter"] = float(chapter_number)
            else:
                manga_item["latest_chapter"] = 0.0

            # Parse url
            url = manga.css(self.url_selector).get()
            if not url.startswith("https://www.mgeko.cc"):
                url = f"https://www.mgeko.cc{url}"
            manga_item["url"] = url
            
            manga_item["source"] = "mgeko"

            yield manga_item

        # Pagination
        next_page = response.css(self.next_page_selector).get()
        if next_page and "javascript:void(0)" not in next_page:
            yield response.follow(next_page, self.parse)
