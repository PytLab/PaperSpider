# *PaperSpider*
A Python Web Crawler for Paper data crawling powered by [Scrapy](http://scrapy.org/).

***PaperSpider***是一个用于抓取期刊文章相关信息的爬虫程序，基于[Scrapy](http://scrapy.org)框架编写。

目前支持的期刊:
- [JACS](http://pubs.acs.org/journal/jacsat)

### 安装python以及scrapy

- **安装python**

    本程序基于python2.7编写, 可以从 http://python.org/download/ 上安装Python 2.7

- **安装scrapy框架**
    ```
    $ pip install scrapy
    ```
    具体不同平台安装scrapy框架的方法, 详见: [安装指南](http://scrapy-chs.readthedocs.io/zh_CN/latest/intro/install.html)

### 使用方法(以爬去JACS文章信息为例)

1. 输入文件
    在`/paper_spider`下的`jacs_input.txt`中填入将要爬取的卷号和期刊号。

    例如，要爬取卷号为138，期刊号为16 和 卷号为137，期刊号为13的所有文章信息（标题，发表日期，作者，摘要等），如下格式填写输入文件：

    ``` python
    # Volume number, issue number
    volume_issue = [(138, 16), (137, 13)]
    ```

2. 开始爬取

   在项目的根目录`/paper_spider`执行
   ``` shell
   $ scrapy crawl jacs
   ```

   爬取结果会自动保存在`jacs.txt`中。

   ![](https://github.com/PytLab/PaperSpider/blob/master/assets/jacs_txt.png)

   若想要以不同的格式保存数据：
   ``` shell
   $ scrapy crawl jacs -o jacs.json -t json  # 以json格式保存
   ```
   ``` shell
   $ scrapy crawl jacs -o jacs.csv -t csv  # 以csv格式保存
   ```
   具体的保存方式详见[Feed exports](http://scrapy-chs.readthedocs.io/zh_CN/latest/topics/feed-exports.html)

\*本爬虫目前还不支持保存到数据库，后续会加入对MySQL、MongoDB的支持。
