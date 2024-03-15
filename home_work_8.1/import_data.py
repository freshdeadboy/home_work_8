from mongoengine import connect
import json
from models import Author, Quote

connect('Сluster0', host='mongodb+srv://zajchuk2014:GFnbFetD2EaVWVJh@cluster0.lxirfac.mongodb.net/')

with open('authors.json', 'r') as file:
    authors_data = json.load(file)

with open('quotes.json', 'r') as file:
    quotes_data = json.load(file)

for author_info in authors_data:
    author = Author(**author_info)
    author.save()

for quote_info in quotes_data:
    author_fullname = quote_info.pop('author')
    author = Author.objects(fullname=author_fullname).first()
    if author:
        quote_info['author'] = author
        quote = Quote(**quote_info)
        quote.save()
