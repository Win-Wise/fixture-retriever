import os
import dateutil.parser
from arbhelpers.arbutils import clean_name, is_valid_event
from arbhelpers.event import Event
from curl_cffi import requests
from dotenv import load_dotenv

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Connection": "keep-alive",
    "Accept": "application/json",
    "Accept-Encoding": "gzip, deflate, br",
    "X-Platform": "cordova-desktop"
}
supported_sports = {"Soccer": "1"}
load_dotenv()


def get_participants(event_string):
    event_string = event_string.strip()
    home, away = event_string.split(" v ")
    return clean_name(home), clean_name(away)


def req_with_retry(url, retry_num):
    try:
        response = requests.get(url, impersonate="chrome", timeout=20)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        if retry_num < 3:
            print(f"Exception while accessing url: {url}, retrying...")
            return req_with_retry(url, retry_num + 1)
        else:
            print(f"ERROR. Retries exceeded for url {url}")
            raise e


def get_events(sport, days_forward):
    url = os.environ.get("FANDUEL_EVENTS_REQUEST").format(sport=supported_sports.get(sport))
    response = req_with_retry(url, retry_num=0)
    for event_id, event in response['attachments']['events'].items():
        #home, away, sport, id, book
        if " v " in event['name']:
            home, away = get_participants(event['name'])
            start_time = dateutil.parser.isoparse(event['openDate'])
            e = Event(home=home, away=away, sport=sport.lower(), id_=event_id, book='FANDUEL')
            e.start_time = start_time
            if is_valid_event(e, days_forward):
                yield e


def retrieve_fixtures(days_forward):
    for sport_ in supported_sports.keys():
        for event_ in get_events(sport_, days_forward):
            print("Found event: ", end="")
            event_.print()
            yield event_