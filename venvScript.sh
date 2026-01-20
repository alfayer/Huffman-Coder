python -m venv .venv
.\.venv\Scripts\Activate.ps1
#控制台输入exp或者gen决定接下来运行什么命令
if ($args[0] -eq "exp") {
    pip install -r requirements.txt
} elseif ($args[0] -eq "gen") {
    pip freeze > requirements.txt
} else {
    Write-Host "Please provide a valid argument: 'exp' or 'gen'."
}
