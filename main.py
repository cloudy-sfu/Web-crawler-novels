import os
import pandas as pd
import time
import numpy as np
from tqdm import tqdm
from argparse import ArgumentParser
import logging
from urllib.parse import urlparse

# %% Parse arguments.
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

# %% Initialize constants.
target = os.path.abspath(command.target)
if os.path.isfile(target):
    os.remove(target)
if not os.path.isdir(target):
    os.makedirs(target, exist_ok=True)
cover_path = os.path.join(target, 'index')
toc_path = os.path.join(target, '.toc')
with open('data/book_prefix.tex', 'r') as f:
    cover_latex = f.read()
logging.basicConfig(filename=os.path.join(command.target, command.log_dir), level=logging.INFO)

# %% Choose download script.
url_schema = urlparse(command.source)
downloader_dict = {  # hostname -> module name
    '51shucheng.net': '51shucheng_net',
    'qmxs123.com': 'qmxs123_com'
}
for hostname, module_name in downloader_dict.items():
    if url_schema.hostname.endswith(hostname):
        downloader = __import__(module_name)
        break
else:
    raise Exception(f'[Error] Cannot find a downloader for domain {url_schema.hostname}')

# %% Download basic information.
if command.clear_cover or (not os.path.isfile(cover_path)) or (not os.path.isfile(toc_path)):
    meta = downloader.get_meta(command.source)
    cover_latex = cover_latex.replace(r'\title{}', r'\title{%s}' % meta['title']) \
        .replace(r'\author{}', r'\author{%s}' % meta['author']) \
        .replace('ABSTRACT', meta['abstract'])
    with open(cover_path, 'w', encoding='utf-8') as f:
        f.write(cover_latex)
    chapter_list = pd.DataFrame(data=meta['chapter_list'], columns=['name', 'link'])
    chapter_list['downloaded'] = None
    chapter_list.to_pickle(toc_path)
else:
    chapter_list = pd.read_pickle(toc_path)

# %% Download chapters.
if command.clear_progress:
    chapter_list['downloaded'] = None
chapters_not_downloaded = chapter_list[chapter_list['downloaded'].isna()].copy(deep=True)
for i, chapter in tqdm(chapters_not_downloaded.iterrows(), total=chapters_not_downloaded.shape[0]):
    chapter_path = os.path.join(target, f"chapter_{i}")
    chapter = downloader.get_chapter(chapter['link'])
    if not chapter:
        chapter_list.loc[i, 'downloaded'] = 1
        chapter_list.to_pickle(toc_path)
        logging.warning(f'[Warning] Current chapter {i}. Total fails: '
              f'{chapter_list["downloaded"].sum()}/{chapter_list["downloaded"].notna().sum()}. '
              f'Please manually download the chapter and save it at {chapter_path} ')
    with open(chapter_path, 'w', encoding='utf-8') as f:
        f.write(r'\section{' + chapter['title'] + '}\n')
        f.write(chapter['body'])
    chapter_list.loc[i, 'downloaded'] = 0
    chapter_list.to_pickle(toc_path)
    # logging.info(f'[INFO] Success to download chapter {i}. Title: {chapter['title']}.‘)
    time_sleep_sec = round(np.random.uniform(0.5, 1), 2)
    time.sleep(time_sleep_sec)

# %% Compiling
book = ''
logging.info('[INFO] Start to combine chapters into one file.')
with open(cover_path, 'r', encoding='utf-8') as g:
    book += g.read()
for i in chapter_list.index:
    chapter_path = os.path.join(target, f'chapter_{i}')
    try:
        with open(chapter_path, 'r', encoding='utf-8') as g:
            book += g.read()
    except FileNotFoundError:
        logging.warning(f'[Warning] Chapter {i} is absent. Please visit {chapter_list.loc[i, "link"]} and save to '
                        f'{chapter_path}')
with open('data/book_suffix.tex', 'r', encoding='utf-8') as f:
    book += f.read()
book_path = os.path.join(target, 'book.tex')
with open(book_path, 'w', encoding='utf-8') as f:
    f.write(book)
