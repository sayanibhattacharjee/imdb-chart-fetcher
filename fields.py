from scrapy import Item
from scrapy.item import Field


class ImdbItem(Item):
    
    title = Field()
    duration = Field()
    genre = Field()
    year = Field()
    rating = Field()
    summary = Field()
    