import json
import logging
import re

from DrissionPage import ChromiumPage
from bs4 import BeautifulSoup

from cloudflare_bypasser import CloudflareBypasser

chrome = ChromiumPage()

def get_meta(source):
    chrome.get(source)
    cf_bypasser = CloudflareBypasser(chrome)
    cf_bypasser.bypass()

    cover_page = chrome.html
    cover_text = BeautifulSoup(cover_page, features='html.parser')
    logging.info('Success to get the cover page.')

    chapter_list = cover_text.find('ul', {'id': 'toc-list'}).find_all('li')
    chapter_list = [[x.a.text, x.a['href']] for x in chapter_list]

    for js_script in cover_text.find_all('script', {'type': 'application/ld+json'}):
        try:
            js_dict = json.loads(js_script.text)
        except json.JSONDecodeError:
            continue
        if js_dict.get("@type") == "Book":
            book = {
                "abstract": js_dict["description"],
                "title": js_dict["name"],
                "author": js_dict["author"]["name"],
                'chapter_list': chapter_list,
            }
            break
    else:
        raise Exception("Cannot find book meta data in cover page.")
    return book


def get_chapter(source):
    chrome.get(source)
    cf_bypasser = CloudflareBypasser(chrome)
    cf_bypasser.bypass()
    chapter_page = chrome.html
    chapter_text = BeautifulSoup(chapter_page, features='html.parser')
    logging.info(f"Successfully getting chapter {source}")
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
