# Novel Compiler

 Download and compile books from some online literature websites

![](https://shields.io/badge/dependencies-Python_3.11-blue)
![](https://shields.io/badge/dependencies-XeLaTex-blue)

## Usage

Purposed users: 

Authors and editors of the target books may add emoji, advertisements, hyperlinks in their work. They may also use special symbols to circumvent censorship on sensitive words. The generated text may unclear, and the pages of generated book may different from expected. For example, some authors like to use `&`, `/` symbols, which are conflicted to Latex command and causes compiling failures. **I assume the users are familiar with HTML and Latex code,** able to use regex to check, amend, or escape these symbols.

1. Run `pip install -r requirements.txt` to install libraries.
2. According to where to download the books, choose the proper script (referring to "supported websites" table). The scripts support pausing at any time by pressing `Ctrl+C` (default keyboard interruption signal), and resuming at next run.<br>
   *The behaviors are controlled by arguments `clear_progress` and `clear_cover`.*
3. Download [SourceHanSerifCN-Regular.ttf](https://github.com/wordshub/free-font/blob/master/assets/font/%E4%B8%AD%E6%96%87/%E6%80%9D%E6%BA%90%E5%AD%97%E4%BD%93%E7%B3%BB%E5%88%97/%E6%80%9D%E6%BA%90%E5%AE%8B%E4%BD%93/SourceHanSerifCN-Regular.ttf) to `$target`. <br>
   *It refers to the value of argument `target`.* 
4. The source code of the book is saved at `$target/book.tex`. Use `XeLaTex` to compile it.
5. If satisfied with the result, run `clear_cache.py` to clear files other than Latex code and rendered book.

Supported websites:

| Website                     | Script            |
| --------------------------- | ----------------- |
| https://www.51shucheng.net/ | 51shucheng_net.py |

