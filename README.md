# GroupSplitter

Windows desktop app to split a list of names (e.g. parish families) into **M** random, **balanced** groups and export **one PDF per group**.

## What you need

- **Input:** One of **CSV**, **TSV**, **TXT**, or **Excel (.xlsx)** with family names in the **first column** (one family per row). For **.txt**, use one name per line. A header row such as `Family Name` is detected automatically.
- **Settings:** Number of groups **M** (default 4).
- **Output:** `Group_1.pdf` … `Group_M.pdf` in the folder you choose. Each list is numbered (1, 2, 3, …).

When you click **Generate PDFs**, a **10 → 0 countdown** runs first (one second per step), then a progress window shows each family assigned to a group (~4 seconds), then counts through each PDF as it is saved.

## Run from source (developers)

```powershell
cd GroupSplitter
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app/main.py
```

## Build standalone `.exe`

```powershell
.\build_exe.ps1
```

The executable is under `dist\GroupSplitter.exe` (one-file build).

Windows may show SmartScreen for unsigned apps; that is normal unless the exe is code-signed.

## Input file tips

| Format | Notes |
|--------|--------|
| **.csv** | Comma-separated; first column = family name |
| **.tsv** | Tab-separated |
| **.txt** | One family name per line |
| **.xlsx** | Open in Excel; names in column A (first sheet) |

- Extra columns are ignored (only the first column is used).
- Empty rows/lines are skipped.
- Legacy **.xls** is not supported; save as **.xlsx** in Excel.

## Sample data

Try [`sample_data/families_sample.csv`](sample_data/families_sample.csv) with **M = 4** before using your full list.

## Tests

```powershell
python -m unittest discover -s tests -v
python tests/smoke_test.py
```

## CI/CD and releases

GitHub Actions runs on this repository:

| Workflow | When | What it does |
|----------|------|----------------|
| **CI** (`.github/workflows/ci.yml`) | Push or pull request to `master` / `main` | Unit tests and smoke test on Windows and Ubuntu, then builds `GroupSplitter.exe` and uploads it as a workflow artifact |
| **Release** (`.github/workflows/release.yml`) | Push of a tag matching `v*` (for example `v1.0.0`) | Re-runs tests, builds the Windows exe, and publishes it on a GitHub Release |

Create a versioned release:

```powershell
git tag v1.0.0
git push origin v1.0.0
```

The release includes `GroupSplitter.exe` and `GroupSplitter-v1.0.0-windows.exe`. You can also run **Release** from the Actions tab to test the Windows build without publishing; that run uploads the exe as a workflow artifact only.

## Author

[AntonyCyriac](https://github.com/AntonyCyriac)

## Publish to GitHub

Repo: [github.com/AntonyCyriac/GroupSplitter](https://github.com/AntonyCyriac/GroupSplitter)

From a network that allows GitHub (not blocked by corporate proxy):

```powershell
$env:Path = "C:\Users\acyriac\AppData\Local\Programs\Git\cmd;" + $env:Path
cd C:\Users\acyriac\Downloads\GroupSplitter
.\push_to_github.ps1
```

If `git` is not found, add Git’s `cmd` folder to your user **PATH**, or use the full path to `git.exe`.
