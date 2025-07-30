# usage: scrapy runspider examples/heritage.py


from scrapy import Spider


class HeritageSpider(Spider):
    name = "heritage"
    # start_urls = ["https://www.ha.com"]
    start_urls = [
        # "https://fineart.ha.com/itm/prints-and-multiples/damien-hirst-b-1965-theodora-from-the-empresses-2022-laminated-giclee-print-in-colors-on-aluminum-composite-panel/a/16228-43162.s?ic4=GalleryView-Thumbnail-071515",
        "https://fineart.ha.com/itm/works-on-paper/damien-hirst-b-1965-spin-painting-2009-acrylic-on-wove-paper-20-1-2-inches-521-cm-diameter-sheet-stamped/a/16228-43163.s?ic4=GalleryView-Thumbnail-071515",
    ]
    curl_cffi_options = {"impersonate": "safari184_ios"}

    custom_settings = {
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_curl_cffi.handler.CurlCffiDownloadHandler",
            "https": "scrapy_curl_cffi.handler.CurlCffiDownloadHandler",
        },
        "DOWNLOADER_MIDDLEWARES": {
            "scrapy_curl_cffi.middlewares.CurlCffiMiddleware": 200,
            "scrapy_curl_cffi.middlewares.DefaultHeadersMiddleware": 400,
            "scrapy_curl_cffi.middlewares.UserAgentMiddleware": 500,
            "scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware": None,  # noqa: E501
            "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": None,
        },
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        # "HTTPERROR_ALLOW_ALL": True,
    }

    def parse(self, response):
        # breakpoint()
        yield {"title": response.css("title::text").get()}

        # urls = [
        #     "https://fineart.ha.com/itm/prints-and-multiples/damien-hirst-b-1965-theodora-from-the-empresses-2022-laminated-giclee-print-in-colors-on-aluminum-composite-panel/a/16228-43162.s?ic4=GalleryView-Thumbnail-071515",
        #     "https://fineart.ha.com/itm/works-on-paper/damien-hirst-b-1965-spin-painting-2009-acrylic-on-wove-paper-20-1-2-inches-521-cm-diameter-sheet-stamped/a/16228-43163.s?ic4=GalleryView-Thumbnail-071515",
        # ]
        # for url in urls:
        #     yield response.follow(url, callback=self.parse_item)

    def parse_item(self, response):
        yield {"title": response.css("title::text").get()}
