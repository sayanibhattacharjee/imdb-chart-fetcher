import sys
import json
import requests
from bs4 import BeautifulSoup
import pandas

class Scrapper():
    def __init__(self) -> None:
        
        self.header = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'Accept-Language':'en-GB,en-US;q=0.9,en;q=0.8',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'})

    def parse(self, chart_url, item_count):        

        response = requests.get(chart_url, headers=self.header)
        res = BeautifulSoup(response.content, features='lxml')
        movie_list = res.find("tbody", class_="lister-list")
        url_list = movie_list.find_all('tr')
        
        self.check_for_count(url_list, item_count)

    
    def check_for_count(self, url_list, item_count):
        
        dataframe = pandas.DataFrame(columns= ['index', 'url'])
        for i, elem in enumerate(url_list):
                if(i < int(item_count)):
                    wrapper= elem.find("td", class_="titleColumn")
                    tag = wrapper.find("a",  href=True)
                    link = tag['href']
                    dataframe = dataframe.append({'index': i, 'url': 'https://www.imdb.com/' + str(link)}, ignore_index=True) # ignore_indexbool, default False
        # with open("./url_list/moview_list.csv","r") as fp:
        #     pass

        dataframe.to_csv('./url_list/movie_list.csv', index=False)


    def extractDetails(self):
        
        result = []
        dataframe = pandas.read_csv('./url_list/movie_list.csv')
        all_urls = dataframe['url']

        item = {}
        for i, url in enumerate(all_urls):
            page = requests.get(url, headers=self.header)
            soup = BeautifulSoup(page.content, features='lxml')

            item['title'], title_year, title_wrapper = self.get_title(soup) 
            item['year'] = self.get_movie_release_year(soup, title_year)
            item['rating'] = self.get_rating(soup)
            item['summary'] = self.get_summary(soup)
            item['duration'] = self.get_duration(title_wrapper)
            item['genre'] = self.get_genre(title_wrapper)

            result.append(item)

        result = json.dumps(result)
        return result


    def get_title(self, soup):
        
        title_wrapper = soup.find("div", class_="title_wrapper")
        title_year = title_wrapper.find("h1").text.strip()
        title = title_year.split('(')[0].strip()
        return title, title_year, title_wrapper

    def get_movie_release_year(self, soup, title_year):
    
        year = title_year.split('(')[1][:-1]
        return year

    def get_rating(self, soup):
        
        imdb_rating = soup.find("span", itemprop="ratingValue").text.strip()
        return imdb_rating

    def get_summary(self, soup):
        
        summary = soup.find("div", class_="summary_text").text.strip()
        return summary

    def get_duration(self, title_wrapper):
        
        sub_text = title_wrapper.find("div", class_="subtext")
        duration = sub_text.find("time").text.strip()
        return duration

    def get_genre(self, title_wrapper):
        
        sub_text = title_wrapper.find("div", class_="subtext")
        genre_tags = sub_text.find_all("a", text=True)
        genre = ""
        for genre_tag in genre_tags[:-1]:
            genre += genre_tag.text.strip() + ' '
        genre = genre.rstrip()      
        genre = genre.replace(" ", ", ")    
        return genre
        

if __name__ == "__main__":
    chart_url = sys.argv[1]
    items_count = sys.argv[2]

    s = Scrapper()
    try:
        scrapper = s.parse(chart_url, items_count)
    except:
        raise Exception("Failed to get movie URLs")
    try:
        result = s.extractDetails()
        print("result", result)
    except:    
        raise Exception("Failed to extract movie deatils")
