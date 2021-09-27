import requests
from requests import Response


def save_html(html: str, fn: str):
    if html:
        with open(fn, 'w', encoding='utf-8') as f:
            f.write(html)


def get_url(url: str) -> Response:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0'}
    _response = requests.get(url,headers=headers)
    return _response


if __name__ == '__main__':
    url = 'https://www.companywall.rs/'
    response = get_url(url)

    print(f'status = {response.status_code}')
    print(len(response.text))

    if response.status_code == 200:
        save_html(response.text, 'data/main.html')
