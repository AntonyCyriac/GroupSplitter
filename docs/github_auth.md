# GitHub auth notes (GroupSplitter)

## Bearer tokens

- **REST API** (`gh api`, curl): use `Authorization: Bearer YOUR_TOKEN`. The GitHub CLI does this automatically after `gh auth login`.
- **Git push over HTTPS**: GitHub does **not** accept `Authorization: Bearer` on the git upload pack. Use one of:
  - `gh auth setup-git` (recommended), or
  - HTTPS URL: `https://x-access-token:TOKEN@github.com/AntonyCyriac/GroupSplitter.git`, or
  - Username `x-access-token` and password = your PAT / `gh auth token`.

A valid token fixes **authentication** (`401` / invalid credentials). It does **not** bypass **Nokia Zscaler** when the proxy returns **403** and *"Not allowed to upload files to this site"* — that block applies no matter which auth scheme you use.

## Push when uploads are allowed

Use personal hotspot or home network, then:

```powershell
$env:Path = "C:\Users\acyriac\AppData\Local\Programs\Git\cmd;" + $env:Path
cd C:\Users\acyriac\Downloads\GroupSplitter
.\push_to_github.ps1
```

## Optional: fixed PAT in environment

Create a fine-grained PAT on GitHub with **Contents: Read and write** on `GroupSplitter`, then:

```powershell
$env:GH_TOKEN = "github_pat_...."   # do not commit this
gh auth status
git push -u origin main
```

Same Zscaler rule applies: PAT must be used from a network that allows GitHub uploads.
