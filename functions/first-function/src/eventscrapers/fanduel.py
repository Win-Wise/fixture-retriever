import os
import dateutil.parser
from arbhelpers.arbutils import is_valid_event
from arbhelpers.event import BookEvent
from arbhelpers.requesthelper import make_request
from dotenv import load_dotenv

supported_sports = {"Soccer": "1"}
load_dotenv()


def get_participants(event_string):
    event_string = event_string.strip()
    home, away = event_string.split(" v ")
    return home.strip(), away.strip()


def get_events(sport, days_forward):
    url = os.environ.get("FANDUEL_EVENTS_REQUEST").format(sport=supported_sports.get(sport))
    response = make_request(url)
    for event_id, event in response['attachments']['events'].items():
        #home, away, sport, id, book
        if " v " in event['name']:
            home, away = get_participants(event['name'])
            start_time = dateutil.parser.isoparse(event['openDate'])
            e = BookEvent(home=home, away=away, sport=sport.lower(), id_=event_id, book='FANDUEL')
            e.start_time = start_time
            if is_valid_event(e, days_forward):
                yield e


def retrieve_fixtures(days_forward):
    for sport_ in supported_sports.keys():
        for event_ in get_events(sport_, days_forward):
            print("Found event: ", end="")
            event_.print()
            yield event_
