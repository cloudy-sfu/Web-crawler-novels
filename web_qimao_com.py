import json
import logging
import os
import re

from bs4 import BeautifulSoup
from requests import Session

chrome_135 = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en,zh-CN;q=0.9,zh;q=0.8",
    "cache-control": "no-cache",
    "connection": "keep-alive",
    "dnt": "1",
    "host": "www.qimao.com",
    "pragma": "no-cache",
    "referer": "",
    "sec-ch-ua": "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}
session = Session()
if os.path.isfile('proxies.json'):
    with open('proxies.json', 'r') as f:
        proxies = json.load(f)
    session.proxies = proxies
else:
    session.trust_env = False


def get_meta(source):
    chrome_135['referer'] = source
    cover_page = session.get(url=source, headers=chrome_135)
    if cover_page.status_code != 200:
        raise Exception(f'Fail to get the cover page. Status code: {cover_page.status_code}.')
    else:
        logging.info('Success to get the cover page.')
    cover_page.encoding = 'utf-8'
    cover_text = BeautifulSoup(cover_page.text, features='html.parser')

    match = re.search(r'/(\d+)/?$', source)
    if match is None:
        raise Exception("Book ID is not recognized, so the program cannot get the chapter list.")
    book_id = match.group(1)
    toc_page = session.get(url="https://www.qimao.com/api/book/chapter-list",
                           params={'book_id': book_id}, headers=chrome_135)
    if toc_page.status_code != 200:
        raise Exception(f'Fail to get table of content. Status code: {cover_page.status_code}.')
    else:
        logging.info('Success to get table of content.')
    toc = toc_page.json()
    try:
        toc = toc['data']['chapters']
    except KeyError:
        raise Exception(f"Fail to parse table of content.")
    vip_warning = False
    chapter_list = []
    for chapter in toc:
        if chapter.get('is_vip') != '0':
            vip_warning = True
            continue
        # intended to expose KeyError, to avoid parsing wrong page which may be long
        chapter_list.append([
            chapter['title'],
            f"https://www.qimao.com/shuku/{book_id}-{chapter['id']}/",
        ])
    if vip_warning:
        logging.warning("Some chapters are excluded from table of content, because these "
                        "chapters are only available to VIP users of qimao.com ")
    book = {
        'title': cover_text.find('div', {'class': 'title'}).find('span', {'class': 'txt'}).text.strip(),
        'author': cover_text.find('div', {'class': 'sub-title'}).find('a').text.strip(),
        'abstract': cover_text.find('div', {'class': 'qm-with-title-tb'}).text,
        'chapter_list': chapter_list,
    }
    return book


def get_chapter(source):
    chapter_page = session.get(url=source, headers=chrome_135)
    if chapter_page.status_code != 200:
        logging.warning(f'Fail to download {source}. Status code: {chapter_page.status_code}. ')
        return
    chapter_page.encoding = 'utf-8'
    chapter_text = BeautifulSoup(chapter_page.text, features='html.parser')
    chapter_title = chapter_text.find('h2', {'class': 'chapter-title'}).text
    article = chapter_text.find('div', {'class': 'article'})
    chapter_normal = "\n".join([p.text for p in article.find_all('p')])
    chapter_normal = chapter_normal.replace('\xa0', '')
    chapter_normal = re.sub('\n+', '\n\n', chapter_normal)
    chapter_normal = re.sub('<emclass=(.*?)>', '', chapter_normal)
    chapter_normal = re.sub('</?em>', '', chapter_normal)
    chapter_normal = re.sub('\n+tang\n+', '', chapter_normal)
    chapter_normal = re.sub('<\n?p>', '', chapter_normal)
    chapter = {'title': chapter_title, 'body': chapter_normal}
    return chapter
