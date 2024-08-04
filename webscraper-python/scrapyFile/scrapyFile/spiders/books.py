import scrapy
from pymongo import MongoClient
import datetime

client = MongoClient("mongodb+srv://root:helloworld@books.oehyryf.mongodb.net/")
books = client.books
def insertToDB(page, image, title, price, rating):
    genre = books[page]
    doc = {"image": image, "title": title, "price": price, "rating": rating, "date":datetime.datetime.now(tz=datetime.timezone.utc)}
    post_id = genre.insert_one(doc).inserted_id
    

class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["toscrape.com"]

    def start_requests(self):
        urls = ["http://books.toscrape.com/catalogue/category/books/romance_8/index.html",
               "http://books.toscrape.com/catalogue/category/books/travel_2/index.html"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = (response.url.split('/')[-2]).split('_')[0]
        ratings = {
            'One': 1,
            'Two': 2,
            'Three': 3,
            'Four': 4,
            'Five': 5
        }
        cards = response.css(".product_pod")
        for card in cards:
            title = card.css('h3>a::text').get()
            price = card.css('.product_price>p::text').get()
            rating = card.css(".star-rating").attrib['class']
            rating = ratings[rating.split(" ")[1]]
            image = (card.css('.image_container img')).attrib["src"]
            image = image.replace("../../../../","http://books.toscrape.com/")
            insertToDB(page, image, title, price, rating)


# https://www.brainyquote.com/authors/muhammad-ali-jinnah-quotes
# https://www.brainyquote.com/authors/mahatma-gandhi-quotes
# https://www.brainyquote.com/authors/martin-luther-king-jr-quotes