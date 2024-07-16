import os
from datetime import timedelta, timezone
from arbhelpers.arbutils import clean_name
from pymongo import MongoClient
import rapidfuzz

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
                'hyperlink': 1,
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
        is_link = False
        num_candidates += 1
        candidate_start_time = i['start_time'].astimezone(timezone.utc)
        link = {
            'event_id': i['_id'],
            'score': i['score'],
            'text': i['text'],
            'start_time': candidate_start_time,
            'book': i['book'],
        }
        if 'hyperlink' in i:
            link['hyperlink'] = i['hyperlink']

        if i['score'] >= 0.95: #exact match
            upper_bound = start_time + timedelta(hours=12)
            lower_bound = start_time - timedelta(hours=12)
            if upper_bound > candidate_start_time > lower_bound:
                is_link = True
        elif i['score'] > 0.8: #good match
            upper_bound = start_time + timedelta(hours=2)
            lower_bound = start_time - timedelta(hours=2)
            if upper_bound > candidate_start_time > lower_bound:
                is_link = True
        elif i['score'] > 0.65: #decent match
            upper_bound = start_time + timedelta(minutes=30)
            lower_bound = start_time - timedelta(minutes=30)
            if upper_bound > candidate_start_time > lower_bound:
                if i['home'] == event_dict['home'] or i['away'] == event_dict['away']:
                    is_link = True

        if is_link:
            home, away = i['home'], i['away']
            if i['book'] == 'CAESARS': #sometimes caesars flips the home and away teams
                home, away = reconcile_sides(i, event_dict)

            link['home'] = home
            link['away'] = away
            matches.append(link)

    return matches


def reconcile_sides(matched, fixture):
    home_to_home = rapidfuzz.fuzz.QRatio(clean_name(matched['home'].replace("women", "")), clean_name(fixture['home'].replace("women", "")))
    home_to_away = rapidfuzz.fuzz.QRatio(clean_name(matched['home'].replace("women", "")), clean_name(fixture['away'].replace("women", "")))
    if home_to_home >= home_to_away:
        return matched['home'], matched['away']
    else:
        print(f"{matched['home']} vs {matched['away']} and {fixture['home']} vs {fixture['away']} are flipped on {matched['book']}. Flipping back...")
        return matched['away'], matched['home']
