import os
import dateutil.parser
from dotenv import load_dotenv
from arbhelpers.arbutils import is_valid_event
from arbhelpers.event import BookEvent
from arbhelpers.requesthelper import make_request

supported_sports = {"Soccer"}
load_dotenv()


def get_groups():
    url = os.environ.get("DRAFTKINGS_GROUPS_REQUEST")
    response = make_request(url)
    for group in response['displayGroupInfos']:
        if group['displayName'] in supported_sports:
            for eventGroup in group['eventGroupInfos']:
                yield eventGroup['eventGroupId'], group['displayName']


def get_events(group, sport, days_forward):
    url = os.environ.get("DRAFTKINGS_EVENTS_REQUEST").format(group=group)
    response = make_request(url)
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
