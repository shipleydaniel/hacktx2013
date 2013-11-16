# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class RapGeniusItem(Item):
    # define the fields for your item here like:
    song_name = Field()
    artist = Field()
    lyric = Field()
    url = Field()
    match_percentage = Field()

