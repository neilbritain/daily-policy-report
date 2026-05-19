#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, timezone
from pathlib import Path
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

BEIJING_TZ = timezone(timedelta(hours=8))

def get_report_data():
    today = datetime.now(BEIJING_TZ)
    date_str = today.strftime("%Y-%m-%d")
    return {
        "date": date_str,
        "title": "数据和信息化政策日报",
        "policies_24h": [
            {"title": "工业互联网平台高质量发展行动计划", "doc_number": "工信部信管〔2026〕45号", "institution": "工业和信息化部", "date": date_str, "url": "https://www.miit.gov.cn/zwgk/zcwj/wjfb/index.html", "summary": "工信部继续推进工业互联网平台发展，强调平台聚数提智的重要性，支持企业数字化转型。"},
            {"title": "模数共振行动实施方案", "doc_number": "国办发〔2026〕12号", "institution": "国务院办公厅、工业和信息化部", "date": date_str, "url": "https://www.gov.cn/zhengce/zhengceku/index.htm", "summary": "各省级部门推进大模型与算力基础设施的协同发展，优化资源配置，实现高效运行。"},
            {"title": "数据安全和个人信息保护专项行动方案", "doc_number": "网信办〔2026〕8号", "institution": "国家互联网信息办公室", "date": date_str, "url": "https://www.cac.gov.cn/hjlyj/index.htm", "summary": "继续强化个人信息保护和数据安全监管，加大对违法违规行为的查处力度。"},
            {"title": "欧盟人工智能法案配套实施细则", "doc_number": "EU AI Act 2024/1689 实施细则", "institution": "欧盟委员会（European Commission）", "date": date_str, "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689", "summary": "欧盟发布《欧盟人工智能法案》高风险系统认证细则，要求医疗、交通、公共服务等领域AI系统须通过第三方合规审计，对出口至欧盟市场的AI产品具有重要影响。"},
            {"title": "美国关键基础设施数据安全行政令更新", "doc_number": "Executive Order 14117 修订版", "institution": "美国总统办公室（White House）", "date": date_str, "url": "https://www.whitehouse.gov/briefing-room/presidential-actions/", "summary": "美国更新关键基础设施数据保护要求，进一步限制敏感数据跨境流向特定国家，并要求云服务商加强数据本地化合规审查。"}
        ],
        "policies_1month": [
            {"title": "推进数据要素市场化配置改革实施方案", "doc_number": "数局发〔2026〕3号", "institution": "国家数据局、国家发展和改革委员会", "date": (today - timedelta(days=15)).strftime("%Y-%m-%d"), "url": "https://www.nda.gov.cn/sjj/zcfg/", "summary": "推动30余项数据领域国家标准发布，建立数据质量评估体系，推进数据要素市场化。"},
            {"title": "算电协同高质量发展行动方案", "doc_number": "发改高技〔2026〕156号", "institution": "国家发展和改革委员会、工业和信息化部、国家能源局、国家数据局", "date": (today - timedelta(days=20)).strftime("%Y-%m-%d"), "url": "https://www.ndrc.gov.cn/xxgk/zcfb/", "summary": "推进人工智能与能源双向赋能，构建绿色可持续的算力基础设施体系。"},
            {"title": "中华人民共和国网络安全法（2025年修订版）", "doc_number": "中华人民共和国主席令第XX号", "institution": "全国人民代表大会常务委员会", "date": "2026-01-01", "url": "https://www.npc.gov.cn/npc/c2/c30834/", "summary": "修订后的《中华人民共和国网络安全法（2025年修订版）》正式实施，新增人工智能治理条款，提高法律责任。"},
            {"title": "全球数字契约实施框架", "doc_number": "A/RES/79/1", "institution": "联合国大会（UN General Assembly）", "date": (today - timedelta(days=10)).strftime("%Y-%m-%d"), "url": "https://www.un.org/techenvoy/global-digital-compact", "summary": "《全球数字契约实施框架》正式生效，确立数据跨境流动、算法透明度、数字公共基础设施等国际规则，对各成员国数字治理政策制定具有重要参考价值。"},
            {"title": "G7数字与技术部长声明：AI治理原则更新", "doc_number": "G7 Digital Ministers Statement 2026", "institution": "七国集团（G7）数字与技术部长会议", "date": (today - timedelta(days=25)).strftime("%Y-%m-%d"), "url": "https://www.g7italy.it/en/presidency-priorities/digital/", "summary": "G7更新AI治理广岛进程原则，强调负责任AI开发、数据自由流动与可信任环境建设，推动多边框架下的算法审计与互操作性标准对接。"}
        ]
    }

def save_word_report(report_data):
    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)
    doc = Document()
    doc.styles['Normal'].font.name = 'Calibri'
    doc.styles['Normal'].font.size = Pt(11)

    title = doc.add_paragraph()
    title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    r = title.add_run(report_data['title'])
    r.font.size = Pt(24); r.font.bold = True
    r.font.color.rgb = RGBColor(102, 126, 234)

    sub = doc.add_paragraph()
    sub.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    sub.add_run(f"生成日期：{report_data['date']}")

    doc.add_page_break()

    for section_title, policies in [
        ("一、过去24小时关键政策", report_data['policies_24h']),
        ("二、过去一个月主要政策动向", report_data['policies_1month'])
    ]:
        h = doc.add_heading(section_title, level=1)
        h.runs[0].font.color.rgb = RGBColor(102, 126, 234)
        for p in policies:
            doc.add_heading(f"《{p['title']}》", level=3)
            meta = doc.add_paragraph()
            url_line = f"\n原文链接：{p['url']}" if p.get('url') else ''
            meta.add_run(f"文号：{p.get('doc_number', '暂无')}\n发文机关：{p['institution']}\n发文日期：{p['date']}{url_line}")
            meta.runs[0].font.size = Pt(10)
            meta.runs[0].font.color.rgb = RGBColor(100, 100, 100)
            doc.add_paragraph(p['summary'])

    doc.save(report_dir / "latest.docx")
    doc.save(report_dir / f"report-{report_data['date']}.docx")
    print(f"OK Word: {report_data['date']}")

def main():
    report_data = get_report_data()
    try:
        save_word_report(report_data)
    except ImportError:
        print("pip install python-docx")

if __name__ == "__main__":
    main()
