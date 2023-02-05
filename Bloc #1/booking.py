import os
import logging

import scrapy
from scrapy.crawler import CrawlerProcess

class BookingSpider(scrapy.Spider):
    # Name of your spider
    name = "booking"

    # Starting URL
    start_urls = ['https://www.booking.com/index.fr.html?label=gen173nr-1BCAEoggI46AdIM1gEaE2IAQGYAQ24AQfIAQzYAQHoAQGIAgGoAgO4AqPW-Z4GwAIB0gIkMDhiNWU4YjEtMjY3NS00OWQ4LWJhNjEtMjBhOGJhNjZlYjNh2AIF4AIB&sid=6f08f67db155f4465fc126b846333584&keep_landing=1&sb_price_type=total&']

    # Parse function for form request
    def parse(self, response):
        # FormRequest used to make a search in Paris
        return scrapy.FormRequest.from_response(
            response,
            formdata={'ss': 'Mont Saint Michel'},
            callback=self.after_search
        )

    # Callback used after login
    def after_search(self, response):
        
        name = response.xpath('/html/body/div[3]/div/div[4]/div[1]/div[1]/div[4]/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div[2]/div/div/div/div[1]/div/div[1]/div/h3/a/div[1]').get()
        url = response.xpath('/html/body/div[3]/div/div[4]/div[1]/div[1]/div[4]/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div[2]/div/div/div/div[1]/div/div[1]/div/h3/a').get()
        distance = response.xpath('/html/body/div[3]/div/div[4]/div[1]/div[1]/div[4]/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div[2]/div/div/div/div[1]/div/div[2]/div/span/span/span').get()
        score = response.xpath('/html/body/div[3]/div/div[4]/div[1]/div[1]/div[4]/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div[2]/div/div/div/div[2]/div[1]/div/a/span/div/div[1]').get()
        description = response.xpath('/html/body/div[3]/div/div[4]/div[1]/div[1]/div[4]/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div[2]/div/div/div/div[1]/div/div[3]').get()


    
        yield {
            'name': name,
            'url': url.attrib["href"],
            'distance_from_center': distance,
            'score': score,
            'description': description
         }

        try:
            next_page = response.css('a.next-link').attrib["href"]
        except KeyError:
            logging.info('No next page. Terminating crawling process.')
        else:
            yield response.follow(next_page, callback=self.parse)

# Name of the file where the results will be saved
filename = "hotels_mont_sait_michel" + '.json'

# If file already exists, delete it before crawling (because Scrapy will concatenate the last and new results otherwise)
if filename in os.listdir('Projet_Kayak/'):
        os.remove('Projet_Kayak/' + filename)

# Declare a new CrawlerProcess with some settings
process = CrawlerProcess(settings = {
    'USER_AGENT': 'Chrome/97.0',
    'LOG_LEVEL': logging.INFO,
    "AUTOTHROTTLE_ENABLED": True,
    "FEEDS": {
        'Projet_Kayak/' + filename: {"format": "json"},
    }
})

# Start the crawling using the spider you defined above
process.crawl(BookingSpider)
process.start()