import logging
import time

from DrissionPage import ChromiumPage
from bs4 import BeautifulSoup, NavigableString

from cloudflare_bypasser import CloudflareBypasser

base_url = "https://www.99csw.com/"
chrome = ChromiumPage()


def get_meta(source):
    chrome.get(source)
    cf_bypasser = CloudflareBypasser(chrome)
    cf_bypasser.bypass()
    cover_page = chrome.html
    logging.info('Success to get the cover page.')
    cover_text = BeautifulSoup(cover_page, features='html.parser')
    chapter_list = cover_text.find('dl', {'id': 'dir'})
    dt = None
    chapter_list_1 = []
    for label in chapter_list.children:
        if label.name == "dt":
            dt = label.text
        elif label.name == "dd":
            link = label.a
            if dt:
                chapter_list_1.append([f"{dt}: {link.text}", base_url + link['href']])
            else:
                chapter_list_1.append([link.text, base_url + link['href']])
    book = {
        'title': cover_text.find('div', {'id': 'book_info'}).h2.text,
        'author': cover_text.find('dl', {'id': 'author_box'}).h4.text,
        'abstract': cover_text.find('div', {'class': 'intro'}).text,
        'chapter_list': chapter_list_1,
    }
    return book


def get_chapter(source):
    try:
        chrome.get(source)
        cf_bypasser = CloudflareBypasser(chrome)
        cf_bypasser.bypass()
        last_height = 0
        while True:
            chrome.run_js("window.scrollTo(0, document.body.scrollHeight);")
            current_height = chrome.run_js("document.body.scrollHeight", as_expr=True)
            if current_height > last_height:
                last_height = current_height
                time.sleep(0.4)
            else:
                break
        chapter_page = chrome.html
    except Exception as e:
        logging.warning(f'Fail to download {source}. Error: {e}.')
        return
    chapter_text = BeautifulSoup(chapter_page, features='html.parser')
    chapter_text = chapter_text.find("div", {"id": "content"})

    chapter_title = [line.text for line in chapter_text.find_all("h2")]
    chapter_title = "~~".join(chapter_title)
    paragraph_list = chapter_text.find_all("div", {"class": True})
    paragraph_list_1 = []
    for i, paragraph in enumerate(paragraph_list):
        if i % 6 == 0:
            paragraph_text = "".join([
                text for text in paragraph.contents if isinstance(text, NavigableString)
            ])
            paragraph_text = paragraph_text.strip()
            paragraph_list_1.append(paragraph_text)
    chapter_normal = "\n\n".join(paragraph_list_1)
    chapter_normal += "\n\n"
    chapter = {'title': chapter_title, 'body': chapter_normal}
    return chapter
