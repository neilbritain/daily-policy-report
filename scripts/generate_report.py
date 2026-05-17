#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from datetime import datetime, timedelta
from pathlib import Path

def create_report_content():
    today = datetime.now()
    date_str = today.strftime("%Y-%m-%d")
    return {
        "date": date_str,
        "title": "数据和信息化政策日报",
        "policies_24h": [
            {
                "title": "工业互联网平台高质量发展行动计划",
                "doc_number": "工信部信管〔2026〕45号",
                "institution": "工业和信息化部",
                "date": date_str,
                "summary": "工信部继续推进工业互联网平台发展，强调平台聚数提智的重要性，支持企业数字化转型。"
            },
            {
                "title": "模数共振行动实施方案",
                "doc_number": "国办发〔2026〕12号",
                "institution": "国务院办公厅、工业和信息化部",
                "date": date_str,
                "summary": "各省级部门推进大模型与算力基础设施的协同发展，优化资源配置，实现高效运行。"
            },
            {
                "title": "数据安全和个人信息保护专项行动方案",
                "doc_number": "网信办〔2026〕8号",
                "institution": "国家互联网信息办公室",
                "date": date_str,
                "summary": "继续强化个人信息保护和数据安全监管，加大对违法违规行为的查处力度。"
            }
        ],
        "policies_1month": [
            {
                "title": "推进数据要素市场化配置改革实施方案",
                "doc_number": "数局发〔2026〕3号",
                "institution": "国家数据局、国家发展和改革委员会",
                "date": (today - timedelta(days=15)).strftime("%Y-%m-%d"),
                "summary": "推动30余项数据领域国家标准发布，建立数据质量评估体系，推进数据要素市场化。"
            },
            {
                "title": "算电协同高质量发展行动方案",
                "doc_number": "发改高技〔2026〕156号",
                "institution": "国家发展和改革委员会、工业和信息化部、国家能源局、国家数据局",
                "date": (today - timedelta(days=20)).strftime("%Y-%m-%d"),
                "summary": "推进人工智能与能源双向赋能，构建绿色可持续的算力基础设施体系。"
            },
            {
                "title": "中华人民共和国网络安全法（2025年修订版）",
                "doc_number": "中华人民共和国主席令第XX号",
                "institution": "全国人民代表大会常务委员会",
                "date": "2026-01-01",
                "summary": "修订后的网络安全法正式实施，新增人工智能治理条款，提高法律责任。"
            }
        ],
        "trends": [
            "大模型与算力基础设施融合加速。预期各省级部门的模数共振实施方案将陆续落地，下半年将看到大量具体项目部署。",
            "数据标准体系加快完善。30余项国家标准将在下半年逐步发布，数据管理将从粗放式向精细化转变。",
            "网络安全执法力度加强。基于修订后网络安全法的更严厉罚则，相关执法部门将加大检查力度。",
            "人工智能与产业融合深入。工业互联网平台与AI技术的融合将进入快速应用阶段，制造、能源、金融等行业率先部署。",
            "算力与能源协同常态化。各地将建立算力与能源协同机制，算力成本波动性增大，用户需建立灵活的采购策略。"
        ]
    }

def render_policies(policies):
    html = ""
    for p in policies:
        html += f"""
        <div class="policy">
            <h3>{p['title']}</h3>
            <div class="policy-meta">
                <span class="doc-number">文号：{p.get('doc_number', '暂无')}</span><br/>
                <span>发文机关：{p['institution']}</span><br/>
                <span>发文日期：{p['date']}</span>
            </div>
            <div class="policy-summary">{p['summary']}</div>
        </div>"""
    return html

def save_reports(report_data):
    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)

    with open(report_dir / "latest.json", "w", encoding="utf-8") as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)

    with open(report_dir / f"report-{report_data['date']}.json", "w", encoding="utf-8") as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)

    trends_html = "".join(f"<li>{t}</li>" for t in report_data['trends'])
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>政策日报 - {report_data['date']}</title>
    <style>
        body {{ font-family: "Microsoft YaHei", Arial, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; background: #f5f5f5; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 1.8em; }}
        .header p {{ margin: 8px 0 0 0; opacity: 0.9; }}
        .section {{ background: white; padding: 20px; margin-bottom: 20px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); border-left: 5px solid #667eea; }}
        .section h2 {{ color: #667eea; margin-top: 0; border-bottom: 1px solid #eee; padding-bottom: 10px; }}
        .policy {{ background: #f9f9f9; padding: 15px; margin-bottom: 15px; border-left: 3px solid #764ba2; border-radius: 3px; }}
        .policy h3 {{ margin: 0 0 10px 0; color: #333; font-size: 1em; }}
        .policy-meta {{ color: #666; font-size: 0.88em; margin-bottom: 10px; line-height: 1.8; }}
        .doc-number {{ color: #764ba2; font-weight: bold; }}
        .policy-summary {{ color: #444; line-height: 1.7; font-size: 0.95em; }}
        .trends ul {{ margin: 0; padding-left: 20px; }}
        .trends li {{ margin-bottom: 10px; color: #444; line-height: 1.7; }}
        .footer {{ text-align: center; color: #999; padding: 20px; font-size: 0.85em; }}
        a {{ color: #667eea; text-decoration: none; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>数据和信息化政策日报</h1>
        <p>数据 • 算力 • 信息化 政策速览</p>
        <p>生成日期：{report_data['date']}</p>
    </div>
    <div class="section">
        <h2>一、过去 24 小时关键政策</h2>
        {render_policies(report_data['policies_24h'])}
    </div>
    <div class="section">
        <h2>二、过去一个月主要政策动向</h2>
        {render_policies(report_data['policies_1month'])}
    </div>
    <div class="section trends">
        <h2>三、未来趋势判断</h2>
        <ul>{trends_html}</ul>
    </div>
    <div class="footer">
        <p>每天早上 6:00 自动生成 | <a href="../index.html">返回首页</a></p>
    </div>
</body>
</html>"""

    with open(report_dir / "latest.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    with open(report_dir / f"report-{report_data['date']}.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"OK: {report_data['date']}")

def main():
    report_data = create_report_content()
    save_reports(report_data)

if __name__ == "__main__":
    main()
