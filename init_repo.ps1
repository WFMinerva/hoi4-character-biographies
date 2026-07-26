$ErrorActionPreference = "Stop"

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw "未找到Git。请先安装Git for Windows。"
}

# 首次迁移验证与日常审计分开：先证明源码没有在搬运中变化。
python .\tools\verify_initial_baseline.py
python .\tools\audit_all.py
python .\tools\build_release.py --baseline
python .\tools\verify_build.py

if (-not (Test-Path ".git")) {
    git init
    git branch -M main
}

if (-not (git rev-parse --verify HEAD 2>$null)) {
    git add .
    git commit -m "baseline: import verified v130c7 stable source and maintenance playbooks"
    git tag v130c7-stable
} else {
    Write-Host "Git仓库已有提交，未重复创建基线。"
}

Write-Host "初始化完成。当前分支："
git branch --show-current
