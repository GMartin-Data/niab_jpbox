import re

from loguru import logger
import scrapy

from jpbox.items import JpboxItem


BASE_URL = "https://www.jpbox-office.com/v9_hebdomadaire.php?view=2&idpays=4&year="

# Logger config
logs_path = 'logs/logfile.log'
logger.add(logs_path, level="ERROR")


class JpBoxSpider(scrapy.Spider):
    name = "jp_box"
    
    @logger.catch
    def start_requests(self):
        years = list(range(2_024, 1_997, -1))
        for year in years:
            year_url = BASE_URL + str(year)
            # Follow the year page
            yield scrapy.Request(url = year_url,
                                 callback = self.parse_year_page)
            
    @logger.catch
    def parse_year_page(self, response):
        if response.status != 200:
            logger.error(f"Non 200 Status Code: {response.status_code} for URL {response.url}")    
        week_links = response.css("h3 a[href^='v9_tophebdo']::attr(href)").getall()
        for week_link in week_links:
            week_url = "https://www.jpbox-office.com/" + week_link
            # Follow the week page
            yield scrapy.Request(url = week_url,
                                 callback = self.parse_week_page)
            
    @logger.catch
    def parse_week_page(self, response):
        if response.status != 200:
            logger.error(f"Non 200 Status Code: {response.status_code} for URL {response.url}")
        rows = response.css("table.tablesmall5 tr")[1:]
        for row in rows:
            if row.css('td[class$="jaune"]'):
                item = JpboxItem()
                contents = row.css("td.col_poster_contenu_majeur.cellulejaune::text").getall()
                item["jp_copies"] = contents[3].strip()
                film_link = row.css("td.col_poster_titre.cellulejaune a::attr(href)").get()
                film_url = "https://www.jpbox-office.com/" + film_link
                # Follow the film page
                yield scrapy.Request(url = film_url,
                                     callback = self.parse_film_page,
                                     meta = {"item": item})
                
    @logger.catch
    def parse_film_page(self, response):
        if response.status != 200:
            logger.error(f"Non 200 Status Code: {response.status_code} for URL {response.url}")    
        item = response.meta["item"]
        item["jp_title"] = response.css("h1::text").get().strip()
        jp_director = response.css('h4 a[href^="fichacteur"]::text').get()
        try:
            item["jp_director"] = jp_director.strip()
        except AttributeError:
            item["jp_director"] = None
        item["jp_nationality"] = response.css('a[href^="fichepays"]::text').get()
        page = response.text
        item["jp_duration"] = re.search(r"\d?h? ?\d{1,2}min", page).group()
        item["jp_genres"] = response.css('a[href^="fichgenres"]::text').get()
        item["jp_release"] = response.css('a[href^="v9_avenir"]::text').get().strip()
        raw_dist = response.css('div[itemtype="http://schema.org/Organization"]::text').getall()
        raw_dist = [elem.strip() for elem in raw_dist] 
        item["jp_distributors"] = [elem for elem in raw_dist if elem != '']

        yield item
