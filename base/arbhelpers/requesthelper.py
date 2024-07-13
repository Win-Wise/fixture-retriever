import os
from curl_cffi import requests

default_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Connection": "keep-alive",
    "Accept": "application/json",
    "Accept-Encoding": "gzip, deflate, br",
}

proxy = f"http://{os.environ.get('ZR_API_KEY')}:premium_proxy=true&custom_headers=true@proxy.zenrows.com:8001"
proxies = {"http": proxy, "https": proxy}


def make_request(url, use_proxy=False, headers=None):
    return req_with_retry(url=url, retry_num=0, use_proxy=use_proxy, headers=headers)


def req_with_retry(url, retry_num, use_proxy=False, headers=None):
    if headers is None:
        request_headers = default_headers
    else:
        request_headers = dict(default_headers)
        request_headers.update(headers)
    try:
        if use_proxy:
            response = requests.get(url, impersonate="chrome124", headers=request_headers, proxies=proxies, verify=False)
        else:
            response = requests.get(url, impersonate="chrome", headers=headers, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        if retry_num < 3:
            print(f"Exception while accessing url: {url}, retrying...")
            return req_with_retry(url, retry_num + 1, use_proxy=use_proxy, headers=headers)
        else:
            print(f"ERROR. Retries exceeded for url {url}")
            raise e
