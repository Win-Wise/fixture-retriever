import os
from urllib import parse
from json import JSONDecodeError

from curl_cffi import requests

default_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Connection": "keep-alive",
    "Accept": "application/json",
    "Accept-Encoding": "gzip, deflate, br",
}


def generate_proxies(proxy_settings):
    base = f"http://{os.environ.get('ZR_API_KEY')}:custom_headers=true"
    suffix = "@proxy.zenrows.com:8001"
    if not proxy_settings['enabled']:
        return None
    else:
        if 'params' in proxy_settings:
            proxy = base + "&" + parse.urlencode(proxy_settings['params']) + suffix
        else:
            proxy = base + suffix
        return {"http": proxy, "https": proxy}


def make_request(url, proxy_settings=None, headers=None):
    if proxy_settings is None:
        proxies = None
    else:
        proxies = generate_proxies(proxy_settings)

    if headers is None:
        request_headers = default_headers
    else:
        request_headers = dict(default_headers)
        request_headers.update(headers)

    return req_with_retry(url=url, retry_num=0, proxies=proxies, request_headers=request_headers)


def req_with_retry(url, retry_num, proxies=None, request_headers=None):
    try:
        print(f"Requesting url: {url} with proxy: {proxies} and headers: {request_headers}")
        if proxies is not None:
            response = requests.get(url, impersonate="chrome124", headers=request_headers, proxies=proxies, verify=False)
        else:
            response = requests.get(url, impersonate="chrome", headers=request_headers, timeout=5)
        response.raise_for_status()
        try:
            resp_page = response.json()
            return resp_page
        except JSONDecodeError as jse:
            print(f"Error: {jse.msg}, could not parse body as json for request with status: {response.status_code}:\n{response}")
            raise Exception
    except Exception as e:
        if retry_num < 3:
            print(f"Exception {e} while accessing url: {url}, retrying...")
            return req_with_retry(url, retry_num + 1, proxies=proxies, request_headers=request_headers)
        elif retry_num == 3 and proxies is None:
            print(f"Exception {e} while accessing url: {url}. Last retry, trying with proxy...")
            return req_with_retry(url, retry_num + 1,
                                  proxies=generate_proxies({
                                      'enabled': True,
                                      'params': {
                                          'premium_proxy': True,
                                          'proxy_country': 'us'
                                      }
                                  }),
                                  request_headers=request_headers)
        else:
            print(f"ERROR. Retries exceeded for url {url}")
            raise e
