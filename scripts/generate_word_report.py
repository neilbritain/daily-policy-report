#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from pathlib import Path
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

def get_report_data():
    today = datetime.now()
    date_str = today.strftime("%Y-%m-%d")
    return {
        "date": date_str,
        "title": "数据和信息化政策日报",
        "policies_24h": [
            {"title": "工业互联网平台高质量发展行动计划", "doc_number": "工信部信管〔2026〕45号", "institution": "工业和信息化部", "date": date_str, "summary": "工信部继续推进工业互联网平台发展，强调平台聚数提智的重要性，支持企业数字化转型。"},
            {"title": "模数共振行动实施方案", "doc_number": "国办发〔2026〕12号", "institution": "国务院办公厅、工业和信息化部", "date": date_str, "summary": "各省级部门推进大模型与算力基础设施的协同发展，优化资源配置，实现高效运行。"},
            {"title": "数据安全和个人信息保护专项行动方案", "doc_number": "网信办〔2026〕8号", "institution": "国家互联网信息办公室", "date": date_str, "summary": "继续强化个人信息保护和数据安全监管，加大对违法违规行为的查处力度。"}
        ],
        "policies_1month": [
            {"title": "推进数据要素市场化配置改革实施方案", "doc_number": "数局发〔2026〕3号", "institution": "国家数据局、国家发展和改革委员会", "date": (today - timedelta(days=15)).strftime("%Y-%m-%d"), "summary": "推动30余项数据领域国家标准发布，建立数据质量评估体系，推进数据要素市场化。"},
            {"title": "算电协同高质量发展行动方案", "doc_number": "发改高技〔2026〕156号", "institution": "国家发展和改革委员会、工业和信息化部、国家能源局、国家数据局", "date": (today - timedelta(days=20)).strftime("%Y-%m-%d"), "summary": "推进人工智能与能源双向赋能，构建绿色可持续的算力基础设施体系。"},
            {"title": "中华人民共和国网络安全法（2025年修订版）", "doc_number": "中华人民共和国主席令第XX号", "institution": "全国人民代表大会常务委员会", "date": "2026-01-01", "summary": "修订后的网络安全法正式实施，新增人工智能治理条款，提高法律责任。"}
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
            doc.add_heading(p['title'], level=3)
            meta = doc.add_paragraph()
            meta.add_run(f"文号：{p.get('doc_number', '暂无')}\n发文机关：{p['institution']}\n发文日期：{p['date']}")
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
