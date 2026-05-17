# 🚀 快速启动指南

## 3 个功能：一键完成

✅ **1. Word 文档生成**  
✅ **2. Skill 打包**  
✅ **3. 每日自动发布到网站**

---

## 安装前准备

### 所需工具
```bash
# 检查 Python 版本
python --version  # 需要 3.8+

# 检查 Git
git --version
```

### 安装依赖
```bash
pip install python-docx requests beautifulsoup4 python-dateutil
```

---

## 5 分钟快速部署

### 步骤 1：在 GitHub 创建仓库

1. 访问 [GitHub](https://github.com)
2. 点击 `+` → `New repository`
3. 名称：`daily-policy-report`
4. 选择 `Public`
5. 创建

### 步骤 2：上传代码

```bash
cd D:\D\lidahe2026\c-c\daily-policy-report

# 初始化 Git
git init
git add .
git commit -m "初始化项目"

# 连接到 GitHub（替换 你的用户名）
git branch -M main
git remote add origin https://github.com/你的用户名/daily-policy-report.git
git push -u origin main
```

### 步骤 3：启用 GitHub Pages

1. GitHub 仓库 → Settings
2. 左侧菜单 → Pages
3. Source：选择 `main` 分支
4. 文件夹：`/root`
5. 保存

### 步骤 4：完成！

等待 5-10 分钟，网站自动上线：
```
https://你的用户名.github.io/daily-policy-report
```

---

## 日常操作

### 手动生成报告（测试）

```bash
# 1. 生成 HTML 和 JSON 报告
python scripts/generate_report.py

# 2. 生成 Word 文档
python scripts/generate_word_report.py

# 3. 打包 Skill
python scripts/package_skill.py

# 4. 提交和发布
git add -A
git commit -m "手动更新报告"
git push
```

### 自动生成（推荐）

网站会自动每天早上 6:00 北京时间生成并发布报告。  
你无需做任何操作！

---

## 输出文件说明

### 生成的文件位置

```
reports/
├── latest.html              # 最新 HTML 报告
├── latest.docx              # 最新 Word 文档 ⭐
├── latest.json              # 最新 JSON 数据
├── report-2026-05-17.html   # 按日期保存的 HTML
├── report-2026-05-17.docx   # 按日期保存的 Word ⭐
└── index.html               # 报告索引页

dist/
└── daily-policy-report-*.skill  # 打包的 Skill 文件 ⭐

public/
├── index.html               # 网站首页
├── reports/                 # 报告文件夹
└── skills/                  # Skill 包文件夹
```

### 文件用途

| 文件 | 用途 | 下载方式 |
|------|------|---------|
| `.docx` | Word 文档，可编辑打印 | 网站报告页面 |
| `.html` | 网页版报告 | 网站直接查看 |
| `.json` | 数据格式，程序读取 | API 调用 |
| `.skill` | Skill 包，可安装 | GitHub Releases |

---

## 网站功能

### 首页
- 📊 显示最新报告摘要
- 📥 下载最新 Word 和 HTML 报告
- 📁 访问所有历史报告

### 报告页面
```
https://你的用户名.github.io/daily-policy-report/reports/
```
- 📅 按日期查看所有报告
- 💾 下载任意日期的 Word 版本
- 📋 查看报告详情

### 下载链接（示例）
```
最新 Word 报告：
https://你的用户名.github.io/daily-policy-report/reports/latest.docx

特定日期的 Word：
https://你的用户名.github.io/daily-policy-report/reports/政策日报_2026-05-17.docx

Skill 包：
https://你的用户名.github.io/daily-policy-report/skills/daily-policy-report-*.skill
```

---

## 自定义配置

### 修改报告生成时间

编辑 `.github/workflows/generate-report.yml`：

```yaml
on:
  schedule:
    - cron: '0 22 * * *'  # 修改这一行
```

| Cron 表达式 | 北京时间 |
|-----------|---------|
| `0 22 * * *` | 06:00 |
| `0 14 * * *` | 22:00 |
| `0 0 * * *` | 08:00 |
| `0 8 * * *` | 16:00 |

### 修改报告内容

编辑 `scripts/generate_report.py` 中的 `create_report_content()` 函数。

### 修改网站样式

编辑 `index.html` 中的 `<style>` 标签。

---

## 常见问题

### Q: 网站多久更新一次？
**A**: 每天早上 6:00 北京时间自动更新。

### Q: Word 文档怎样下载？
**A**: 访问网站，点击"下载完整报告"中的"查看最新报告"，然后点击 Word 链接。

### Q: 如何获得 Skill 包？
**A**: 在网站上访问 `/skills` 目录，或在 GitHub Releases 中下载。

### Q: 能否使用自定义域名？
**A**: 可以。在 GitHub Settings → Pages 中配置自定义域名。

### Q: 报告内容怎样更新？
**A**: 编辑 `scripts/generate_report.py` 中的政策数据。

### Q: 能否改为其他语言？
**A**: 可以。修改所有文件中的中文文本。

---

## 成本计算

| 项目 | 成本 |
|------|------|
| GitHub Pages | **免费** ✅ |
| 域名（可选） | $10-20/年 |
| 服务器 | **无需** ✅ |
| 存储 | **无限制** ✅ |
| 带宽 | **无限制** ✅ |
| **总计** | **$0（使用 GitHub 域名）** 🎉 |

---

## 后续优化

- 💾 **集成实时数据源** - 连接政策 API
- 📧 **邮件订阅** - 自动发送到收件箱
- 🔍 **搜索功能** - 快速查找政策
- 📊 **数据分析** - 政策趋势统计
- 🔔 **推送通知** - 微信/钉钉提醒

---

## 获取帮助

- 📖 [完整文档](README.md)
- 🛠️ [Skill 说明](SKILL.md)
- 📦 [安装指南](dist/INSTALL.md)
- 🐛 [报告问题](https://github.com/你的用户名/daily-policy-report/issues)

---

## 下一步

1. ✅ 按照上面的步骤部署网站
2. ✅ 等待每天早上 6 点自动生成报告
3. ✅ 在网站上下载 Word 或 HTML 版本
4. ✅ 分享网站链接给团队

**就这么简单！** 🎉

---

**版本**: 1.0.0  
**最后更新**: 2026-05-17
