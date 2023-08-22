import os
import pandas as pd
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('-t', '--target', type=str, default='./raw/default',
                    help='The directory to save the book.')
command, _ = parser.parse_known_args()

# %% Load TOC file.
target = os.path.abspath(command.target)
cover_path = os.path.join(target, 'index')
toc_path = os.path.join(target, '.toc')
toc_df = pd.read_pickle(toc_path)

# %% Delete cached files.
for i in toc_df.index:
    try:
        chapter_path = os.path.join(target, f'chapter_{i}')
        os.remove(chapter_path)
    except FileExistsError:
        pass
try:
    os.remove(toc_path)
except FileExistsError:
    pass
try:
    os.remove(cover_path)
except FileExistsError:
    pass
