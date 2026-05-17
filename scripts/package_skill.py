#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
打包 daily-policy-report skill
"""

import json
import shutil
import zipfile
from pathlib import Path
from datetime import datetime

def create_skill_package():
    """创建 Skill 包"""

    skill_dir = Path(".")
    package_dir = Path("dist")
    package_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    skill_name = "daily-policy-report"
    package_name = f"{skill_name}-{timestamp}.skill"
    package_path = package_dir / package_name

    # 要包含的文件/目录
    include_items = [
        "SKILL.md",
        "README.md",
        "scripts/",
        "public/",
        "reports/",
        ".github/workflows/generate-report.yml"
    ]

    # 创建临时目录
    temp_dir = package_dir / "temp_skill"
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir()

    # 复制文件
    print(f"📦 打包 Skill: {skill_name}")

    for item in include_items:
        item_path = skill_dir / item
        if not item_path.exists():
            print(f"⚠️ 跳过不存在的项目: {item}")
            continue

        if item_path.is_file():
            shutil.copy2(item_path, temp_dir / item_path.name)
            print(f"  ✓ 复制文件: {item}")
        elif item_path.is_dir():
            dest_path = temp_dir / item_path.name
            shutil.copytree(item_path, dest_path, dirs_exist_ok=True)
            print(f"  ✓ 复制目录: {item}")

    # 创建 manifest.json
    manifest = {
        "name": "daily-policy-report",
        "version": "1.0.0",
        "description": "每日数据和信息化政策报告自动生成和发布系统",
        "author": "Policy Report Team",
        "created": datetime.now().isoformat(),
        "features": [
            "自动收集政策信息",
            "生成 Word 和 HTML 报告",
            "每日自动发布",
            "支持历史报告查询"
        ],
        "requirements": {
            "python": ">=3.8",
            "packages": [
                "python-docx>=0.8.11",
                "requests>=2.28.0",
                "beautifulsoup4>=4.11.0"
            ]
        },
        "automation": {
            "schedule": "0 6 * * *",
            "description": "每天早上 6:00 自动生成报告"
        }
    }

    with open(temp_dir / "manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print("  ✓ 创建 manifest.json")

    # 创建 ZIP 文件
    with zipfile.ZipFile(package_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in temp_dir.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(temp_dir)
                zipf.write(file_path, arcname)

    # 清理临时目录
    shutil.rmtree(temp_dir)

    print(f"✅ Skill 包已创建: {package_path}")
    print(f"   文件大小: {package_path.stat().st_size / 1024:.1f} KB")

    return str(package_path)

def create_installation_guide():
    """创建安装指南"""

    guide = """# Skill 安装指南

## 安装 daily-policy-report Skill

### 前置要求
- Python 3.8+
- 必要的 Python 包已在 manifest.json 中列出

### 安装步骤

#### 方法 1：使用 Skill Manager（推荐）
```bash
skill install daily-policy-report-*.skill
```

#### 方法 2：手动安装
1. 解压 `.skill` 文件
2. 将文件复制到你的 skills 目录
3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

### 配置

1. 编辑 `scripts/generate_report.py` 中的数据源
2. 根据需要调整 `.github/workflows/generate-report.yml` 中的时间表
3. 配置你的网站发布目标

### 验证安装

```bash
# 测试报告生成
python scripts/generate_report.py

# 生成 Word 版本
pip install python-docx
python scripts/generate_word_report.py
```

### 自动化设置

该 Skill 包含 GitHub Actions 配置，自动每天生成报告。

要启用自动化：
1. 将文件推送到 GitHub
2. 在 Settings > Actions 中启用 GitHub Actions
3. 报告会在指定时间自动生成

### 故障排除

**问题：找不到模块**
```bash
pip install -r requirements.txt
```

**问题：报告未生成**
- 检查 `.github/workflows/generate-report.yml` 的时间设置
- 查看 GitHub Actions 的执行日志

**问题：网站未更新**
- 确保 GitHub Pages 已启用
- 检查文件是否成功推送

### 支持

如有问题，请查看：
- README.md - 完整文档
- SKILL.md - Skill 详细说明
- 官方仓库的 Issues

### 更新

要更新到最新版本：
```bash
skill update daily-policy-report
```

---

版本：1.0.0
最后更新：{datetime.now().strftime('%Y-%m-%d')}
"""

    with open(Path("dist/INSTALL.md"), "w", encoding="utf-8") as f:
        f.write(guide)

    print("✅ 安装指南已创建: dist/INSTALL.md")

def main():
    """主函数"""
    print("🚀 开始打包 Skill...\n")

    # 创建 Skill 包
    package_path = create_skill_package()

    print()

    # 创建安装指南
    create_installation_guide()

    print("\n✅ Skill 打包完成！")
    print(f"\n📦 可发布的文件:")
    print(f"   - {package_path}")
    print(f"   - dist/INSTALL.md")

if __name__ == "__main__":
    main()
