import os
import importlib
import boto3
from pymongo import MongoClient
from arbhelpers.arbutils import get_embedding

client = MongoClient(host=os.environ["MONGODB_URI"])
collection = fixtures_coll = client['arbriver']['fixtures']

# WE DON'T WANT THIS CODE TO EXECUTE FOR EVERY LAMBDA SO WE KEEP IT ABOVE THE HANDLER
secrets_client = boto3.client(service_name='secretsmanager', region_name='us-east-1')
betfair_password = secrets_client.get_secret_value(SecretId=os.environ['BETFAIR_PASSWORD_SECRET']).get('SecretString')
betfair_app_key = secrets_client.get_secret_value(SecretId=os.environ['BETFAIR_APP_KEY_SECRET']).get('SecretString')
zr_api_key = secrets_client.get_secret_value(SecretId=os.environ['ZR_API_KEY_SECRET']).get('SecretString')
uk_https_proxy = secrets_client.get_secret_value(SecretId=os.environ['UK_HTTPS_PROXY_SECRET']).get('SecretString')

os.environ['BETFAIR_PASSWORD'] = betfair_password
os.environ['BETFAIR_APP_KEY'] = betfair_app_key
os.environ['ZR_API_KEY'] = zr_api_key
os.environ['UK_HTTPS_PROXY'] = uk_https_proxy

s3 = boto3.resource('s3')
BUCKET_NAME = os.environ['ARBRIVER_BUCKET']
s3.Bucket(BUCKET_NAME).download_file('betfair-certs/client-2048.crt', '/tmp/client-2048.crt')
s3.Bucket(BUCKET_NAME).download_file('betfair-certs/client-2048.key', '/tmp/client-2048.key')

def lambda_handler(event, context):
    book = event['book'].lower()
    days_forward = event['days_forward']
    print(f"Loading module eventscrapers.{book}")
    scraper = importlib.import_module("eventscrapers." + book)
    print(f"Searching {days_forward} days forward for book: {book}")
    num_events = 0
    for e in scraper.retrieve_fixtures(days_forward):
        num_events += 1
        e_dict = e.to_dict()
        e_dict['text_embedding'] = get_embedding(e)
        collection.replace_one({"_id": e_dict["_id"]}, e_dict, upsert=True)
    print(f"Retrieved {num_events} events")
    return True
