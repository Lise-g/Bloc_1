import os
import logging

import scrapy
from scrapy.crawler import CrawlerProcess


class BookingSpider5Spider(scrapy.Spider):
    name = 'booking_spider5'
    # Starting URL
    start_urls = ['https://www.booking.com/searchresults.en-us.html']

    # List of cities
    def __init__(self):
        
        self.list_cities = ["Mont Saint Michel", "St Malo", "Bayeux", "Le Havre", "Rouen", "Paris", "Amiens", "Lille", "Strasbourg", "Chateau du Haut Koenigsbourg", "Colmar", "Eguisheim", "Besancon", "Dijon",
                            "Annecy", "Grenoble", "Lyon", "Gorges du Verdon", "Bormes les Mimosas", "Cassis", "Marseille", "Aix en Provence", "Avignon", "Uzes", "Nimes", "Aigues Mortes", "Saintes Maries de la mer",
                            "Collioure", "Carcassonne", "Ariege", "Toulouse", "Montauban", "Biarritz", "Bayonne", "La Rochelle"]

        self.list_offset = ['0', '25', '50', '75', '100', '125', '150', '175', '200']

    # Parse function for form request
    def parse(self, response):
        # FormRequest used to make a search with several offsets in order to get about 200 hotels per city, and loop over all the required cities
        for i, city in enumerate(self.list_cities) :
            for offset in self.list_offset :
                yield scrapy.FormRequest.from_response(
                    response,
                    formdata={'ss': city, 'offset': offset},
                    callback=self.after_search,
                    cb_kwargs = {'id_city' : i}
                )

    # Callback used after search form
    def after_search(self, response, id_city) :

        names = response.xpath('//*[@class="a1b3f50dcd b2fe1a41c3 a7c67ebfe5 d19ba76520 d14b211b4f"]/div[1]/div/div[1]/div/h3/a/div[1]/text()')
        urls = response.xpath('//*[@class="a1b3f50dcd b2fe1a41c3 a7c67ebfe5 d19ba76520 d14b211b4f"]/div[1]/div/div[1]/div/h3/a')
        scores = response.xpath('//*[@class="a1b3f50dcd b2fe1a41c3 a7c67ebfe5 d19ba76520 d14b211b4f"]/div[2]/div[1]/a/span/div/div[1]/text()')
        descriptions = response.xpath('//*[@class="a1b3f50dcd b2fe1a41c3 a7c67ebfe5 d19ba76520 d14b211b4f"]/div[1]/div/div[3]/text()')


        for name, url, score, description in zip(names, urls, scores, descriptions):
            yield scrapy.Request(
                url = response.urljoin(url.attrib["href"]),
                callback=self.hotel_coord,
                cb_kwargs = {
                    'id_city' : id_city,
                    'city' : response.xpath('//*[@id="right"]/div[1]/div/div/div/h1/text()').get().split(':')[0],
                    'name': name.get(),
                    'url': url.attrib["href"],
                    'score' : score.get(),
                    'description' : description.get()
                }
            )

    def hotel_coord(self, response, id_city, city, name, url, score, description) :

        yield {
            'id_city' : id_city,
            'city' : city,
            'name': name,
            'url': url,
            'score' : score,
            'description' : description,
            'coordinates': response.xpath('//*[@id="hotel_header"]').attrib['data-atlas-latlng'],
        }

# Name of the file where the results will be saved
filename = "hotels_complete5.json"

# If file already exists, delete it before crawling (because Scrapy will concatenate the last and new results otherwise)
if filename in os.listdir('results/'):
        os.remove('results/' + filename)