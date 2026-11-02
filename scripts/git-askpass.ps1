param([string]$Prompt)
if ($Prompt -match 'Username') {
    'AntonyCyriac'
} else {
    & 'C:\Program Files\GitHub CLI\gh.exe' auth token
}
