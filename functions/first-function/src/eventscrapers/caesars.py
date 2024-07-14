import os
import dateutil.parser
from arbhelpers.arbutils import is_valid_event
from arbhelpers.event import BookEvent
from arbhelpers.requesthelper import make_request
from dotenv import load_dotenv

supported_sports = {"Soccer": "football"}
load_dotenv()


def get_participants(event_string):
    event_string = event_string.replace("|", "")
    home, away = event_string.split(" vs ")
    return home.strip(), away.strip()


def get_events(sport, days_forward):
    url = os.environ.get("CAESARS_EVENTS_REQUEST").format(sport=supported_sports.get(sport))
    response = make_request(url=url, proxy_settings={'enabled': True, 'params': {'premium_proxy': True}}, headers={'X-Platform': 'cordova-desktop'})
    for competition in response['competitions']:
        for event in competition['events']:
            home, away = get_participants(event['name'])
            e = BookEvent(home, away, sport.lower(), event['id'], 'CAESARS')
            e.start_time = dateutil.parser.isoparse(event['startTime'])
            if is_valid_event(e, days_forward):
                yield e


def retrieve_fixtures(days_forward):
    for sport_ in supported_sports.keys():
        for event_ in get_events(sport_, days_forward):
            print("Found event: ", end="")
            event_.print()
            yield event_

