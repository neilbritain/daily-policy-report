# 🚀 快速部署指南

## 5 分钟快速上线

### 第 1 步：创建 GitHub 账号（如果没有）

访问 [GitHub](https://github.com) 注册免费账号

---

### 第 2 步：创建仓库（在 GitHub 网站上）

1. 登录 GitHub
2. 点击右上角 `+` → `New repository`
3. 填写信息：
   - **Repository name**: `daily-policy-report`
   - **Description**: 数据和信息化政策日报
   - **选择**: `Public`（公开）
   - **不需要选择其他选项**
4. 点击 `Create repository`

---

### 第 3 步：上传代码到 GitHub

在本地运行以下命令：

```bash
# 进入项目目录
cd D:\D\lidahe2026\c-c\daily-policy-report

# 初始化 Git（如果还没初始化）
git init

# 添加所有文件
git add .

# 提交
git commit -m "初始化项目"

# 添加远程仓库（替换 你的用户名）
git remote add origin https://github.com/你的用户名/daily-policy-report.git

# 推送到 GitHub
git branch -M main
git push -u origin main
```

---

### 第 4 步：启用 GitHub Pages

1. 在 GitHub 上打开你的仓库
2. 点击 `Settings` → 左侧菜单 `Pages`
3. 在 `Source` 下：
   - 选择 `Deploy from a branch`
   - 选择 `main` 分支
   - 选择文件夹 `/ (root)`
4. 点击 `Save`

**5 分钟后**，你的网站就会在这个地址上线：
```
https://你的用户名.github.io/daily-policy-report
```

---

### 第 5 步：自动化每日报告（可选）

网站会自动每天生成报告。GitHub Actions 已配置在 `.github/workflows/generate-report.yml` 中。

**每天早上 6:00 北京时间**，新的报告会自动生成并发布。

---

## 验证部署成功

✅ **检查清单**：

1. 访问 `https://你的用户名.github.io/daily-policy-report`
2. 应该看到蓝紫色的首页
3. 点击"查看最新报告"，应该能看到今天的政策报告

---

## 自定义域名（可选，费用）

如果你想使用自己的域名（如 `policy-report.com`）：

1. 购买域名（阿里云、腾讯云等，$10-20/年）
2. 在 GitHub Settings → Pages 中添加自定义域名
3. 根据指示配置 DNS

---

## 手动生成报告（测试）

如果想立即生成报告而不等待自动化：

```bash
# 1. 安装依赖
pip install requests beautifulsoup4 python-dateutil

# 2. 生成报告
python scripts/generate_report.py

# 3. 提交和推送
git add -A
git commit -m "手动生成报告"
git push
```

报告会在网站上显示。

---

## 成本计算

| 项目 | 费用 |
|------|------|
| GitHub Pages | **免费** ✅ |
| 域名 | 可选（$10-20/年） |
| 服务器 | **不需要** ✅ |
| 存储 | **无限制** ✅ |
| 带宽 | **无限制** ✅ |
| **总费用** | **$0（使用 GitHub 域名）** |

---

## 常见问题

### Q: 网站多久能上线？
**A**: 代码推送后，5-10 分钟内网站会上线。

### Q: 报告多久更新一次？
**A**: 每天早上 6:00 北京时间自动生成新报告。

### Q: 如何查看历史报告？
**A**: 访问 `/reports` 页面，可以看到最近 30 份报告。

### Q: 能改成其他更新时间吗？
**A**: 可以。编辑 `.github/workflows/generate-report.yml` 的 `cron` 字段。

### Q: 如何修改报告内容？
**A**: 编辑 `scripts/generate_report.py` 中的 `create_report_content()` 函数。

---

## 后续优化建议

- 💾 **集成真实数据源**：连接新闻 API 自动获取政策信息
- 📧 **邮件订阅**：添加邮件订阅功能
- 🔍 **搜索功能**：添加报告搜索和过滤
- 📱 **移动适配**：优化手机显示
- 🔔 **微信推送**：集成微信通知

---

## 需要帮助？

- GitHub Pages 文档：https://pages.github.com
- GitHub Actions 文档：https://docs.github.com/actions

祝你使用愉快！🎉
