# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs

from scrapy.exceptions import DropItem


class PaperSpiderPipeline(object):
    def process_item(self, item, spider):
        return item


class JacsDuplicatesPipeline(PaperSpiderPipeline):
    """
    Pipline class for filtering invalid items.
    """
    def __init__(self):
        """
        Constructor.
        """
        super(self.__class__, self).__init__()

    def process_item(self, item, spider):
        if not item["abstract"]:
            raise DropItem("Duplicate item found: {}".format(item))
        else:
            return item


class JacsTextWriterPipeline(PaperSpiderPipeline):
    """
    Pipline class for writing item content to text.
    """
    def __init__(self):
        """
        Constructor.
        """
        super(self.__class__, self).__init__()
        self.__filename = "jasc.txt"

    def process_item(self, item, spider):

        # Check validity.
        if not item["abstract"]:
            raise DropItem("Duplicate item found: {}".format(item))

        # Get content of an item.
        content = u"="*50 + u"\n"
        title_string = u"Title: \n" + item["title"] + u"\n"
        abstract_string = u"Abstract: \n" + item["abstract"] + u"\n"
        content += (title_string + abstract_string)

        # Write item content to file.
        with codecs.open(self.__filename, "ab", encoding="utf-8") as f:
            f.write(content)
        
        return item

