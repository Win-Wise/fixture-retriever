from apifootball import get_events
from arbhelpers.arbutils import get_embedding
from matchlinker import get_match_links
from pymongo import MongoClient
import boto3
import os

client = MongoClient(host=os.environ["MONGODB_URI"])
matches_coll = client['arbriver']['matches']

secrets_client = boto3.client(service_name='secretsmanager', region_name='us-east-1')
os.environ['RAPIDAPI_API_KEY'] = secrets_client.get_secret_value(SecretId=os.environ['RAPIDAPI_API_KEY_SECRET']).get('SecretString')

def lambda_handler(event, context):
    for event_ in get_events(event['days_forward']):
        embedding = get_embedding(event_)
        e_dict = event_.to_dict()
        e_dict['text_embedding'] = embedding
        matches = get_match_links(e_dict)
        if len(matches) > 0:
            e_dict['links'] = matches
            del e_dict['text_embedding']
            print(f"Found {len(matches)} bookmaker items for event: {e_dict['text']}")
            matches_coll.replace_one({"_id": e_dict["_id"]}, e_dict, upsert=True)
        else:
            print(f"No bookmaker items for event: {e_dict['text']}, skipping...")
