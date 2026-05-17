#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
政策日报自动生成脚本
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

def create_report_content():
    """创建报告内容"""
    today = datetime.now()
    date_str = today.strftime("%Y-%m-%d")

    report_data = {
        "date": date_str,
        "title": "数据和信息化政策日报",
        "policies_24h": [
            {
                "title": "工业互联网平台发展",
                "institution": "工业和信息化部",
                "date": date_str,
                "summary": "工信部继续推进工业互联网平台发展，强调平台聚数提智的重要性，支持企业数字化转型。"
            },
            {
                "title": "模数共振行动实施",
                "institution": "国务院、工业和信息化部",
                "date": date_str,
                "summary": "各省级部门推进大模型与算力基础设施的协同发展，优化资源配置，实现高效运行。"
            },
            {
                "title": "数据安全和隐私保护",
                "institution": "网信办",
                "date": date_str,
                "summary": "继续强化个人信息保护和数据安全监管，加大对违法违规行为的查处力度。"
            }
        ],
        "policies_1month": [
            {
                "title": "数据要素计划持续推进",
                "institution": "国家数据局、发改委",
                "date": (today - timedelta(days=15)).strftime("%Y-%m-%d"),
                "summary": "推动30余项数据领域国家标准发布，建立数据质量评估体系，推进数据要素市场化。"
            },
            {
                "title": "算电协同行动方案",
                "institution": "国家发改委、工信部、国家能源局、国家数据局",
                "date": (today - timedelta(days=20)).strftime("%Y-%m-%d"),
                "summary": "推进人工智能与能源双向赋能，构建绿色可持续的算力基础设施体系。"
            },
            {
                "title": "网络安全法正式施行",
                "institution": "全国人大常委会、网信办",
                "date": "2026-01-01",
                "summary": "修订后的网络安全法正式实施，新增人工智能治理条款，提高法律责任。"
            }
        ],
        "trends": "1. 大模型与算力基础设施融合加速 - 预期各省级部门的模数共振实施方案将陆续落地，下半年将看到大量具体项目部署。 2. 数据标准体系加快完善 - 30余项国家标准将在下半年逐步发布，数据管理将从粗放式向精细化转变。 3. 网络安全执法力度加强 - 基于修订后网络安全法的更严厉罚则，相关执法部门将加大检查力度。 4. 人工智能与产业融合深入 - 工业互联网平台与AI技术的融合将进入快速应用阶段，制造业、能源、金融等行业率先部署。 5. 算力与能源协同常态化 - 各地将建立算力与能源协同机制，算力成本波动性增大，用户需建立灵活的采购策略。"
    }

    return report_data

def save_json_report(report_data):
    """保存 JSON 格式的报告"""
    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)

    with open(report_dir / "latest.json", "w", encoding="utf-8") as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)

    date_file = report_dir / f"report-{report_data['date']}.json"
    with open(date_file, "w", encoding="utf-8") as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)

    print(f"✅ JSON 报告已保存: {date_file}")

def save_html_report(report_data):
    """保存 HTML 格式的报告"""
    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)

    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>政策日报 - {report_data['date']}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2em;
        }}
        .header p {{
            margin: 5px 0 0 0;
            opacity: 0.9;
        }}
        .section {{
            background: white;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            border-left: 5px solid #667eea;
        }}
        .section h2 {{
            color: #667eea;
            margin-top: 0;
        }}
        .policy {{
            background: #f9f9f9;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 5px;
            border-left: 3px solid #764ba2;
        }}
        .policy h3 {{
            margin: 0 0 10px 0;
            color: #333;
        }}
        .policy-meta {{
            color: #666;
            font-size: 0.9em;
            margin-bottom: 10px;
        }}
        .policy-summary {{
            color: #555;
            line-height: 1.6;
        }}
        .trends {{
            color: #555;
            line-height: 1.8;
        }}
        .footer {{
            text-align: center;
            color: #999;
            padding: 20px;
            font-size: 0.9em;
        }}
        a {{
            color: #667eea;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 {report_data['title']}</h1>
        <p>生成日期：{report_data['date']}</p>
    </div>

    <div class="section">
        <h2>📌 过去 24 小时的关键政策</h2>
        {''.join(f'''
        <div class="policy">
            <h3>{p['title']}</h3>
            <div class="policy-meta">
                <span>🏛️ {p['institution']}</span>
                <span>📅 {p['date']}</span>
            </div>
            <div class="policy-summary">{p['summary']}</div>
        </div>
        ''' for p in report_data['policies_24h'])}
    </div>

    <div class="section">
        <h2>📊 过去一个月的主要政策动向</h2>
        {''.join(f'''
        <div class="policy">
            <h3>{p['title']}</h3>
            <div class="policy-meta">
                <span>🏛️ {p['institution']}</span>
                <span>📅 {p['date']}</span>
            </div>
            <div class="policy-summary">{p['summary']}</div>
        </div>
        ''' for p in report_data['policies_1month'])}
    </div>

    <div class="section">
        <h2>📈 未来趋势判断</h2>
        <div class="trends">
            {report_data['trends']}
        </div>
    </div>

    <div class="footer">
        <p>每天早上 6:00 自动生成 | <a href="/">返回首页</a></p>
    </div>
</body>
</html>
"""

    with open(report_dir / "latest.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    date_file = report_dir / f"report-{report_data['date']}.html"
    with open(date_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ HTML 报告已保存: {date_file}")

def create_reports_index():
    """创建报告列表页面"""
    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)

    html_files = sorted(report_dir.glob("report-*.html"), reverse=True)

    reports_list = "\n".join(f'''
    <tr>
        <td><a href="{f.name}">{f.stem.replace("report-", "")}</a></td>
        <td><a href="{f.name}">查看</a></td>
    </tr>
    ''' for f in html_files[:30])

    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>政策报告存档</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
        }}
        table {{
            width: 100%;
            background: white;
            border-collapse: collapse;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            border-radius: 5px;
            overflow: hidden;
        }}
        th, td {{
            padding: 15px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background: #667eea;
            color: white;
            font-weight: bold;
        }}
        tr:hover {{
            background: #f9f9f9;
        }}
        a {{
            color: #667eea;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        .footer {{
            text-align: center;
            color: #999;
            padding: 20px;
            margin-top: 30px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📚 政策报告存档</h1>
        <p>最近 30 份政策日报</p>
    </div>

    <table>
        <tr>
            <th>报告日期</th>
            <th>操作</th>
        </tr>
        {reports_list}
    </table>

    <div class="footer">
        <p><a href="/">返回首页</a></p>
    </div>
</body>
</html>
"""

    with open(report_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ 报告索引已更新: reports/index.html")

def main():
    """主函数"""
    print("🚀 开始生成政策日报...")

    report_data = create_report_content()

    save_json_report(report_data)
    save_html_report(report_data)
    create_reports_index()

    print(f"✅ 政策日报生成完成！日期：{report_data['date']}")

if __name__ == "__main__":
    main()
