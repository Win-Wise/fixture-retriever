import os
import dateutil.parser
from arbhelpers.arbutils import is_valid_event
from arbhelpers.event import BookEvent
from dotenv import load_dotenv
from curl_cffi import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Connection": "keep-alive",
    "Accept": "application/json",
    "Accept-Encoding": "gzip, deflate, br",
    "X-Platform": "cordova-desktop"
}
proxy = f"http://{os.environ.get('ZR_API_KEY')}:premium_proxy=true&custom_headers=true@proxy.zenrows.com:8001"
proxies = {"http": proxy, "https": proxy}
supported_sports = {"Soccer": "football"}
load_dotenv()


def get_participants(event_string):
    event_string = event_string.replace("|", "")
    home, away = event_string.split("vs")
    return home.strip(), away.strip()


def get_events(sport, days_forward):
    url = os.environ.get("CAESARS_EVENTS_REQUEST").format(sport=supported_sports.get(sport))
    response = requests.get(url, impersonate="chrome124", headers=headers, proxies=proxies, verify=False)
    response.raise_for_status()
    for competition in response.json()['competitions']:
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

