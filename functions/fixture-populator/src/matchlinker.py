import os
from datetime import timedelta, timezone
from pymongo import MongoClient

# connect to your Atlas cluster
client = MongoClient(host=os.environ["MONGODB_URI"])
fixtures_coll = client["arbriver"]["fixtures"]
match_coll = client["arbriver"]["matches"]

# MATCHING STRATEGY
# first grab 15 closest events (each event represents an event on a sportsbook)
# for each neighbor, do the following:
    # if the neighbor is an exact match (score >=0.95), add it to matches as long as it has a start_time within 24 hours of the fixture
    # if the neighbor is a close match (score >=0.8), add it to matches as long as it has a start_time within 4 hours of the fixture
    # if the neighbor is a possible match (score >=0.65)
        # add it to matches as long as start_time is within 1 hour and at least 1 of home/away is exact match


def get_match_links(event_dict):
    pipeline = [
        {
            '$vectorSearch': {
                'index': 'vector_index',
                'path': 'text_embedding',
                'queryVector': event_dict['text_embedding'],
                'numCandidates': 256,
                'limit': 15
            }
        }, {
            '$project': {
                '_id': 1,
                'book': 1,
                'text': 1,
                'home': 1,
                'away': 1,
                'start_time': 1,
                'score': {
                    '$meta': 'vectorSearchScore'
                }
            }
        }
    ]
    result = fixtures_coll.aggregate(pipeline)
    matches = []

    start_time = event_dict['start_time'].astimezone(timezone.utc)
    num_candidates = 0
    for i in result:
        num_candidates += 1
        candidate_start_time = i['start_time'].astimezone(timezone.utc)
        link = {
            'event_id': i['_id'],
            'score': i['score'],
            'text': i['text'],
            'start_time': candidate_start_time,
            'book': i['book'],
            'home': i['home'],
            'away': i['away'],
        }

        if i['score'] >= 0.95: #exact match
            upper_bound = start_time + timedelta(hours=12)
            lower_bound = start_time - timedelta(hours=12)
            if upper_bound > candidate_start_time > lower_bound:
                matches.append(link)
        elif i['score'] > 0.8: #good match
            upper_bound = start_time + timedelta(hours=2)
            lower_bound = start_time - timedelta(hours=2)
            if upper_bound > candidate_start_time > lower_bound:
                matches.append(link)
        elif i['score'] > 0.65: #decent match
            upper_bound = start_time + timedelta(minutes=30)
            lower_bound = start_time - timedelta(minutes=30)
            if upper_bound > candidate_start_time > lower_bound:
                if i['home'] == event_dict['home'] or i['away'] == event_dict['away']:
                    matches.append(link)
    return matches
