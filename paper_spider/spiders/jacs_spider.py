# -*- coding: utf-8 -*-

import os
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
        "abstract": "//p[@class='articleBody_abstractText']/text()",
        "author": "//a[@id='authors']/text()",
        "citation": "//div[@id='citation']/*/text() | //div[@id='citation']/text()",
        "doi": "//div[@id='doi']/text()",
        "pub_date": "//div[@id='pubDate']/text()",
    }

    def __init__(self):
        """
        JACS Spider constructor.
        """
        super(self.__class__, self).__init__()
        self.allowed_domains = ["pubs.acs.org"]

        # Get start urls.
        self.__get_start_urls()

        # Base domain for getting full url.
        self.__base_domain = unicode("http://pubs.acs.org")

    def __get_start_url(self, volume, issue):
        """
        Private helper function to get full url from volumn and issue number.
        """
        return (u"http://pubs.acs.org/toc/jacsat/" +
                unicode(volume) + u"/" + unicode(issue))

    def __get_start_urls(self, filename="./jacs_input.txt"):
        """
        Private helper function to get start url for spider.
        """
        # Check file existance.
        if os.path.exists(filename):
            glob, loc = {}, {}
            execfile(filename, glob, loc)
            if "volume_issue" not in loc:
                msg = "'volume_issue' is not supplied in {}.".format(filename)
                raise ValueError(msg)
        else:
            raise IOError("{} is not found.".format(filename))

        # Check data validity.
        if not loc["volume_issue"]:
            raise ValueError("No volume and issue data.")

        # Collect start urls.
        self.start_urls = []
        for volume, issue in loc["volume_issue"]:
            start_url = self.__get_start_url(volume, issue)
            self.start_urls.append(start_url)

    def parse(self, response):
        sel = Selector(response)

        # Loop to get requests for article urls.
        for url in  sel.xpath(self.xpath_queries["url"]):
            full_url = self.__base_domain + url.extract()
            yield Request(full_url, callback=self.parse_article)

    def parse_article(self, response):
        """
        Call back function for article requests.
        """
        sel = Selector(response)

        # JACS spider item.
        item = JacsSpiderItem()

        # Get title.
        title_selector = sel.xpath(self.xpath_queries["title"])
        item["title"] = title_selector[0].extract()

        # Get authors.
        author_selectors = sel.xpath(self.xpath_queries["author"])
        author_names = [author_selector.extract()
                        for author_selector in author_selectors]
        authors = u", ".join(author_names)
        item["authors"] = authors

        # Get url.
        item["url"] = response.url

        # DOI number.
        dois = sel.xpath(self.xpath_queries["doi"]).extract()
        item["doi"] = dois[0] if dois else u""

        # Get citation.
        citation_strings = sel.xpath(self.xpath_queries["citation"]).extract()
        citation = u"".join(citation_strings)
        item["citation"] = citation

        # Publication date.
        pub_dates = sel.xpath(self.xpath_queries["pub_date"]).extract()
        if pub_dates:
            item["pub_date"] = pub_dates[0].split(u":")[1].strip()
        else:
            item["pub_date"] = u""

        # Get abstract.
        abs_selectors = sel.xpath(self.xpath_queries["abstract"])
        abstract = unicode("")
        for abs_selector in abs_selectors:
            abstract += abs_selector.extract()
        item["abstract"] = abstract

        return item


