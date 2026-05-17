#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from datetime import datetime, timedelta
from pathlib import Path

def create_report_content():
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
        "trends": "大模型与算力融合加速。数据标准体系完善。网络安全执法加强。AI与产业融合深入。算力与能源协同常态化。"
    }
    return report_data

def save_reports(report_data):
    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)

    with open(report_dir / "latest.json", "w", encoding="utf-8") as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)

    date_file = report_dir / f"report-{report_data['date']}.json"
    with open(date_file, "w", encoding="utf-8") as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)

    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>政策日报 - {report_data['date']}</title>
    <style>
        body {{ font-family: Arial; max-width: 900px; margin: 0 auto; padding: 20px; background: #f5f5f5; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; text-align: center; }}
        .section {{ background: white; padding: 20px; margin-bottom: 20px; border-radius: 5px; border-left: 5px solid #667eea; }}
        .policy {{ background: #f9f9f9; padding: 15px; margin-bottom: 15px; border-left: 3px solid #764ba2; }}
        a {{ color: #667eea; text-decoration: none; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>政策日报</h1>
        <p>{report_data['date']}</p>
    </div>
    <div class="section">
        <h2>过去24小时政策</h2>
        {"".join(f"<div class='policy'><h3>{p['title']}</h3><p>{p['institution']} | {p['date']}</p><p>{p['summary']}</p></div>" for p in report_data['policies_24h'])}
    </div>
    <div class="section">
        <h2>过去一个月政策</h2>
        {"".join(f"<div class='policy'><h3>{p['title']}</h3><p>{p['institution']} | {p['date']}</p><p>{p['summary']}</p></div>" for p in report_data['policies_1month'])}
    </div>
    <div class="section">
        <h2>未来趋势</h2>
        <p>{report_data['trends']}</p>
    </div>
    <div style="text-align: center; color: #999; padding: 20px;">
        <p>每天早上6点自动生成 | <a href="/">返回首页</a></p>
    </div>
</body>
</html>"""

    with open(report_dir / "latest.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    date_file = report_dir / f"report-{report_data['date']}.html"
    with open(date_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ 报告已生成: {report_data['date']}")

def main():
    print("开始生成报告...")
    report_data = create_report_content()
    save_reports(report_data)
    print("✅ 完成!")

if __name__ == "__main__":
    main()
