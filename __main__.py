import os
import ssl
import sys
import time
from datetime import datetime
from itertools import count
from urllib.request import Request, urlopen

# import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

from collection import crawler


def crawling_pelicana():
    results = []

    for page in count(start=110):
        url = 'https://pelicana.co.kr/store/stroe_search.html?page=33&branch_name=&gu=&si=&page=%d' % page

        html = crawler.crawling(url)

        bs = BeautifulSoup(html, 'html.parser')
        tag_table = bs.find('table', attrs={'class': 'table mt20'})
        tag_tbody = tag_table.find('tbody')
        tags_tr = tag_tbody.findAll('tr')

        # 끝 검출
        if len(tags_tr) == 0:
            break

        for tag_tr in tags_tr:
            strings = list(tag_tr.strings)
            name = strings[1]
            address = strings[3]
            sidogu = address.split(' ')[:2]

            results.append((name, address) + tuple(sidogu))

    # store
    # table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gu'])
    # print(table)
    # table.to_csv('__results__/pelicana.csv', encoding='utf-8', mode='w', index=True)

    # for result in results:
    #     print(result)


def crawling_nene():
    results = []
    end_page = ''

    for page in range(1, 5):

        url = 'https://nenechicken.com/17_new/sub_shop01.asp?ex_select=1&ex_select2=&IndexSword=&GUBUN=A&page=%d' % page

        html = crawler.crawling(url)

        bs = BeautifulSoup(html, 'html.parser')
        tags_shopinfo = bs.findAll('div', attrs={'class': 'shopInfo'})

        if end_page == '':
            end_page = bs.find('span', attrs={'class': 'page_noselect'}).text

        print(f'{datetime.now()} : success for request[{url}]')
        # 끝 검출
        if int(end_page) < page:
            break

        for tag in tags_shopinfo:
            name = tag.find('div', {'class': 'shopName'}).text
            address = tag.find('div', {'class': 'shopAdd'}).text
            sido = address.split(' ')[0]
            gusi = address.split(' ')[1]

            results.append((name, address, sido, gusi))

    # store
    # table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gusi'])

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # table.to_csv(f'{BASE_DIR}/__results__/nene.csv', encoding='utf-8', mode='w', index=True)
    # table.to_csv('/root/crawling-results/nene.csv', encoding='utf-8', mode='w', index=True)

def crawling_kyochon():
    results = []

    for sido1 in range(1, 18):
        for sido2 in count(1):
            url = 'http://www.kyochon.com/shop/domestic.asp?sido1=%d&sido2=%d&txtsearch=' % (sido1, sido2)
            html = crawler.crawling(url)

            # 끝 검출
            if html is None:
                break

            bs = BeautifulSoup(html, 'html.parser')
            tag_ul = bs.find('ul', attrs={'class': 'list'})
            tags_span = tag_ul.findAll('span', attrs={'class': 'store_item'})

            for tag_span in tags_span:
                strings = list(tag_span.strings)
                # print(strings)

                name = strings[1]
                address = strings[3].strip('\r\n\t')
                sidogu = address.split()[:2]

                results.append((name, address) + tuple(sidogu))

    # store
    # table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gusi'])
    # print(table)
    # table.to_csv('__results__/kyochon.csv', encoding='utf-8', mode='w', index=True)


def crawling_goobne():
    results = []
    url = 'http://www.goobne.co.kr/store/search_store.jsp'

    wd = webdriver.Chrome('/cafe24/chromedriver/chromedriver.exe')
    wd.get(url)
    time.sleep(5)

    for page in count(1):
        # 자바스크립트 실행
        script = 'store.getList(%d)' % page
        wd.execute_script(script)
        print(f'{datetime.now(): success for request [{script}]}')
        time.sleep(3)

        # 실행결과 HTML(동적으로 랜더링 된 HTML) 가져오기
        html = wd.page_source

        # parsing with bs4
        bs = BeautifulSoup(html, 'html.parser')
        tag_tbody = bs.find('tbody', attrs={'id': 'store_list'})
        tags_tr = tag_tbody.findAll('tr')

        # 마지막 페이지 감지
        if tags_tr[0].get('class') is None:
            break

        for tag_tr in tags_tr:
            strings = list(tag_tr.strings)
            name = strings[1]
            address = strings[6]
            sidogu = address.split()[:2]
            results.append((name, address) + tuple(sidogu))

    wd.quit()

    # store
    # table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gusi'])
    # print(table)
    # table.to_csv('__results__/goobne.csv', encoding='utf-8', mode='w', index=True)


if __name__ == '__main__':
    # pelicana
    # crawling_pelicana()

    # nene
    crawling_nene()

    # kyochon
    # crawling_kyochon()

    # goobne
    # crawling_goobne()
