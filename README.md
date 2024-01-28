# Web crawler novels

 Download and compile books from online literature websites

![](https://shields.io/badge/dependencies-Python_3.11-blue?style=flat-square)
![](https://shields.io/badge/dependencies-XeLaTex-blue?style=flat-square)

## Usage

### Download books

Supported websites:

| Website                     | Example index                                |
| --------------------------- | -------------------------------------------- |
| https://www.51shucheng.net/ | https://www.51shucheng.net/wangluo/huaqiangu |
| https://www.qmxs123.com/    | https://www.qmxs123.com/book/9436/           |

1. Run the following command before the first time of using this program.
    ```
    pip install -r requirements.txt
    ```

2. Run the following command to download a book. Denote the book source is https://example.com/book_name and the target directory is `raw/book_name`.
   ```
   python main.py -s "https://example.com/book_name" -t "raw/book_name"
   ```
   
3. For more detailed usage, run the following command.
   ```
   python main.py -h
   ```

### Export to Latex

Users are supposed to be familiar with $\LaTeX$ code. Because articles may contain [reserved words](https://en.wikipedia.org/wiki/Reserved_word) in $\LaTeX$ and will lead to compile failure, users should be able to identify and [escape](https://en.wikipedia.org/wiki/Escape_character) it.

**Required fonts**

| Character set | Font                                                         |
| ------------- | ------------------------------------------------------------ |
| Latin         |                                                              |
| Chinese       | [SourceHanSerifCN-Regular.ttf](https://github.com/wordshub/free-font/blob/master/assets/font/%E4%B8%AD%E6%96%87/%E6%80%9D%E6%BA%90%E5%AD%97%E4%BD%93%E7%B3%BB%E5%88%97/%E6%80%9D%E6%BA%90%E5%AE%8B%E4%BD%93/SourceHanSerifCN-Regular.ttf) |

1. Run the following command.
   ```
   python export_latex.py -t "raw/book_name"
   ```

2. Proofread text in `raw/book_name/book.tex`, and amend the content manually.

3. Because this book is in Chinese, so we need Chinese font. Look up the table "required fonts". The required font is [SourceHanSerifCN-Regular.ttf](https://github.com/wordshub/free-font/blob/master/assets/font/%E4%B8%AD%E6%96%87/%E6%80%9D%E6%BA%90%E5%AD%97%E4%BD%93%E7%B3%BB%E5%88%97/%E6%80%9D%E6%BA%90%E5%AE%8B%E4%BD%93/SourceHanSerifCN-Regular.ttf), so save it into `raw/book_name`.

4. Use [XeLaTex](https://www.overleaf.com/learn/latex/XeLaTeX) to compile TEX file. If table of content is missing, run again. (Maximum trial 3 times)
   ```
   cd raw/book_name
   xelatex book.tex
   ```

5. If the result is correct, `cd` back to the program root directory.

6. Run the following command to clear files after using. Latex code and rendered book won't be deleted.

   ```
   python clear_cache.py -t "raw/book_name"
   ```

