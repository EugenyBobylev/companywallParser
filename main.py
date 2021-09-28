from os.path import exists
from typing import List

from bs4 import BeautifulSoup, Tag
import requests
from requests import Response
from model import CompanyInfo

# User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0'
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


def get_full_url(part_url: str) -> str:
    url = 'https://companywall.rs' + part_url
    return url


# ********************** request data from Internet *************************
def get_company_detail(info: CompanyInfo) -> Response:
    url = get_full_url(info.company_url)
    response: Response = get_url(url)
    return response


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


# ********************* parsers *******************************************
def parse_company_info(panel: Tag) -> CompanyInfo:
    _a = panel.select_one('a')
    company_name = _a.text
    company_url = _a['href']

    last_row: Tag = panel.select('.row')[-1]
    company_address = last_row.select('span')[-1].text
    company_info = CompanyInfo(company_name=company_name, company_url=company_url, company_address=company_address)
    return company_info


def parse_companies_info(html: str) -> List[CompanyInfo]:
    _bs = BeautifulSoup(html, 'html.parser')
    _pane: Tag = _bs.select_one('.tab-pane.fade.show.active')
    _panels = _pane.select('.panel')

    companies_info = []
    for panel in _panels:
        company_info = parse_company_info(panel)
        companies_info.append(company_info)

    return companies_info


# ********************* scenaries ******************************************
def load_first_page():
    url = 'https://www.companywall.rs/'
    response = get_url(url)
    if response.status_code != 200:
        print_response_info(response)

    code = '9602'
    response = get_company_by_code(code)
    if response.status_code == 200:
        save_html(response.text, f'data/{code}.html')
        print_response_info(response)


# ********************* aditional funcitons ********************************
def print_response_info(response: Response):
    print(f'status = {response.status_code}')
    print(response.headers)
    print(len(response.text))


if __name__ == '__main__':
    page = load_html('data/detail.html')

    bs = BeautifulSoup(page, 'html.parser')

    # PIB
    pib_tag: Tag = bs.find('dt', text='PIB')
    company_pib = pib_tag.find_next_sibling("dd").text
    print(f'company PIB = {company_pib}')
    # MB
    pib_tag: Tag = bs.find('dt', text='MB')
    company_mb = pib_tag.find_next_sibling("dd").text
    print(f'company MB = {company_mb}')
    # дата основания
    datum_tag: Tag = bs.find('dt', text='Datum osnivanja')
    company_created = datum_tag.find_next_sibling("dd").text
    print(f'created = {company_created}')

    # phone
    print(60 * '*')
    phone_tag: Tag = bs.find('i', class_='fas fa-phone').parent
    part_phone_url = phone_tag.find_next_sibling("dd").find("img")['src']
    phone_url = get_full_url(part_phone_url)
    print(phone_url)
