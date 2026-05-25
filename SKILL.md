---
name: daily-policy-report
description: 生成关于中国数据、算力、网络、信息化领域的政策日报。自动通过网络搜索（DuckDuckGo + 官网抓取）收集真实政策，调用 Claude API 生成格式化日报（HTML + Word），并自动 commit 发布到 GitHub Pages。每天北京时间 06:00 自动运行。
---

# 数据和信息化政策日报 Skill v3.0

## 核心特性

- ✅ **真实搜索** - DuckDuckGo 搜索 + 政府官网抓取，不再使用硬编码内容
- ✅ **Claude AI 分析** - 调用 Anthropic API 整理、摘要、趋势判断
- ✅ **自动提交** - GitHub Actions 生成后自动 commit 回仓库
- ✅ **多格式输出** - HTML 网页版 + Word 文档版 + JSON 数据版
- ✅ **Claude Code Skill** - 可在 Claude Code 中直接调用

## 重点关注范围

### 政府层级（按优先级）
- 🏛️ 国务院 / 国务院办公厅
- 📋 国家数据局 / 工信部 / 网信办 / 发改委 / 科技部
- 🏢 省市（重点关注辽宁、江苏、上海、广东及其他）

### 政策类型
- 📊 数据管理 - 数据安全、数据流通、数据治理、数据要素
- ⚡ 算力基础设施 - 算力调度、数据中心、算电协同
- 🌐 网络相关 - 5G、物联网、边缘计算
- 🔒 网络安全 - 信息安全、等级保护、隐私保护
- 🤖 AI 相关 - 生成式 AI 监管、算法治理
- 💻 信息化建设 - 数字政府、一网通办

## 技术架构

```
requests + BeautifulSoup     → 搜索 DuckDuckGo / 抓取官网
           ↓
     Claude API (claude-opus-4-5)  → 整理分析生成 JSON
           ↓
   generate_report.py         → 输出 HTML + JSON
   generate_word_report.py    → 输出 Word 文档
           ↓
   GitHub Actions              → 自动 commit + Pages 部署
```

## 依赖

```
requests>=2.28
beautifulsoup4>=4.11
anthropic>=0.20
python-docx>=0.8.11
python-dateutil
```

## 环境变量

| 变量 | 说明 |
|------|------|
| `ANTHROPIC_API_KEY` | Anthropic API Key（必须） |

## 输出

| 文件 | 说明 |
|------|------|
| `reports/latest.json` | 结构化数据 |
| `reports/latest.html` | 网页报告 |
| `reports/latest.docx` | Word 文档 |
| `reports/report-YYYY-MM-DD.*` | 按日期存档 |

## 更新日志

**v3.0 (2026-05-25)**
- 🔄 完全重写 generate_report.py，改用真实搜索 + Claude API
- 🔄 generate_word_report.py 改为读取 JSON，不再硬编码
- 🔧 修复 GitHub Actions：加 `contents: write` 权限，增加 commit 步骤
- ✨ 新增 Claude Code Skill（`.claude/skills/daily-policy-report/SKILL.md`）

**v2.0 (2026-05-17)**
- 加入 Word 报告生成
- 优化 HTML 样式

**v1.0 (2026-05-15)**
- 初始版本
