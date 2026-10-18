param([switch]$Install)
$ErrorActionPreference = 'Stop'
Push-Location $PSScriptRoot
try {
    $venvPython = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
    if (-not (Test-Path -LiteralPath $venvPython)) {
        $pythonCommand = Get-Command py -ErrorAction SilentlyContinue
        if ($pythonCommand) { & $pythonCommand.Source -3 -m venv .venv }
        else {
            $pythonCommand = Get-Command python -ErrorAction SilentlyContinue
            if (-not $pythonCommand) { throw 'Please install Python 3.10 or newer first: https://www.python.org/downloads/' }
            & $pythonCommand.Source -m venv .venv
        }
        if ($LASTEXITCODE -ne 0) { throw 'Could not create Python virtual environment.' }
        $Install = $true
    }
    if ($Install) {
        & $venvPython -m pip install -r requirements.txt
        if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed. Please check your connection.' }
    }
    if (-not (Test-Path -LiteralPath 'frontend\dist\index.html')) {
        throw 'Frontend is missing. Run npm ci and npm run build in the frontend directory.'
    }
    Write-Host 'Open http://127.0.0.1:1400 in your browser. Press Ctrl+C to stop.'
    & $venvPython app.py
    if ($LASTEXITCODE -ne 0) { throw 'Application stopped with an error. See details above.' }
}
finally { Pop-Location }
