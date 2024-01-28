import json
import logging
import os
import pickle
from argparse import ArgumentParser

# %% Constants.
parser = ArgumentParser()
parser.add_argument('-t', '--target', type=str,
                    help='The directory to save the book.')
parser.add_argument('-l', '--log_dir', type=str,
                    default='web_crawler_novels.log',
                    help='Log file\'s name. By default "web_crawler_novels.log".')
command, _ = parser.parse_known_args()

# %% Logging.
target = os.path.abspath(command.target)
logging.basicConfig(
    filename=os.path.join(target, command.log_dir).__str__(),
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',
)

# %% Get meta latex_template
logging.info('Start to generate cover page based on meta latex_template.')
with open(os.path.join(target, 'meta.json'), 'r', encoding='utf-8') as f:
    meta = json.load(f)

# %% Generate cover page.
with open('latex_template/book_prefix.tex', 'r') as f:
    book = f.read()
book = book.replace(r'\title{}', r'\title{%s}' % meta['title']) \
    .replace(r'\author{}', r'\author{%s}' % meta['author']) \
    .replace('ABSTRACT', meta['abstract'])

# %% Generate chapters
logging.info('Start to combine chapters and format.')
with open(os.path.join(target, '.toc'), 'rb') as f:
    chapter_list = pickle.load(f)
for i in chapter_list.index:
    chapter_path = os.path.join(target, f'chapter_{i}')
    try:
        with open(chapter_path, 'r', encoding='utf-8') as g:
            book_raw = g.read()
            title, main_content = book_raw.split('\n', maxsplit=1)
            book += r'\section{' + title + '}\n'
            book += main_content
    except FileNotFoundError:
        logging.warning(f'Chapter {i} is absent. Please visit '
                        f'{chapter_list.loc[i, "link"]} and save it to {chapter_path}')
with open('latex_template/book_suffix.tex', 'r', encoding='utf-8') as f:
    book += f.read()
with open(os.path.join(target, 'book.tex'), 'w', encoding='utf-8') as f:
    f.write(book)
