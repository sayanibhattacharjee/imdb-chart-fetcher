from scrapy import Spider
from scrapy.selector import Selector
from scrapy.http.request import Request
import requests

from fields import ImdbItem

class ImdbSpider(Spider):

    def __init__(self, base_url):
        self.base_url = base_url
        # self.self.item_count = self.item_count
       
        self.protocol = "http"
        self.base_url = "www.imdb.com"
        self.header = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'Accept-Language':'en-GB,en-US;q=0.9,en;q=0.8',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'})
        self.item = ImdbItem()


    def parse(self):
        
        print("parsing")
        
        response = requests.get(self.base_url, headers=self.header)
        sel = Selector(response)

        
        url_list = sel.xpath('//tbody[@class="lister-list"]/tr\
                /td[@class="titleColumn"]/a/@href').extract()
        
        movies = []
        for url in url_list:
            movies.append(self.protocol + "://" + self.base_url + url)

        print("movies url", movies)

        for movie in movies:
            yield Request(movie, callback=self.parse_movie)
        
        print("self.item", self.item)
        return self.item

    
    def parse_movie(self, response):
        
        sel = Selector(response)
        
        self.item['title'] = self.get_title(sel) 
        self.item['duration'] = self.get_duration(sel)
        self.item['genre'] = self.get_genre(sel)
        self.item['year'] = self.get_movie_release_year(sel)
        self.item['rating'] = self.get_rating(sel)
        self.item['summary'] = self.get_summary(sel)
        
        return self.item

    def get_title(self, selector):
        
        title = selector.xpath('//h1[@class="header"]/span[@self.itemprop ="name"]/text()').extract()[0]
        
        return self.trim(title)
    
    def get_movie_release_year(self, selector):
        
        year = selector.xpath('//h1[@class="header"]/span/a/text()').extract()[0]
        # To-do
        return self.trim(year)
    
    def get_rating(self, selector):
        
        rating = selector.xpath('//span[@self.itemprop="ratingValue"]/text()').extract()[0]

        return float(self.trim(rating))

    def get_summary(self, selector):
        
        summary = selector.xpath('//td[@id="overview-top"]/p[@self.itemprop="description"]/text()').extract()[0]
        
        return self.trim(summary)
    
    def get_duration(self, selector):
        
        duration = selector.xpath('//time[@self.itemprop="duration"]/text()').extract()[0]

        return int(self.trim(duration).split()[0])
    
    def get_genre(self, selector):
       
        genre = selector.xpath('//span[@self.itemprop="genre"]/text()').extract()

        return self.trim_list(genre)


