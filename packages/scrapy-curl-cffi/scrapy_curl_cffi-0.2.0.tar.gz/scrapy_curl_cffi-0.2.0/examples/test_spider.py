from scrapy import Request, Spider


class TestSpider(Spider):
    name = "test"

    async def start(self):
        yield Request("https://httpbin.org/get", meta={"bindaddress": "192.168.1.131"})

    def parse(self, response):
        yield {
            "url": response.url,
            "data": response.json(),
            "meta": response.meta,
            "ip_address": response.ip_address,
        }
