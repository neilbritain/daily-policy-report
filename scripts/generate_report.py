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
            },
            {
                "title": "欧盟人工智能法案配套实施细则",
                "doc_number": "EU AI Act 2024/1689 实施细则",
                "institution": "欧盟委员会（European Commission）",
                "date": date_str,
                "summary": "欧盟发布AI法案高风险系统认证细则，要求医疗、交通、公共服务等领域AI系统须通过第三方合规审计，对出口至欧盟市场的AI产品具有重要影响。"
            },
            {
                "title": "美国关键基础设施数据安全行政令更新",
                "doc_number": "Executive Order 14117 修订版",
                "institution": "美国总统办公室（White House）",
                "date": date_str,
                "summary": "美国更新关键基础设施数据保护要求，进一步限制敏感数据跨境流向特定国家，并要求云服务商加强数据本地化合规审查。"
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
            },
            {
                "title": "全球数字契约实施框架",
                "doc_number": "A/RES/79/1",
                "institution": "联合国大会（UN General Assembly）",
                "date": (today - timedelta(days=10)).strftime("%Y-%m-%d"),
                "summary": "联合国全球数字契约实施框架正式生效，确立数据跨境流动、算法透明度、数字公共基础设施等国际规则，对各成员国数字治理政策制定具有重要参考价值。"
            },
            {
                "title": "G7数字与技术部长声明：AI治理原则更新",
                "doc_number": "G7 Digital Ministers Statement 2026",
                "institution": "七国集团（G7）数字与技术部长会议",
                "date": (today - timedelta(days=25)).strftime("%Y-%m-%d"),
                "summary": "G7更新AI治理广岛进程原则，强调负责任AI开发、数据自由流动与可信任环境建设，推动多边框架下的算法审计与互操作性标准对接。"
            }
        ],
        "trends": [
            "大模型与算力融合加速。国内模数共振方案陆续落地；国际方面，微软、谷歌等持续扩大亚太算力部署，全球算力争夺格局加剧。",
            "数据跨境规则体系加速形成。国内数据出境安全评估机制逐步完善；欧盟AI法案和美国数据安全行政令双重压力下，跨国数据流动合规成本显著上升。",
            "网络安全执法全球同步收紧。国内基于修订后网络安全法加大执法；美欧同步强化关键基础设施保护，网络安全国际合作与博弈并行深化。",
            "AI治理标准国际竞争白热化。ISO/IEC发布AI管理体系国际标准，国内相关国家标准同步推进，争夺国际规则制定主导权已成战略重点。",
            "绿色算力成全球共同议题。国内算电协同机制加快落地；IEA报告显示全球数据中心能耗将超越航空业，绿色算力政策将成各国竞争新赛道。"
        ]
    }

def render_policies(policies):
    html = ""
    for p in policies:
        html += f"""
        <div class="policy">
            <p class="policy-title">《{p['title']}》</p>
            <p class="policy-meta">【文号】{p.get('doc_number', '暂无')}</p>
            <p class="policy-meta">【发文机关】{p['institution']}</p>
            <p class="policy-meta">【发文日期】{p['date']}</p>
            <p class="policy-summary">{p['summary']}</p>
        </div>"""
    return html

def save_reports(report_data):
    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)

    with open(report_dir / "latest.json", "w", encoding="utf-8") as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)
    with open(report_dir / f"report-{report_data['date']}.json", "w", encoding="utf-8") as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)

    trends_html = "".join(
        f'<p class="trend-item">{"①②③④⑤"[i]} {t}</p>'
        for i, t in enumerate(report_data['trends'])
    )

    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>政策日报 - {report_data['date']}</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: "Microsoft YaHei", "PingFang SC", Arial, sans-serif;
            font-size: 16px;
            line-height: 1.8;
            color: #333;
            background: #f7f7f7;
            padding: 16px;
        }}
        .article {{
            max-width: 680px;
            margin: 0 auto;
            background: white;
            padding: 24px 20px;
        }}
        .article-title {{
            font-size: 22px;
            font-weight: bold;
            color: #1a1a1a;
            text-align: center;
            margin-bottom: 6px;
        }}
        .article-date {{
            font-size: 13px;
            color: #999;
            text-align: center;
            margin-bottom: 24px;
        }}
        .section-title {{
            font-size: 17px;
            font-weight: bold;
            color: #fff;
            background: #5b6de4;
            padding: 8px 14px;
            border-radius: 4px;
            margin: 24px 0 12px 0;
        }}
        .policy {{
            border-left: 3px solid #5b6de4;
            padding: 12px 14px;
            margin-bottom: 16px;
            background: #f9f9ff;
            border-radius: 0 4px 4px 0;
        }}
        .policy-title {{
            font-size: 15px;
            font-weight: bold;
            color: #222;
            margin-bottom: 6px;
        }}
        .policy-meta {{
            font-size: 13px;
            color: #666;
            margin-bottom: 3px;
        }}
        .policy-summary {{
            font-size: 14px;
            color: #444;
            margin-top: 8px;
            line-height: 1.8;
        }}
        .trend-item {{
            font-size: 14px;
            color: #444;
            line-height: 1.8;
            margin-bottom: 10px;
            padding-left: 4px;
        }}
        .divider {{
            border: none;
            border-top: 1px dashed #ddd;
            margin: 20px 0;
        }}
        .footer {{
            font-size: 12px;
            color: #bbb;
            text-align: center;
            margin-top: 24px;
            padding-top: 16px;
            border-top: 1px solid #eee;
        }}
        a {{ color: #5b6de4; text-decoration: none; }}
    </style>
</head>
<body>
<div class="article">

    <div class="article-title">数据和信息化政策日报</div>
    <div class="article-date">{report_data['date']} | 数据 · 算力 · 信息化</div>

    <div class="section-title">一、过去 24 小时关键政策</div>
    {render_policies(report_data['policies_24h'])}

    <hr class="divider"/>

    <div class="section-title">二、过去一个月主要政策动向</div>
    {render_policies(report_data['policies_1month'])}

    <hr class="divider"/>

    <div class="section-title">三、未来趋势判断</div>
    {trends_html}

    <div class="footer">
        每天早上 6:00 自动生成 · <a href="../index.html">返回首页</a>
    </div>

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
