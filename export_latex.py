import json
import logging
import os
import pickle
import re
from argparse import ArgumentParser


def tex_escape(text):
    """
    :param text: a plain text message
    :return: the message escaped to appear correctly in LaTeX
    """
    conv = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
        '\\': r'\textbackslash{}',
        '<': r'\textless{}',
        '>': r'\textgreater{}',
    }
    regex = re.compile('|'.join(
        re.escape(str(key))
        for key in sorted(conv.keys(), key=lambda item: -len(item))
    ))
    return regex.sub(lambda match: conv[match.group()], text)


# Usage
raw_text = "Earnings increased by 20% & margin is ~5 points. Use code: \\variable_{x}"
print(tex_escape(raw_text))

# %% Constants.
parser = ArgumentParser()
parser.add_argument('--target', type=str,
                    help='The directory to save the book.')
cmd, _ = parser.parse_known_args()

# %% Logging.
target = os.path.abspath(cmd.target)
logging.basicConfig(
    filename=os.path.join(cmd.target, "export_latex_log.txt").__str__(),
    level=logging.INFO,
    format="[%(levelname)s] %(message)s",
)

# %% Get meta latex_template
logging.info('Start to generate cover page based on meta latex_template.')
with open(os.path.join(target, 'meta.json'), 'r', encoding='utf-8') as f:
    meta = json.load(f)

# %% Generate cover page.
with open('latex_template/book_prefix.tex', 'r') as f:
    book = f.read()
abstract_gap_lines = re.sub(r'(?<!\n)\n(?!\n)', '\n\n', meta['abstract'])
book = book.replace(r'\title{}', r'\title{%s}' % meta['title']) \
    .replace(r'\author{}', r'\author{%s}' % meta['author']) \
    .replace('ABSTRACT', abstract_gap_lines)

# %% Generate chapters
logging.info('Start to combine chapters and format.')
with open(os.path.join(target, '.toc'), 'rb') as f:
    chapter_list = pickle.load(f)
for i in chapter_list.index:
    chapter_path = os.path.join(target, f'chapter_{i}.json')
    try:
        with open(chapter_path, 'r') as g:
            chapter = json.load(g)
        book += (r'\section{' +
                 re.sub(r"\s", '~', tex_escape(chapter['title']))
                 + '}\n')
        main_content_gap_lines = re.sub(
            r'(?<!\n)\n(?!\n)', '\n\n', tex_escape(chapter['body']))
        book += main_content_gap_lines + "\n\n"
    except FileNotFoundError:
        logging.warning(f'Chapter {i} is absent. Please visit '
                        f'{chapter_list.loc[i, "link"]} and save it to {chapter_path}')
with open('latex_template/book_suffix.tex', 'r', encoding='utf-8') as f:
    book += f.read()
with open(os.path.join(target, 'book.tex'), 'w', encoding='utf-8') as f:
    f.write(book)
