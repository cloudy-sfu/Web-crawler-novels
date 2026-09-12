# Web crawler novels

 Download and compile books from online literature websites

![](https://shields.io/badge/dependencies-Python_3.13-blue)
![](https://shields.io/badge/dependencies-XeLaTex-darkgreen)
![](https://shields.io/badge/dependencies-PowerShell_7-navy)


## Acknowledgment

[Cloudflare bypass script](https://github.com/sarperavci/CloudflareBypassForScraping)


## Install

Supported websites:

| Website                                       | Example of the book's index page             | Additional dependencies |
| --------------------------------------------- | -------------------------------------------- | ----------------------- |
| [无忧书城](https://www.51shucheng.net/)       | https://www.51shucheng.net/wangluo/huaqiangu |                         |
| [七猫小说](https://www.qm11.cc/)              | https://www.qm111.cc/book/9436/              |                         |
| [七猫中文网](https://www.qimao.com/)          | https://www.qimao.com/shuku/1761744/         |                         |
| [九九藏书网](https://www.99csw.com/index.php) | https://www.99csw.com/book/3952/136682.htm   | Google Chrome           |

Create a Python virtual environment and run the following command.

```bash
pip install -r requirements.txt
```

Ensure XeTex (Tex Live) is installed, by executing `xelatex` command in PowerShell.

Supported characters set in novel: Latin & Greek & Cyrillic & Chinese & Korean & Japanese


## Usage

Activate Python virtual environment.

In PowerShell, let the current folder be the program's root folder. Run `main.ps1` with the following arguments.

Arguments:

| Name      | Required? | Description                                                  |
| --------- | --------- | ------------------------------------------------------------ |
| `-Source` | ✓         | URL of the book's index page.                                |
| `-Name`   |           | The book name. It will be the folder name to contain the book. If the book name contain special characters, and isn't a valid folder name in the current operation system, consider a shorter and plain abbreviation name. |


### Customized usage

The program supports downloading book only. It can restart from the interrupted chapter, or from the beginning (use or invalidate table of content).

Run `python download.py -h` for more details.

```
usage: download.py [-h] [--source SOURCE] [--target TARGET] [--clear_progress] [--clear_cover]

options:
  -h, --help        show this help message and exit
  --source SOURCE   URL of the book's index page.
  --target TARGET   The book name. It will be the folder name to contain the book. If the book name contain special characters, and isn't a valid folder name in the current operation system, consider
                    a shorter and plain abbreviation name.
  --clear_progress  If set, the downloading progress of chapters will be cleared. The program will overwrite from the first chapter.
  --clear_cover     If set, the program will ignore `clear_progress` flag, get the table of contents, and clear the downloading progress of chapters, but will not delete existed chapter files.
```

Let `$target` be the path of the downloaded book.

Run the following command to create the combined Latex file from the downloaded book.

```
python export_latex.py --target $target
```

Compile Latex file to PDF twice by the following command.

```
cd $target
xelatex book.tex
xelatex book.tex
```

> [!note]
> 
> It compiles twice to fix the known problem that table of content is not correctly rendered when compiling only once.

To delete the cached chapter text, back to the program's root folder and run the following command.

```
python clear_cache.py --target $target
```


### Proxy

Save proxies config to file `proxies.json` in format of [requests proxies](https://requests.readthedocs.io/en/latest/user/advanced/#proxies).

