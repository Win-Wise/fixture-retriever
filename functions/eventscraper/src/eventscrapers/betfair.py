from datetime import datetime, timedelta
import os

import boto3
import requests
import betfairlightweight

from arbhelpers.event import BookEvent

proxy = f"https://Iv08hg:KelqtNSB@89-34-98-2.ip.ipb.cloud:9443"
proxies = {"http": proxy, "https": proxy}
session = requests.Session()
session.proxies = proxies

s3 = boto3.resource('s3')

BUCKET_NAME = os.environ['ARBRIVER_BUCKET']
keys = ['client-2048.crt', 'client-2048.key', 'client-2048.pem']
for KEY in keys:
    local_file_name = '/tmp/'+KEY
    s3.Bucket(BUCKET_NAME).download_file('betfair-certs/' + KEY, local_file_name)
session.cert = ("/tmp/client-2048.crt", "/tmp/client-2048.key")
session.verify = False


supported_sports = {"soccer": 1}


def get_participants(event_string: str):
    return 


def retrieve_fixtures(days_forward: int):
    events_dict = {}
    
    time_range = {
        "from": datetime.now().isoformat(timespec='milliseconds') + 'Z',
        "to": (datetime.now() + timedelta(days=days_forward)).isoformat(timespec='milliseconds') + 'Z'
    }
    
    trading = betfairlightweight.APIClient('dannyray44@hotmail.co.uk',
                                           os.environ['BETFAIR_PASSWORD'],
                                           app_key=os.environ['BETFAIR_APP_KEY'], 
                                           cert_files=("/tmp/client-2048.crt", "/tmp/client-2048.key"),
                                           session=session,
                                           lightweight=True)

    trading.login()

    for sport_name, sport_id in supported_sports.items():
        events_dict[sport_name] = trading.betting.list_events(
            filter= betfairlightweight.filters.market_filter(
                event_type_ids=[sport_id], 
                market_start_time= time_range
            )
        )

    # print(f"events_dict = {events_dict['soccer']}")

    for sport_name, events_list in events_dict.items():
        for event in events_list:
            try:
                home, away = event['event']['name'].split(' v ')
            except Exception as e:
                print(e)
                continue
            ev = BookEvent(home, away, sport_name, event['event']['id'], 'BETFAIR')
            ev.start_time = datetime.fromisoformat(event['event']['openDate'][:-1])
            yield ev
            

    trading.logout()




if __name__ == "__main__":
    retrieve_fixtures(1)
