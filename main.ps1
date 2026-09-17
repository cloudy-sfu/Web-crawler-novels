[CmdletBinding()]
param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$Source,
    [Parameter(Mandatory=$true, Position=1)]
    [string]$Name
)

$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $true

& .\Tinytex-installer\install.ps1
tlmgr install ctex amsmath amsfonts fontspec xcolor xurl hyperref bookmark xecjk

if (-not (Test-Path -Path "./latex_template/SourceHanSerifCN-Regular.ttf" -PathType Leaf)) {
    curl --create-dirs -o "./latex_template/SourceHanSerifCN-Regular.ttf" "https://raw.githubusercontent.com/wordshub/free-font/refs/heads/master/assets/font/%E4%B8%AD%E6%96%87/%E6%80%9D%E6%BA%90%E5%AD%97%E4%BD%93%E7%B3%BB%E5%88%97/%E6%80%9D%E6%BA%90%E5%AE%8B%E4%BD%93/SourceHanSerifCN-Regular.ttf"
}
python download.py --source $Source --target $Name
python export_latex.py --target $Name
cp "./latex_template/SourceHanSerifCN-Regular.ttf" "$Name/SourceHanSerifCN-Regular.ttf"

Push-Location $Name
xelatex book.tex
xelatex book.tex

Pop-Location
python clear_cache.py --target $Name
