from os.path import exists

from bs4 import BeautifulSoup
import requests
from requests import Response

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0'}


# *********************** Utils *********************************************
def save_html(html: str, fn: str):
    if html:
        with open(fn, 'w', encoding='utf-8') as f:
            f.write(html)


def load_html(fn: str) -> str:
    if exists(fn):
        with open(fn, 'r') as f:
            _html = f.read()
            return _html


# ********************** request data from Internet *************************
def get_company_by_code(code: str) -> Response:
    _url = f'https://www.companywall.rs/pretraga?cr=RSD&n=&mv=&r=&c=&FromDateAlt=&FromDate=&ToDateAlt=' \
           f'&ToDate=&at={code}&area=&subarea=&sbjact=t&type=&hr=&dsm%5B0%5D.Code=1101&dsm%5B1%5D.' \
           f'Code=966&dsm%5B-1%5D.Code=0&dsm%5B-1%5D.From=0&dsm%5B-1%5D.To=0&xpnd=true HTTP/1.1'
    _response = get_url(_url)
    return _response


def get_url(url: str) -> Response:
    global headers
    _response = requests.get(url, headers=headers)
    if 'Set-Cookie' in _response.headers:
        headers['Cookie'] = _response.headers['Set-Cookie']
    return _response


# ********************* scenaries ******************************************
def load_first_page():
    url = 'https://www.companywall.rs/'
    response = get_url(url)
    if response.status_code != 200:
        print_response_info()

    code = '9602'
    response = get_company_by_code(code)
    if response.status_code == 200:
        save_html(response.text, f'data/{code}.html')
        print_response_info()


# ********************* aditional funcitons ********************************
def print_response_info():
    print(f'status = {response.status_code}')
    print(response.headers)
    print(len(response.text))


if __name__ == '__main__':
    page = load_html('data/9602.html')

    bs = BeautifulSoup(page, 'html.parser')
    pane = bs.select_one('.tab-pane.fade.show.active')

    panels = pane.select('.panel')
    print(f'count of panels = {len(panels)}')

    print(30 * '*')
    panel = panels[0]
    a = panel.select_one('a')
    company_name = a.text
    company_url = a['href']

    last_row = panel.select('.row')[-1]
    company_address = last_row.select('span')[-1].text

    print(f'name = "{company_name}"')
    print(f'url = "{company_url}"')
    print(f'adress = {company_address}')
