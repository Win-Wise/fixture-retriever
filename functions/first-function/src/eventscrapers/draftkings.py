import os
import dateutil.parser
from dotenv import load_dotenv
from arbhelpers.arbutils import is_valid_event
from arbhelpers.event import BookEvent
from curl_cffi import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Connection": "keep-alive",
    "Accept": "application/json",
    "Accept-Encoding": "gzip, deflate, br"
}
supported_sports = {"Soccer"}
load_dotenv()


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


def get_groups():
    url = os.environ.get("DRAFTKINGS_GROUPS_REQUEST")
    response = req_with_retry(url, retry_num=0)
    for group in response['displayGroupInfos']:
        if group['displayName'] in supported_sports:
            for eventGroup in group['eventGroupInfos']:
                yield eventGroup['eventGroupId'], group['displayName']


def get_events(group, sport, days_forward):
    url = os.environ.get("DRAFTKINGS_EVENTS_REQUEST").format(group=group)
    response = req_with_retry(url, retry_num=0)
    for event in response['eventGroup']['events']:
        if 'teamName1' in event:
            e = BookEvent(event['teamName1'],
                      event['teamName2'],
                      sport.lower(), event['eventId'],
                      'DRAFTKINGS')
            e.start_time = dateutil.parser.isoparse(event['startDate'])
            if 'mediaList' in event:
                for media in event['mediaList']:
                    if "betradar" in media['mediaProviderName'].lower():
                        e.betradar_id = media['mediaId']
                        break
            if is_valid_event(e, days_forward=days_forward):
                yield e


def retrieve_fixtures(days_forward):
    for group_, sport_ in get_groups():
        for event_ in get_events(group_, sport_, days_forward):
            print("Found event: ", end="")
            event_.print()
            yield event_
