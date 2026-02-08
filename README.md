# Web crawler novels

 Download and compile books from online literature websites

![](https://shields.io/badge/dependencies-Python_3.13-blue)
![](https://shields.io/badge/dependencies-XeLaTex-blue)



## Acknowledgment

[Cloudflare bypass script](https://github.com/sarperavci/CloudflareBypassForScraping)



## Install

Supported websites:

| Website                                       | Example of the book's index page             | Additional dependencies |
| --------------------------------------------- | -------------------------------------------- | ----------------------- |
| [无忧书城](https://www.51shucheng.net/)       | https://www.51shucheng.net/wangluo/huaqiangu |                         |
| [七猫小说](https://www.qm11.cc/)              | https://www.qm11.cc/book/9436/               |                         |
| [七猫中文网](https://www.qimao.com/)          | https://www.qimao.com/shuku/1761744/         |                         |
| [九九藏书网](https://www.99csw.com/index.php) | https://www.99csw.com/book/3952/136682.htm   | Google Chrome           |

Create a Python virtual environment and run the following command.

```bash
pip install -r requirements.txt
```

Type `xelatex` in terminal and watch the output to confirm XeTex (Tex Live) is installed. If not, follow the instructions below.

---

Install R language from https://cran.r-project.org/

Run the following command in R.

```R
install.packages('tinytex')
tinytex::install_tinytex()
```

To uninstall in the future, run the following command in R.

```R
tinytex::uninstall_tinytex()
```

Type `xelatex` in terminal to confirm the installation is successful.

---

Supported characters set in novel: Latin & Greek & Cyrillic & Chinese & Korean & Japanese



## Usage

### Basic usage

![](https://shields.io/badge/OS-Windows-navy)
![](https://shields.io/badge/dependencies-PowerShell_7-skyblue)

Activate Python virtual environment.

Run the following command in PowerShell with arguments.

Script:

```
.\main.ps1
```

Arguments:

| Name      | Description                                                  | Required? |
| --------- | ------------------------------------------------------------ | --------- |
| `-Source` | URL of the book's index page.                                | Yes       |
| `-Name`   | The book name. It will be the folder name to contain the book. If the book name contain special characters, and isn't a valid folder name in the current operation system, consider a shorter and plain abbreviation name. |           |



### Interrupted Downloads

The program supports downloading book only. It can restart from the interrupted chapter, or from the beginning (use or invalidate  table of content).

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

When the book is downloaded to `$target` folder, run the following command to create the combined Latex file.

```
python export_latex.py --target $target
```

Compile Latex file to PDF twice by the following command.

```
cd $target
xelatex book.tex
xelatex book.tex
```

To clear the cached chapter text, back to the program's root folder and run the following command.

```
python clear_cache.py --target $target
```



### Proxy

Save proxies config to file `proxies.json` in format of [requests proxies](https://requests.readthedocs.io/en/latest/user/advanced/#proxies).

