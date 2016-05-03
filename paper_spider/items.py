# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item
from scrapy import Field


class PaperSpiderItem(Item):
    """
    A base item class for other drived item classes.
    """
    title = Field()
    url = Field()
    authors = Field()
    citation = Field()
    pub_date = Field()
    doi = Field()
    abstract = Field()


class JacsSpiderItem(PaperSpiderItem):
    """
    Item class for JACS article.
    """
    def __init__(self):
        super(self.__class__, self).__init__()
