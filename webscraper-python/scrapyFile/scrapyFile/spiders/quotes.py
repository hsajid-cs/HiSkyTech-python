import scrapy
import datetime
import pandas as pd
from scrapy.crawler import CrawlerProcess


def insertToDB(title, statement, author, tags):
    """
    Funtion to insert the data into the database
    title: Title of the page
    statement: The quote
    author: The author of the quote
    tags: Tags associated with the quote
    rtype: None
    """
    doc = {"statement": statement, "author": author, "tags": tags, "date":datetime.datetime.now(tz=datetime.timezone.utc)}
    # create a dataframe
    df = pd.DataFrame([doc])
    # write dataframe to csv file
    df.to_csv(f"{title}.csv", mode='a',header=not pd.io.common.file_exists(f"{title}.csv"), lineterminator='\n', index=False)

class QuotesSpider(scrapy.Spider):
    """
    Spider to scrape the quotes from the website
    """
    name = "quotes" # Name of the spider
    allowed_domains = ["toscrape.com"] # Allowed domains

    def start_requests(self):

        # List of URLs to scrape
        start_urls = ['https://quotes.toscrape.com/tag/love',
                      'https://quotes.toscrape.com/tag/inspirational',
                        'https://quotes.toscrape.com/tag/friendship']
        
        # Looping through the URLs
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """
        Function to parse the response and extract the data
        response: The response from the website
        rtype: None
        """

        # Extracting the title of the page
        title = response.css('h3>a::text').get()

        # Extracting the quotes
        quotes = response.css('.quote')

        # Looping through the quotes
        for quote in quotes:
            statement = quote.css('.text::text').get().strip('“”') # Extracting the quote
            author = quote.css('.author::text').get() # Extracting the author
            tags = quote.css('.tags a::text').getall() # Extracting the tags
            id = insertToDB(title, statement, author, tags) # Inserting the data into the database
        

        # Follow pagination link
        next_page = response.css('ul.pager li.next a::attr(href)').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_url, callback=self.parse)

process = CrawlerProcess()
process.crawl(QuotesSpider)
process.start()
