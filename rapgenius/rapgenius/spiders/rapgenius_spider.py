from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from rapgenius.items import RapGeniusItem
from scrapy.http.request import Request
import re


def count_matches(string):
    count = 0
    for m in re.finditer('</em>', string):
        count += 1
    return count

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
        self.lyric_length = len(lyric.split(" "))
        lyric.replace(" ", "+")  
        self.start_urls = ["http://rapgenius.com/search?q=%s" % lyric]
        self.base_url = "http://rapgenius.com"

    def parse_song(self, response):
        print "*****in parse_song******"
        item = response.meta['item']
        sel = Selector(response)
        lyrics = sel.css("//div[@class='lyrics'")
        print lyrics
        return item

    def parse(self, response):
        sel = Selector(response)
        results = sel.xpath("//ul/li[@class='search_result']")
        item = RapGeniusItem()
        items = []

        for result in results:
            title = result.xpath("a/span[@class='title_with_artists']").extract()
            info = remove_html_tags(title[0]).split(u' \u2013 ')
            matches = result.xpath("p").extract()
            print result.xpath("p").extract()
            url = result.xpath("a/@href").extract()
            item['url'] = self.base_url + url[0]
            item['artist'] = info[0].split('\n    ')[1]            # This is hacky!
            item['song_name'] = info[1].splitlines()[0]
            request = Request(item['url'], callback='self.parse_song')
            request.meta['item'] = item
            yield request
        #     items.append(item)
        # print items










