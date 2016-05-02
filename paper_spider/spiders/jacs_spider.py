# -*- coding: utf-8 -*-

from scrapy import Request
from scrapy.spider import Spider
from scrapy.selector import Selector

from paper_spider.items import JacsSpiderItem


class JacsSpider(Spider):
    # Spider name.
    name = "jacs"

    # Xpath queries.
    xpath_queries = {
        "title": "//span[@class='hlFld-Title']/text()",
        "url": "//div[@class='hlFld-Title']/h2/div/a[2]/@href",
        "abstract": "//p[@class='articleBody_abstractText']/text()"
    }

    def __init__(self):
        """
        JACS Spider constructor.
        """
        super(self.__class__, self).__init__()
        self.allowed_domains = ["pubs.acs.org"]
        self.start_urls = ["http://pubs.acs.org/toc/jacsat/138/16#Articles"]

        # Base domain for getting full url.
        self.__base_domain = unicode("http://pubs.acs.org")

    def parse(self, response):
        sel = Selector(response)

        # Loop to get requests for article urls.
        for url in  sel.xpath(self.xpath_queries["url"]):
            full_url = self.__base_domain + url.extract()
            yield Request(full_url, callback=self.parse_abstract)

    def parse_abstract(self, response):
        """
        Call back function for article requests.
        """
        sel = Selector(response)

        # JACS spider item.
        item = JacsSpiderItem()

        # Get abstract.
        abs_selectors = sel.xpath(self.xpath_queries["abstract"])
        abstract = unicode("")
        for abs_selector in abs_selectors:
            abstract += abs_selector.extract()
        item["abstract"] = abstract

        # Get title.
        title_selector = sel.xpath(self.xpath_queries["title"])
        item["title"] = title_selector[0].extract()

        return item

