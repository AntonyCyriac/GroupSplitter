# Push GroupSplitter to GitHub (run after `gh auth login`)
# If you are on Nokia/corporate Wi‑Fi, Zscaler may block git push and API uploads.
# Use personal mobile hotspot or home network, then run this script.
$ErrorActionPreference = "Stop"

$env:Path = "C:\Users\acyriac\AppData\Local\Programs\Git\cmd;C:\Users\acyriac\AppData\Local\Programs\Git\bin;" + $env:Path
$gh = "C:\Program Files\GitHub CLI\gh.exe"
$askpass = Join-Path $PSScriptRoot "scripts\git-askpass.cmd"

Set-Location $PSScriptRoot
git remote set-url origin https://github.com/AntonyCyriac/GroupSplitter.git

& $gh auth status
& $gh auth setup-git

$env:GIT_TERMINAL_PROMPT = "0"
$env:GIT_ASKPASS = $askpass

git push -u origin main
Write-Host "Done: https://github.com/AntonyCyriac/GroupSplitter"
