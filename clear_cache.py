import os
from argparse import ArgumentParser

import pandas as pd

parser = ArgumentParser()
parser.add_argument('--target', type=str,
                    help='The directory to save the book.')
cmd, _ = parser.parse_known_args()

target = os.path.abspath(cmd.target)

toc_path = os.path.join(target, '.toc')
try:
    toc_df = pd.read_pickle(toc_path)
except FileNotFoundError:
    pass
else:
    for i in toc_df.index:
        try:
            chapter_path = os.path.join(target, f'chapter_{i}.json')
            os.remove(chapter_path)
        except FileNotFoundError:
            pass

for item in [
    '.toc',
    'meta.json',
    'book.aux',
    'book.toc',
    'book.log',
    'download_log.txt',
    'export_latex_log.txt',
]:
    try:
        item_path = os.path.join(target, item)
        os.remove(item_path)
    except FileNotFoundError:
        pass
