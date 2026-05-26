# 每日政策报告自动生成脚本
# 由 Windows Task Scheduler 每天 06:00 自动调用

$ErrorActionPreference = "Stop"
$LogFile = "D:\D\lidahe2026\c-c\daily-policy-report\logs\run_$(Get-Date -Format 'yyyy-MM-dd').log"

# 确保日志目录存在
New-Item -ItemType Directory -Force "D:\D\lidahe2026\c-c\daily-policy-report\logs" | Out-Null

function Log($msg) {
    $ts = Get-Date -Format "HH:mm:ss"
    $line = "[$ts] $msg"
    Write-Host $line
    Add-Content -Path $LogFile -Value $line -Encoding UTF8
}

try {
    Log "===== 政策日报生成开始 ====="
    Set-Location "D:\D\lidahe2026\c-c\daily-policy-report"

    # 读取持久化的 Key（User 级别环境变量）
    $env:DEEPSEEK_API_KEY   = [System.Environment]::GetEnvironmentVariable("DEEPSEEK_API_KEY",   "User")
    $env:ANTHROPIC_API_KEY  = [System.Environment]::GetEnvironmentVariable("ANTHROPIC_API_KEY",  "User")
    $env:PYTHONIOENCODING   = "utf-8"

    if (-not $env:DEEPSEEK_API_KEY -and -not $env:ANTHROPIC_API_KEY) {
        throw "未找到 DEEPSEEK_API_KEY 或 ANTHROPIC_API_KEY，请先设置"
    }
    Log "API Key: OK"

    # 拉取最新代码
    Log "git pull..."
    git pull --quiet
    Log "git pull 完成"

    # 生成 HTML/JSON 报告
    Log "生成 HTML 报告..."
    python scripts/generate_report.py
    Log "HTML 报告生成完成"

    # 生成 Word 报告
    Log "生成 Word 报告..."
    python scripts/generate_word_report.py
    Log "Word 报告生成完成"

    # 提交并推送
    git add reports/
    $changed = git diff --cached --name-only
    if ($changed) {
        $date = Get-Date -Format "yyyy-MM-dd"
        git commit -m "[auto] $date 政策日报自动更新"
        git push
        Log "已提交并推送: $changed"
    } else {
        Log "无新内容，跳过提交"
    }

    Log "===== 完成 ====="
}
catch {
    Log "===== 错误: $_ ====="
    exit 1
}
