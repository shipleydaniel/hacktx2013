from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from rapgenius.items import RapGeniusItem
import re


def count_matches(string):
    count = 0
    for m in re.finditer('</em>', string):
        count += 1
    print count

def remove_html_tags(string):
    formatted = ""
    tag = False
    for char in string:
        if char == '<':
            tag = True
        if not tag:
            formatted += char
        if char == '>':
            tag = False
    return formatted

class RapGeniusSpider(BaseSpider):
    name = "rapgenius"
    allowed_domains = ["rapgenius.com"]
    start_urls = [
        "http://rapgenius.com/search?q=",
    ]
    lyric_length = 0

    def __init__(self, lyric=None, *args, **kwargs):
        super(RapGeniusSpider, self).__init__(*args, **kwargs)
        self.start_urls = ["http://rapgenius.com/search?q=%s" % lyric]

    def parse(self, response):
        sel = Selector(response)
        results = sel.xpath("//ul/li[@class='search_result']")
        for result in results:
            item = RapGeniusItem()
            matches = result.xpath("p").extract()
            count = 0
            for match in matches:
                count_matches(match)

            # title = result.xpath("a/span[@class='title_with_artists']").extract()
            # info = remove_html_tags(title[0]).split(u' \u2013 ')
            # item['artist'] = info[0].split('\n    ')[1]            # This is hacky!
            # item['song_name'] = info[1].splitlines()[0]
            # print item






