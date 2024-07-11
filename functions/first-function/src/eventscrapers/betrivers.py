import os
import dateutil.parser
from arbhelpers.arbutils import is_valid_event
from arbhelpers.event import BookEvent
from curl_cffi import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Connection": "keep-alive",
    "Accept": "application/json",
    "Accept-Encoding": "gzip, deflate, br"
}
supported_sports = {"Soccer": 1000093190}


def req_with_retry(url, retry_num):
    try:
        response = requests.get(url, impersonate="chrome",headers=headers, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        if retry_num < 3:
            print(f"Exception while accessing url: {url}, retrying...")
            return req_with_retry(url, retry_num + 1)
        else:
            print(f"ERROR. Retries exceeded for url {url}")
            raise e


def get_events_page(page_json, sport, days_forward):
    for fixture in page_json['items']:
        home = fixture['participants'][0]
        away = fixture['participants'][1]
        if not home['home']:
            temp = home
            home = away
            away = temp
        start_time = dateutil.parser.isoparse(fixture['start'])
        event = BookEvent(home['name'], away['name'], sport.lower(), str(fixture['id']), "BETRIVERS")
        event.start_time = start_time
        if is_valid_event(event, days_forward):
            yield event


def get_events(group, sport, days_forward):
    page = 1
    while True:
        url = os.environ.get("BETRIVERS_EVENTS_REQUEST").format(group=group, page=page)
        response = req_with_retry(url, retry_num=0)
        for event in get_events_page(response, sport, days_forward):
            if is_valid_event(event, days_forward):
                yield event
        if response['paging']['totalPages'] <= page:
            break
        else:
            page += 1


def retrieve_fixtures(days_forward):
    for sport_, group in supported_sports.items():
        for event_ in get_events(group, sport_, days_forward):
            print("Found event: ", end="")
            event_.print()
            yield event_
