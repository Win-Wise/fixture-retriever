import requests
import os
from arbhelpers.arbutils import is_valid_event
from arbhelpers.event import BookEvent
from datetime import datetime, timedelta, timezone


suported_sports = {"Soccer": "Soccer"}


def get_events(sport_key, days_forward):
    commence_time_to = (datetime.now() + timedelta(days=days_forward)).strftime("%Y-%m-%dT%H:%M:%SZ")
    sports_data = requests.get("https://api.the-odds-api.com/v4/sports/", params={"apiKey": os.environ["THE_ODDS_API_KEY"]}).json()    # Free
    for sport in sports_data:
        if sport["group"] != suported_sports[sport_key]:
            continue
        league = sport["key"]
        league_dict = requests.get(f"https://api.the-odds-api.com/v4/sports/{league}/events",
                                   params={"apiKey": os.environ["THE_ODDS_API_KEY"], "commenceTimeTo": commence_time_to}).json()    # Free
        for fixture in league_dict:
            e = BookEvent(home=fixture["home_team"], away=fixture["away_team"], sport=sport_key, id_=fixture["id"], book="THEODDSAPI")
            e.start_time = datetime.strptime(fixture["commence_time"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
            if is_valid_event(e, days_forward):
                yield e


def retrieve_fixtures(days_forward):
    for sport in suported_sports.keys():
        for event in get_events(sport, days_forward):
            print("Found event: ", end="")
            event.print()
            yield event
