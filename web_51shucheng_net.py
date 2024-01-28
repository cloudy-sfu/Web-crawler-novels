from requests import Session
from bs4 import BeautifulSoup
import re
import logging

chrome_110 = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.7',
    'accept-encoding': 'gzip, deflate',
    'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'cache-control': 'max-age=0',
    'dnt': '1',
    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"', 'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none', 'sec-fetch-user': '?1', 'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/110.0.0.0 Safari/537.36'
}
session = Session()
session.trust_env = False


def get_meta(source):
    cover_page = session.get(url=source, headers=chrome_110)
    if cover_page.status_code != 200:
        raise Exception(f'Fail to get the cover page. Status code: {cover_page.status_code}.')
    else:
        logging.info('Success to get the cover page.')
    cover_page.encoding = 'utf-8'
    cover_text = BeautifulSoup(cover_page.text, features='html.parser')
    chapter_list = cover_text.find('div', {'class': 'mulu-list'}).find_all('li')
    chapter_list = [[x.a.text, x.a['href']] for x in chapter_list]
    book = {
        'title': cover_text.find('div', {'class': 'catalog'}).h1.text,
        'author': re.sub('.*作者：', '', cover_text.find('div', {'class': 'info'}).text.strip()),
        'abstract': cover_text.find('div', {'class': 'intro'}).text,
        'chapter_list': chapter_list,
    }
    return book


def get_chapter(source):
    chapter_page = session.get(url=source, headers=chrome_110)
    if chapter_page.status_code != 200:
        logging.warning(f'Fail to download {source}. Status code: {chapter_page.status_code}. ')
        return
    chapter_page.encoding = 'utf-8'
    chapter_text = BeautifulSoup(chapter_page.text, features='html.parser')
    chapter_title = chapter_text.find('h1').text
    chapter_normal = chapter_text.find('div', {'class': 'neirong'}).text
    chapter_normal = chapter_normal.replace('\xa0', '')
    chapter_normal = re.sub('\n+', '\n\n', chapter_normal)
    chapter_normal = re.sub('<emclass=(.*?)>', '', chapter_normal)
    chapter_normal = re.sub('</?em>', '', chapter_normal)
    chapter_normal = re.sub('\n+tang\n+', '', chapter_normal)
    chapter_normal = re.sub('<\n?p>', '', chapter_normal)
    chapter = {'title': chapter_title, 'body': chapter_normal}
    return chapter
