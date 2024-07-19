from datetime import datetime, timedelta
import os

import boto3
import requests
import betfairlightweight

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


supported_sports = {"Soccer": "1"}


def get_participants(event_string: str):
    pass


def retrieve_fixtures(days_forward: int):
    
    time_range = {
        "from": datetime.now().isoformat(timespec='milliseconds') + 'Z',
        "to": (datetime.now() + timedelta(days=days_forward)).isoformat(timespec='milliseconds') + 'Z'
    }
    
    trading = betfairlightweight.APIClient('dannyray44@hotmail.co.uk',
                                           os.environ['BETFAIR_PASSWORD'],
                                           app_key=os.environ['BETFAIR_APP_KEY'], 
                                           cert_files=("/tmp/client-2048.crt", "/tmp/client-2048.key"),
                                           lightweight=True)

    trading.login()

    for sport_id in supported_sports.keys():
        events_list = trading.betting.list_events(filter=betfairlightweight.filters.market_filter(event_type_ids=sport_id, market_start_time=time_range))
        for event in events_list:
            yield event

    trading.logout()


if __name__ == "__main__":
    retrieve_fixtures(1)