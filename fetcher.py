# from flask import Flask
import sys
import json
# from scrapy import Spider
from scrapy.selector import Selector
from scrapy.http.request import Request
import requests
from bs4 import BeautifulSoup
from fields import ImdbItem


item = {}


def parse(base_url):

    print("parsing")    
    
    header = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'Accept-Language':'en-GB,en-US;q=0.9,en;q=0.8',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'})

    response = requests.get(base_url, headers=header)
    res = BeautifulSoup(response.content, features='lxml')
    movie_list = res.find("tbody", class_="lister-list")
    url_list = movie_list.find_all('tr')

    print("url_list", url_list)
    
    print("item", item)
    

def parse_movie(response):
    
    sel = Selector(response)
    
    item['title'] = get_title(sel) 
    item['duration'] = get_duration(sel)
    item['genre'] = get_genre(sel)
    item['year'] = get_movie_release_year(sel)
    item['rating'] = get_rating(sel)
    item['summary'] = get_summary(sel)
    
    return item

def get_title(self, selector):
    
    title = selector.xpath('//h1[@class="header"]/span[@itemprop ="name"]/text()').extract()[0]
    
    return self.trim(title)

def get_movie_release_year(self, selector):
    
    year = selector.xpath('//h1[@class="header"]/span/a/text()').extract()[0]
    # To-do
    return self.trim(year)

def get_rating(self, selector):
    
    rating = selector.xpath('//span[@itemprop="ratingValue"]/text()').extract()[0]

    return float(self.trim(rating))

def get_summary(self, selector):
    
    summary = selector.xpath('//td[@id="overview-top"]/p[@itemprop="description"]/text()').extract()[0]
    
    return self.trim(summary)

def get_duration(self, selector):
    
    duration = selector.xpath('//time[@itemprop="duration"]/text()').extract()[0]

    return int(self.trim(duration).split()[0])

def get_genre(self, selector):
    
    genre = selector.xpath('//span[@itemprop="genre"]/text()').extract()

    return self.trim_list(genre)

def trim(self, raw_str):
        
        return raw_str.encode('ascii', errors='ignore').strip()

def trim_list(self, raw_list):
       
        return [self.trim(raw_str) for raw_str in raw_list]


if __name__ == "__main__":
    # chart_url = sys.argv[1]
    # items_count = sys.argv[2]

    print("hi")
    base_url = 'https://www.imdb.com/india/top-rated-indian-movies'
    scrapper =  parse(base_url)
    
