from requests import Session
from bs4 import BeautifulSoup
import re
import os
import pandas as pd
import time
import numpy as np
from tqdm import tqdm
from argparse import ArgumentParser
import logging

# %% Initialize constants.
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
parser = ArgumentParser()
parser.add_argument('-s', '--source', type=str, help='The index page of the book at novel website.')
parser.add_argument('-t', '--target', type=str, default='./raw/default',
                    help='The directory to save the book.')
parser.add_argument('--clear_progress', action='store_true',
                    help='If set, the downloading progress of chapters will be cleared. The program will overwrite '
                         'from the first chapter, but will not delete existed chapter files.')
parser.add_argument('--clear_cover', action='store_true',
                    help='If set, the program will ignore `clear_progress` flag, get the table of contents, and clear '
                         'the downloading progress of chapters, but will not delete existed chapter files.')
parser.add_argument('-l', '--log_dir', type=str, default='web_crawler_novel_cn.log',
                    help='Filename of the log file. By default \'web_crawler_novel_cn.log\'.')
command, _ = parser.parse_known_args()
target = os.path.abspath(command.target)
if os.path.isfile(target):
    os.remove(target)
if not os.path.isdir(target):
    os.makedirs(target, exist_ok=True)
logging.basicConfig(filename=os.path.join(command.target, command.log_dir), level=logging.INFO)
cover_path = os.path.join(target, 'index')
toc_path = os.path.join(target, '.toc')

# %% Download basic information.
with open('data/book_prefix.tex', 'r') as f:
    cover_latex = f.read()
if (not os.path.exists(cover_path)) or (not os.path.exists(toc_path)) or command.clear_cover:
    cover_page = session.get(url=command.source, headers=chrome_110)
    if cover_page.status_code != 200:
        raise Exception(f'Fail to get the cover page. Status code: {cover_page.status_code}.')
    else:
        logging.info('[INFO] Success to get the cover page.')
    cover_page.encoding = 'utf-8'
    cover_text = BeautifulSoup(cover_page.text, features='html.parser')
    if (not os.path.exists(cover_path)) or command.clear_cover:
        book_title = cover_text.find('div', {'class': 'catalog'}).h1.text
        book_author = re.sub('.*作者：', '', cover_text.find('div', {'class': 'info'}).text.strip())
        book_abstract = cover_text.find('div', {'class': 'intro'}).text
        cover_latex = cover_latex.replace(r'\title{}', r'\title{%s}' % book_title) \
            .replace(r'\author{}', r'\author{%s}' % book_author) \
            .replace('ABSTRACT', book_abstract)
        with open(cover_path, 'w', encoding='utf-8') as f:
            f.write(cover_latex)
    if (not os.path.exists(toc_path)) or command.clear_cover:
        chapter_list = cover_text.find('div', {'class': 'mulu-list'}).find_all('li')
        chapter_list = [[x.a.text, x.a['href']] for x in chapter_list]
        toc_df = pd.DataFrame(data=chapter_list, columns=['name', 'link'])
        toc_df['downloaded'] = None
        toc_df.to_pickle(toc_path)
    else:
        toc_df = pd.read_pickle(toc_path)
else:
    toc_df = pd.read_pickle(toc_path)

# %% Download chapters.
if command.clear_progress:
    toc_df['downloaded'] = None
chapters_not_downloaded = toc_df[toc_df['downloaded'].isna()].copy(deep=True)
for i, chapter in tqdm(chapters_not_downloaded.iterrows(), total=chapters_not_downloaded.shape[0]):
    chapter_path = os.path.join(target, f"chapter_{i}")
    chapter_page = session.get(url=chapter['link'], headers=chrome_110)
    if chapter_page.status_code != 200:
        toc_df.loc[i, 'downloaded'] = 1
        toc_df.to_pickle(toc_path)
        logging.warning(f'[Warning] Fail to download chapter {i}. Status code: {chapter_page.status_code}. '
                        f'Fails: {toc_df["downloaded"].sum()}/{toc_df["downloaded"].notna().sum()}. '
                        f'Please find the chapter at {chapter["link"]} and save it at {chapter_path} ')
        continue
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
    with open(chapter_path, 'w', encoding='utf-8') as f:
        f.write(r'\section{' + chapter_title + '}\n')
        f.write(chapter_normal)
    toc_df.loc[i, 'downloaded'] = 0
    toc_df.to_pickle(toc_path)
    logging.info(f'[INFO] Success to download chapter {i}. Title: {chapter_title}. '
                 f'Fails: {toc_df["downloaded"].sum()}/{toc_df["downloaded"].notna().sum()}.')
    time_sleep_sec = round(np.random.uniform(0.5, 1), 2)
    time.sleep(time_sleep_sec)

# %% Compiling
book = ''
logging.info('[INFO] Start to combine chapters into one file.')
with open(cover_path, 'r', encoding='utf-8') as g:
    book += g.read()
for i in toc_df.index:
    chapter_path = os.path.join(target, f'chapter_{i}')
    try:
        with open(chapter_path, 'r', encoding='utf-8') as g:
            book += g.read()
    except FileNotFoundError:
        logging.warning(f'[Warning] Chapter {i} is absent. Please find it at {toc_df.loc[i, "link"]} and save '
                        f'it at {chapter_path}')
with open('data/book_suffix.tex', 'r', encoding='utf-8') as f:
    book += f.read()
book_path = os.path.join(target, 'book.tex')
with open(book_path, 'w', encoding='utf-8') as f:
    f.write(book)
