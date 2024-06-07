from typing import Any
import scrapy

class DesktopbgSpider(scrapy.Spider):
    name = "desktopbg_spider"
    start_urls = []

    def __init__(self, name: str | None = None, **kwargs: Any):
        for i in range(20):
            self.start_urls.append(
                f"https://desktop.bg/computers-all?page={i}")

        super().__init__(name, **kwargs)

    def parse(self, response):
        self.logger.info("Accessing product list")
        products = response.css('ul.products > li article')
        self.logger.info(f"Found {len(products)} products")
        for product in products:
            details_url = product.css('a::attr(href)').get()
            self.logger.info(f"Product URL: {details_url}")
            if details_url:
                yield response.follow(details_url, self.parse_product)

    def parse_product(self, response):
        self.logger.info(f"Parsing product page: {response.url}")
        motherboard = response.xpath(
            '/html/body/div[2]/article/section[2]/table/tbody/tr[6]/td').get()
        processor = response.xpath(
            '/html/body/div[2]/article/section[2]/table/tbody/tr[7]/td').get()
        video_card = response.xpath(
            '/html/body/div[2]/article/section[2]/table/tbody/tr[8]/td').get()
        ram = response.xpath(
            '/html/body/div[2]/article/section[2]/table/tbody/tr[9]/td/div[1]/label/span[1]'
        ).get()

        yield {
            'url': response.url,
            'motherboard': motherboard.replace("<td>\n", "").replace("\n</td>", ""),
            'processor': processor.replace("<td>\n", "").replace("\n</td>", ""),
            'video_card': video_card.replace("<td>\n", "").replace("\n</td>", ""),
            'ram': ram.replace("<td>\n", "").replace("\n</td>", "").replace('<span>\n', '').replace('\n</span>', '')
        }
