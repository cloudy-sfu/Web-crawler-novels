import json
import logging
import os
import random
import sys
import time
from argparse import ArgumentParser
from urllib.parse import urlparse
import importlib

import pandas as pd
from tqdm import tqdm


def handle_exception(exc_type, exc_value, exc_traceback):
    sys.__excepthook__(exc_type, exc_value, exc_traceback)
    sys.exit(1)


sys.excepthook = handle_exception

# %% Parse arguments.
parser = ArgumentParser()
parser.add_argument(
    '--source', type=str, help='URL of the book\'s index page.')
parser.add_argument(
    '--target', type=str,
    help='The book name. It will be the folder name to contain the book. If the book '
         'name contain special characters, and isn\'t a valid folder name in the current '
         'operation system, consider a shorter and plain abbreviation name.')
parser.add_argument(
    '--clear_progress', action='store_true',
    help='If set, the downloading progress of chapters will be cleared. The program will '
         'overwrite from the first chapter.')
parser.add_argument(
    '--clear_cover', action='store_true',
    help='If set, the program will ignore `clear_progress` flag, get the table of '
         'contents, and clear the downloading progress of chapters, but will not delete '
         'existed chapter files.')
cmd, _ = parser.parse_known_args()

target = os.path.abspath(cmd.target)
if os.path.isfile(target):
    os.remove(target)
os.makedirs(target, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(cmd.target, "download_log.txt").__str__(),
    level=logging.INFO,
    format="[%(levelname)s] %(message)s",
)
meta_path = os.path.join(target, 'meta.json')
toc_path = os.path.join(target, '.toc')

# %% Choose download script.
url_schema = urlparse(cmd.source)
downloader_dict = {
    # hostname -> module name
    '51shucheng.net': 'web_51shucheng_net',
    'qm11.cc': 'web_qmxs123_com',
    '99csw.com': 'web_99csw_com',
    'qimao.com': 'web_qimao_com',
}
for hostname, module_name in downloader_dict.items():
    if url_schema.hostname.endswith(hostname):
        downloader = importlib.import_module(f'crawlers.{module_name}')
        break
else:
    raise logging.error(f'Cannot find a downloader for domain {url_schema.hostname}')

# %% Download basic information.
if cmd.clear_cover or (not os.path.isfile(meta_path)):
    meta = downloader.get_meta(cmd.source)
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(meta, f, indent=4, ensure_ascii=False)

if cmd.clear_cover or (not os.path.isfile(toc_path)):
    with open(meta_path, 'r', encoding='utf-8') as f:
        meta = json.load(f)
    chapter_list = pd.DataFrame(data=meta['chapter_list'], columns=['name', 'link'])
    chapter_list['downloaded'] = None
    chapter_list.to_pickle(toc_path)
else:
    chapter_list = pd.read_pickle(toc_path)

# %% Download chapters.
if cmd.clear_progress:
    chapter_list['downloaded'] = None
chapters_not_downloaded = chapter_list[chapter_list['downloaded'].isna()].copy(deep=True)
for i, chapter in tqdm(chapters_not_downloaded.iterrows(),
                       total=chapters_not_downloaded.shape[0]):
    chapter_path = os.path.join(target, f"chapter_{i}.json")
    chapter = downloader.get_chapter(chapter['link'])
    if not chapter:
        chapter_list.loc[i, 'downloaded'] = 1
        chapter_list.to_pickle(toc_path)
        logging.warning(f'Current chapter {i}. Total fails: '
                        f'{chapter_list["downloaded"].sum()}/'
                        f'{chapter_list["downloaded"].notna().sum()}. Please manually '
                        f'download the chapter and save at {chapter_path}')
    with open(chapter_path, 'w', encoding='utf-8') as f:
        json.dump(chapter, f, ensure_ascii=False)
    chapter_list.loc[i, 'downloaded'] = 0
    chapter_list.to_pickle(toc_path)
    logging.info(f'Success to download chapter {i}. Title: {chapter["title"]}.')
    time_sleep_sec = round(random.uniform(0.5, 1), 2)
    time.sleep(time_sleep_sec)
