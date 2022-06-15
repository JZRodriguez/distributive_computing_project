import scrapy


class ToScrapeCSSSpider(scrapy.Spider):
    name = "gpus-spider"
    start_urls = [
        'https://www.amazon.com.mx/s?k=NVIDIA+RTX+3060',
    ]

    def parse(self, response):
        counter = 0
        for item in response.css("div.s-result-item.s-asin"):
            yield {
                'title': item.xpath(".//h2/a/span/text()").extract_first(),
                'price': float(item.xpath(".//span[@class='a-price']//text()").extract_first().replace(',', '')[1:]),
                'link': item.css("a.a-link-normal::attr(href)").extract_first(),
                'iteration': counter
            }
            counter += 1

        next_page_url = response.xpath("//a[@class='s-pagination-next']").extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))
