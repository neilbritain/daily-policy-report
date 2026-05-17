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
            {"title": "工业互联网平台发展", "institution": "工业和信息化部", "date": date_str, "summary": "工信部继续推进工业互联网平台发展，强调平台聚数提智的重要性，支持企业数字化转型。"},
            {"title": "模数共振行动实施", "institution": "国务院、工业和信息化部", "date": date_str, "summary": "各省级部门推进大模型与算力基础设施的协同发展，优化资源配置，实现高效运行。"},
            {"title": "数据安全和隐私保护", "institution": "网信办", "date": date_str, "summary": "继续强化个人信息保护和数据安全监管，加大对违法违规行为的查处力度。"}
        ],
        "policies_1month": [
            {"title": "数据要素计划持续推进", "institution": "国家数据局、发改委", "date": (today - timedelta(days=15)).strftime("%Y-%m-%d"), "summary": "推动30余项数据领域国家标准发布，建立数据质量评估体系，推进数据要素市场化。"},
            {"title": "算电协同行动方案", "institution": "国家发改委、工信部、国家能源局、国家数据局", "date": (today - timedelta(days=20)).strftime("%Y-%m-%d"), "summary": "推进人工智能与能源双向赋能，构建绿色可持续的算力基础设施体系。"},
            {"title": "网络安全法正式施行", "institution": "全国人大常委会、网信办", "date": "2026-01-01", "summary": "修订后的网络安全法正式实施，新增人工智能治理条款，提高法律责任。"}
        ]
    }

def save_word_report(report_data):
    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)

    doc = Document()
    style = doc.styles['Normal']
    style.font.name = 'Calibri'
    style.font.size = Pt(11)

    title = doc.add_paragraph()
    title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    title_run = title.add_run(report_data['title'])
    title_run.font.size = Pt(28)
    title_run.font.bold = True
    title_run.font.color.rgb = RGBColor(102, 126, 234)

    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    subtitle_run = subtitle.add_run("数据 • 算力 • 信息化 政策速览")
    subtitle_run.font.size = Pt(14)

    date_para = doc.add_paragraph()
    date_para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    date_run = date_para.add_run(f"生成日期: {report_data['date']}")
    date_run.font.size = Pt(12)

    doc.add_page_break()

    doc.add_heading("一、过去24小时的关键政策", level=1)
    for p in report_data['policies_24h']:
        doc.add_heading(p['title'], level=3)
        meta = doc.add_paragraph(f"机构: {p['institution']} | 日期: {p['date']}")
        meta.runs[0].font.size = Pt(10)
        doc.add_paragraph(p['summary'])

    doc.add_heading("二、过去一个月的主要政策动向", level=1)
    for p in report_data['policies_1month']:
        doc.add_heading(p['title'], level=3)
        meta = doc.add_paragraph(f"机构: {p['institution']} | 日期: {p['date']}")
        meta.runs[0].font.size = Pt(10)
        doc.add_paragraph(p['summary'])

    latest_path = report_dir / "latest.docx"
    doc.save(latest_path)
    print(f"✅ Word报告已生成: {latest_path}")

    date_path = report_dir / f"report-{report_data['date']}.docx"
    doc.save(date_path)

def main():
    print("生成Word报告...")
    report_data = get_report_data()
    try:
        save_word_report(report_data)
        print("✅ 完成!")
    except ImportError:
        print("需要安装: pip install python-docx")

if __name__ == "__main__":
    main()
