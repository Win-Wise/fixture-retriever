import os
from curl_cffi import requests
from arbhelpers.arbutils import clean_name, is_valid_event, next_n_days
from arbhelpers.event import Event
from datetime import datetime

headers = {
    'x-rapidapi-key': os.environ["RAPIDAPI_KEY"],
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
}
url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"


def generate_id(home_team, away_team, sport, start_time):
    return str(abs(hash((home_team, away_team, sport, start_time.isoformat()))))


def get_events(days_forward):
    for d in next_n_days(days_forward):
        querystring = {"date": f"{d:%Y-%m-%d}", "status": "NS"}
        response = requests.get(url, impersonate="chrome", headers=headers, params=querystring).json()
        for fixture in response['response']:
            sport = "SOCCER"
            home = clean_name(fixture['teams']['home']['name'])
            away = clean_name(fixture['teams']['away']['name'])
            start_time = fixture['fixture']['date']
            start_time = datetime.fromisoformat(start_time)
            id_ = generate_id(home, away, sport, start_time)
            e = Event(home, away, sport, id_)
            e.start_time = start_time
            e.league = clean_name(fixture['league']['name'])
            if is_valid_event(e, days_forward=days_forward):
                yield e
