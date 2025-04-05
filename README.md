# Web crawler novels

 Download and compile books from online literature websites

![](https://shields.io/badge/dependencies-Python_3.12-blue)
![](https://shields.io/badge/dependencies-XeLaTex-blue)

Supported websites:

| Website                                       | Example of the book's index page             | Additional dependencies |
| --------------------------------------------- | -------------------------------------------- | ----------------------- |
| [无忧书城](https://www.51shucheng.net/)       | https://www.51shucheng.net/wangluo/huaqiangu |                         |
| [七猫小说](https://www.qm11.cc/)              | https://www.qm11.cc/book/9436/               |                         |
| [七猫中文网](https://www.qimao.com/)          | https://www.qimao.com/shuku/1761744/         |                         |
| [九九藏书网](https://www.99csw.com/index.php) | https://www.99csw.com/book/3952/136682.htm   | Google Chrome           |



## Acknowledgment

[Cloudflare bypass script](https://github.com/sarperavci/CloudflareBypassForScraping)



## Install

Users are supposed to be familiar with $\LaTeX$ code. Because articles may contain [reserved words](https://en.wikipedia.org/wiki/Reserved_word) in $\LaTeX$ and will lead to compile failure, users should be able to identify and [escape](https://en.wikipedia.org/wiki/Escape_character) it.

Create a Python virtual environment and run the following command.

```
pip install -r requirements.txt
```

Install [XeLaTex](https://www.overleaf.com/learn/latex/XeLaTeX) and ensure the operation system can recognize it when calling `xelatex` in the terminal.

Download required fonts to support handling books written in corresponding character sets.

**Required fonts**

| Character set | Font                                                         |
| ------------- | ------------------------------------------------------------ |
| Latin         | (None)                                                       |
| Chinese       | [SourceHanSerifCN-Regular.ttf](https://github.com/wordshub/free-font/blob/master/assets/font/%E4%B8%AD%E6%96%87/%E6%80%9D%E6%BA%90%E5%AD%97%E4%BD%93%E7%B3%BB%E5%88%97/%E6%80%9D%E6%BA%90%E5%AE%8B%E4%BD%93/SourceHanSerifCN-Regular.ttf) |

If the the targeted book is written in multiple languages, the user must find one font that can correctly display all languages. This program doesn't support using multiple fonts.



## Usage

### Download books

Denote the book's index page is `$book_index`, the local folder to save the book is `$local`. Run the following command to download a book.

```
python main.py -s "$book_index" -t "$local"
```

For more features, run the following command.

```
python main.py -h
```

### Export to Latex

1. Run the following command.
   ```
   python export_latex.py -t "$local"
   ```

2. Proofread text in `$local/book.tex`, and amend the content manually.

3. Copy the required font to `$local`.

4. Run the following command, and review the content of `$local/book.pdf`. If table of content is missing, run again (try maximum 3 times).
   ```
   cd $local
   xelatex book.tex
   ```

5. Manually amend the content of `$local/book.tex` and repeat step 4, until the content of `$local/book.pdf` is correct.

6. Run the following command to clear files after using. The $\LaTeX$ file and the rendered book won't be deleted.

   ```
   python clear_cache.py -t "$local"
   ```

### Proxy

Save proxies config to file `proxies.json` in format of [requests proxies](https://requests.readthedocs.io/en/latest/user/advanced/#proxies).

