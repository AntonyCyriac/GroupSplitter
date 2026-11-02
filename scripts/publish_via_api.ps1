# Initial upload when `git push` is blocked (e.g. corporate HTTPS filter).
# Uses GitHub REST API via `gh` — same account as `gh auth login`.
$ErrorActionPreference = "Stop"
$Repo = "AntonyCyriac/GroupSplitter"
$gh = "C:\Program Files\GitHub CLI\gh.exe"

Set-Location (Split-Path $PSScriptRoot -Parent)
$files = git ls-files
if (-not $files) { throw "No tracked files. Run from repo root after git add." }

$tree = @()
foreach ($path in $files) {
    $bytes = [System.IO.File]::ReadAllBytes((Join-Path (Get-Location) $path))
    $b64 = [Convert]::ToBase64String($bytes)
    $blob = & $gh api "repos/$Repo/git/blobs" -f content=$b64 -f encoding=base64 | ConvertFrom-Json
    $tree += @{
        path = $path -replace '\\', '/'
        mode = "100644"
        type = "blob"
        sha  = $blob.sha
    }
    Write-Host "Blob: $path"
}

$treeJson = $tree | ConvertTo-Json -Depth 5 -Compress
$treeResp = & $gh api "repos/$Repo/git/trees" -f tree=$treeJson | ConvertFrom-Json

$commitMsg = "Initial commit: GroupSplitter Windows app."
$commit = & $gh api "repos/$Repo/git/commits" -f message=$commitMsg -f tree=$treeResp.sha | ConvertFrom-Json

try {
    & $gh api "repos/$Repo/git/refs/heads/main" -X PATCH -f sha=$commit.sha | Out-Null
} catch {
    & $gh api "repos/$Repo/git/refs" -f ref="refs/heads/main" -f sha=$commit.sha | Out-Null
}

Write-Host "Published commit $($commit.sha) to https://github.com/$Repo"
