import os
import importlib
from pymongo import MongoClient

client = MongoClient(host=os.environ["MONGODB_URI"])
collection = fixtures_coll = client['arbriver']['fixtures']


def lambda_handler(event, context):
    book = event['book'].lower()
    days_forward = event['days_forward']
    print(f"Loading module eventscrapers.{book}")
    scraper = importlib.import_module("eventscrapers." + book)
    print(f"Searching {days_forward} days forward for book: {book}")
    num_events = 0
    for e in scraper.retrieve_fixtures(days_forward):
        num_events += 1
        e = e.to_dict()
        collection.replace_one({"_id": e["_id"]}, e, upsert=True)
    print(f"Retrieved {num_events} events")
    return True
