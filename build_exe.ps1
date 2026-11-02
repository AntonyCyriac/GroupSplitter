# Build GroupSplitter.exe (Windows)
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

function Get-PythonExe {
    $candidates = @(
        "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe"
    )
    foreach ($c in $candidates) {
        if (Test-Path $c) { return $c }
    }
    try {
        $out = & python -c "import sys; print(sys.executable)" 2>$null
        if ($LASTEXITCODE -eq 0 -and $out) { return $out.Trim() }
    } catch {}
    return $null
}

$python = Get-PythonExe
if (-not $python) {
    throw "Python not found. Install Python 3.12+ or add it to PATH."
}

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    & $python -m venv .venv
}

& .\.venv\Scripts\pip.exe install -r requirements.txt -q
& .\.venv\Scripts\pyinstaller.exe `
    --name GroupSplitter `
    --windowed `
    --onefile `
    --paths . `
    app/main.py

Write-Host "Built: dist\GroupSplitter.exe"
