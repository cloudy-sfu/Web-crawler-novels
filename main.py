import json
import logging
import os
import random
import time
from argparse import ArgumentParser
from urllib.parse import urlparse
import pandas as pd
from tqdm import tqdm

# %% Parse arguments.
parser = ArgumentParser()
parser.add_argument('-s', '--source', type=str,
                    help='The index page of the book at novel website.')
parser.add_argument('-t', '--target', type=str,
                    help='The directory to save the book.')
parser.add_argument('--clear_progress', action='store_true',
                    help='If set, the downloading progress of chapters will be cleared. '
                         'The program will overwrite from the first chapter.')
parser.add_argument('--clear_cover', action='store_true',
                    help='If set, the program will ignore `clear_progress` flag, get the '
                         'table of contents, and clear the downloading progress of '
                         'chapters, but will not delete existed chapter files.')
parser.add_argument('-l', '--log_dir', type=str,
                    default='web_crawler_novels.log',
                    help='Log file\'s name. By default "web_crawler_novels.log".')
command, _ = parser.parse_known_args()

# %% Initialize constants.
target = os.path.abspath(command.target)
if os.path.isfile(target):
    os.remove(target)
os.makedirs(target, exist_ok=True)
meta_path = os.path.join(target, 'meta.json')
toc_path = os.path.join(target, '.toc')
logging.basicConfig(
    filename=os.path.join(command.target, command.log_dir).__str__(),
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',
)

# %% Choose download script.
url_schema = urlparse(command.source)
downloader_dict = {  # hostname -> module name
    '51shucheng.net': 'web_51shucheng_net',
    'qmxs123.com': 'web_qmxs123_com'
}
for hostname, module_name in downloader_dict.items():
    if url_schema.hostname.endswith(hostname):
        downloader = __import__(module_name)
        break
else:
    raise logging.error(f'Cannot find a downloader for domain {url_schema.hostname}')

# %% Download basic information.
if command.clear_cover or (not os.path.isfile(meta_path)):
    meta = downloader.get_meta(command.source)
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(meta, f, indent=4, ensure_ascii=False)

if command.clear_cover or (not os.path.isfile(toc_path)):
    with open(meta_path, 'r', encoding='utf-8') as f:
        meta = json.load(f)
    chapter_list = pd.DataFrame(data=meta['chapter_list'], columns=['name', 'link'])
    chapter_list['downloaded'] = None
    chapter_list.to_pickle(toc_path)
else:
    chapter_list = pd.read_pickle(toc_path)

# %% Download chapters.
if command.clear_progress:
    chapter_list['downloaded'] = None
chapters_not_downloaded = chapter_list[chapter_list['downloaded'].isna()].copy(deep=True)
for i, chapter in tqdm(chapters_not_downloaded.iterrows(),
                       total=chapters_not_downloaded.shape[0]):
    chapter_path = os.path.join(target, f"chapter_{i}")
    chapter = downloader.get_chapter(chapter['link'])
    if not chapter:
        chapter_list.loc[i, 'downloaded'] = 1
        chapter_list.to_pickle(toc_path)
        logging.warning(f'Current chapter {i}. Total fails: '
                        f'{chapter_list["downloaded"].sum()}/'
                        f'{chapter_list["downloaded"].notna().sum()}. Please manually '
                        f'download the chapter and save at {chapter_path}')
    with open(chapter_path, 'w', encoding='utf-8') as f:
        f.write(chapter['title'] + '\n')
        f.write(chapter['body'])
    chapter_list.loc[i, 'downloaded'] = 0
    chapter_list.to_pickle(toc_path)
    logging.info(f'Success to download chapter {i}. Title: {chapter["title"]}.')
    time_sleep_sec = round(random.uniform(0.5, 1), 2)
    time.sleep(time_sleep_sec)
