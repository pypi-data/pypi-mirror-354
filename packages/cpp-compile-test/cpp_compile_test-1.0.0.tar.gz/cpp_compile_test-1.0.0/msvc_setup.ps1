param (
    [string]$VcVarsPath = "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat"
)

if (-not (Test-Path $VcVarsPath)) {
    Write-Error "vcvars64.bat not found at: $VcVarsPath"
    exit 1
}

$tempFile = Join-Path $env:TEMP "vcvars_env.txt"

# Call vcvars and dump the environment to a temp file
$cmd = "call `"$VcVarsPath`" && set > `"$tempFile`""
cmd.exe /c $cmd

if (-not (Test-Path $tempFile)) {
    Write-Error "Failed to create environment dump: $tempFile"
    exit 1
}

# Import environment variables
Get-Content $tempFile | ForEach-Object {
    if ($_ -match "^(.*?)=(.*)$") {
        try {
            Set-Content -Path "env:\$($matches[1])" -Value $matches[2]
        } catch {
            Write-Warning "Failed to import: $($_)"
        }
    }
}

Write-Host "`n MSVC environment loaded successfully from:`n  $VcVarsPath" -ForegroundColor Green
