# Web crawler novels

 Download and compile books from online literature websites

![](https://shields.io/badge/dependencies-Python_3.11-blue?style=flat-square)
![](https://shields.io/badge/dependencies-XeLaTex-blue?style=flat-square)

## Usage

Users are supposed to be familiar with $\LaTeX$ code. Because articles may contain [reserved words](https://en.wikipedia.org/wiki/Reserved_word) in $\LaTeX$ and will lead to compile failure, users should be able to identify and [escape](https://en.wikipedia.org/wiki/Escape_character) it.

Supported websites:

| Website                     | Example index                                |
| --------------------------- | -------------------------------------------- |
| https://www.51shucheng.net/ | https://www.51shucheng.net/wangluo/huaqiangu |
| https://www.qmxs123.com/    | https://www.qmxs123.com/book/9436/           |

Supported fonts:

| Character set | Font                                                         |
| ------------- | ------------------------------------------------------------ |
| Latin         | already supported                                            |
| Chinese       | [SourceHanSerifCN-Regular.ttf](https://github.com/wordshub/free-font/blob/master/assets/font/%E4%B8%AD%E6%96%87/%E6%80%9D%E6%BA%90%E5%AD%97%E4%BD%93%E7%B3%BB%E5%88%97/%E6%80%9D%E6%BA%90%E5%AE%8B%E4%BD%93/SourceHanSerifCN-Regular.ttf) |

Example: download https://www.51shucheng.net/wangluo/huaqiangu to `raw/huaqiangu` and make a PDF document.

1. Run `pip install -r requirements.txt`.

2. Run the following command.

   ```
   python main.py -s "https://www.51shucheng.net/wangluo/huaqiangu" -t "raw/huaqiangu"
   ```

3. For more usage, run the following command.
   ```
   python main.py -h
   ```

4. Because this book is in Chinese, download [SourceHanSerifCN-Regular.ttf](https://github.com/wordshub/free-font/blob/master/assets/font/%E4%B8%AD%E6%96%87/%E6%80%9D%E6%BA%90%E5%AD%97%E4%BD%93%E7%B3%BB%E5%88%97/%E6%80%9D%E6%BA%90%E5%AE%8B%E4%BD%93/SourceHanSerifCN-Regular.ttf) to `raw/huaqiangu`.

5. Proofread text in `raw/huaqiangu/book.tex`, and amend the content manually.

6. Use [XeLaTex](https://www.overleaf.com/learn/latex/XeLaTeX) to compile TEX file.
   ```
   cd raw/huaqiangu/
   xelatex book.tex
   xelatex book.tex  # necessary to run twice due to xelatex's bug
   ```

7. If the result is as expected, run the following command to clear files. Latex code and rendered book won't be affected.

   ```
   python clear_cache.py -t "raw/huaqiangu"
   ```

