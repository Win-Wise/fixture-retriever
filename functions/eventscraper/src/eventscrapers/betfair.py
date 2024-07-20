from datetime import datetime, timedelta
from arbhelpers.event import BookEvent
import os
import requests
import betfairlightweight

supported_sports = {"soccer": 1}


def initialize_session():
    proxy = os.environ.get('UK_HTTPS_PROXY')
    proxies = {"http": proxy, "https": proxy}
    session = requests.Session()
    session.proxies = proxies

    session.cert = ("/tmp/client-2048.crt", "/tmp/client-2048.key")
    session.verify = False
    return session


def retrieve_fixtures(days_forward: int):
    session = initialize_session()
    events_dict = {}
    
    time_range = {
        "from": datetime.now().isoformat(timespec='milliseconds') + 'Z',
        "to": (datetime.now() + timedelta(days=days_forward)).isoformat(timespec='milliseconds') + 'Z'
    }
    
    trading = betfairlightweight.APIClient(os.environ['BETFAIR_USERNAME'],
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
