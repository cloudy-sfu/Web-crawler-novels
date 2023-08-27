# Web crawler novels

 Download and compile books from online literature websites

![](https://shields.io/badge/dependencies-Python_3.11-blue)
![](https://shields.io/badge/dependencies-XeLaTex-blue)

## Usage

Users are supposed to be familiar with $\LaTeX$ code. Because articles on web may have symbols such as `&`, `/`, which are keywords in $\LaTeX$ and users should remove them.

Supported websites:

| Website                     | Example: index link                          |
| --------------------------- | -------------------------------------------- |
| https://www.51shucheng.net/ | https://www.51shucheng.net/wangluo/huaqiangu |

Supported fonts:

| Character set | Font                                                         |
| ------------- | ------------------------------------------------------------ |
| Latin         | already supported                                            |
| Chinese       | [SourceHanSerifCN-Regular.ttf](https://github.com/wordshub/free-font/blob/master/assets/font/%E4%B8%AD%E6%96%87/%E6%80%9D%E6%BA%90%E5%AD%97%E4%BD%93%E7%B3%BB%E5%88%97/%E6%80%9D%E6%BA%90%E5%AE%8B%E4%BD%93/SourceHanSerifCN-Regular.ttf) |

Usage:

1. Run `pip install -r requirements.txt`.

2. Find the book's index link from one of supported websites.

3. For example, to download https://www.51shucheng.net/wangluo/huaqiangu to `raw/huaqiangu`. Run

   ```
   python main.py -s "https://www.51shucheng.net/wangluo/huaqiangu" -t "raw/huaqiangu"
   ```

4. For more usage, run
   ```
   python main.py -h
   ```

5. Download one of supported fonts corresponding to the book's language, and save to the target folder, for example `raw/huaqiangu`.

6. Proofreading text in `raw/huaqiangu/book.tex`, and amend the content manually.

7. Use [XeLaTex](https://www.overleaf.com/learn/latex/XeLaTeX) to compile `raw/huaqiangu/book.tex`.

8. If the result is as expected, run the following command to clear files. Latex code and rendered book won't be affected.

   ```
   python clear_cache.py -t "raw/huaqiangu"
   ```

