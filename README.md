# Web crawler novels CN

 Download and compile books from some Chinese online literature websites

![](https://shields.io/badge/dependencies-Python_3.11-blue)
![](https://shields.io/badge/dependencies-XeLaTex-blue)

## Usage

Users are supposed to be familiar with $\LaTeX$ code. Because articles on web may have symbols such as `&`, `/`, which are keywords in $\LaTeX$ and users should remove them.

Supported websites:

| Website                     | Script            |
| --------------------------- | ----------------- |
| https://www.51shucheng.net/ | 51shucheng_net.py |

Usage:

1. Run `pip install -r requirements.txt`.

2. According to supported website table, choose the script. For example, to download books from https://www.51shucheng.net, choose the script name `51shucheng_net.py`. The script name in this instruction can be different after step 2 according to user's choice.

3. For example, to download https://www.51shucheng.net/wangluo/book_name to `raw/book_name`. Run

   ```
   python 51shucheng_net.py -s "https://www.51shucheng.net/wangluo/book_name" -t "raw/book_name"
   ```

4. For more usage, run
   ```
   python 51shucheng_net.py -h
   ```

5. Download [SourceHanSerifCN-Regular.ttf](https://github.com/wordshub/free-font/blob/master/assets/font/%E4%B8%AD%E6%96%87/%E6%80%9D%E6%BA%90%E5%AD%97%E4%BD%93%E7%B3%BB%E5%88%97/%E6%80%9D%E6%BA%90%E5%AE%8B%E4%BD%93/SourceHanSerifCN-Regular.ttf) to the target folder, for example `raw/book_name`.

6. Use XeLaTex to compile `raw/book_name/book.tex`. If unexpected text are in the result, modify $\LaTeX$ code to amend it.

7. When the result is as expected, run the following command to clear files other than Latex code and rendered book.
   ```
   python clear_cache.py -t "raw/book_name"
   ```
