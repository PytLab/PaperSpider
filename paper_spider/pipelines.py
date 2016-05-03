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
        content = u"\n" + u"="*50 + u"\n"
        split_line = u"-"*30 + u"\n"

        title_string = u"Title: " + item["title"] + u"\n"
        authors_string = u"Authors: \n" + item["authors"] + u"\n"
        citation_string = u"Citation: " + item["citation"] + u"\n"
        url_string = u"URL: " + item["url"] + u"\n"
        doi_string = u"DOI: " + item["doi"] + u"\n"
        pub_date_string = u"Publication Date: " + item["pub_date"] + u"\n"
        abstract_string = u"Abstract: \n" + item["abstract"] + u"\n"

        content += split_line.join([title_string,
                                    authors_string,
                                    citation_string,
                                    url_string,
                                    doi_string,
                                    pub_date_string,
                                    abstract_string])

        # Write item content to file.
        with codecs.open(self.__filename, "ab", encoding="utf-8") as f:
            f.write(content)
        
        return item

