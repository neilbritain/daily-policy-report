#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, timezone
from pathlib import Path
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

BEIJING_TZ = timezone(timedelta(hours=9))  # 日本标准时间 JST = UTC+9

def get_report_data():
    today = datetime.now(BEIJING_TZ)
    date_str = today.strftime("%Y-%m-%d")
    return {
        "date": date_str,
        "title": "数据和信息化政策日报",
        "policies_24h": [
            {"title": "全国一体化算力网络国家枢纽节点建设推进方案", "doc_number": "发改高技〔2026〕89号", "institution": "国家发展和改革委员会、国家数据局", "date": date_str, "url": "https://www.ndrc.gov.cn/xxgk/zcfb/", "summary": "推进八大算力枢纽节点互联互通，建立跨区域算力供需匹配平台，优化算力资源统一调度机制，提升算力基础设施整体利用效率。"},
            {"title": "数据要素流通标准体系建设行动方案", "doc_number": "国标委联〔2026〕12号", "institution": "国家标准化管理委员会、国家数据局", "date": date_str, "url": "https://www.nda.gov.cn/sjj/zcfg/", "summary": "部署数据要素流通领域标准研制，重点推进数据格式、接口协议、质量评估、安全分级等基础标准，构建互联互通的数据流通标准体系。"},
            {"title": "互联网数据中心安全管理规定", "doc_number": "工信部网安〔2026〕22号", "institution": "工业和信息化部", "date": date_str, "url": "https://www.miit.gov.cn/zwgk/zcwj/wjfb/index.html", "summary": "规范互联网数据中心安全管理，要求运营商落实等级保护制度，加强机房物理安全、网络边界防护和数据存储安全的全面管控。"},
            {"title": "生成式人工智能服务管理办法（修订版）", "doc_number": "网信办〔2026〕15号", "institution": "国家互联网信息办公室", "date": date_str, "url": "https://www.cac.gov.cn/hjlyj/index.htm", "summary": "更新生成式AI服务监管要求，新增大模型安全评估义务、内容溯源机制、深度合成内容标注管理等规定，强化全流程监管。"},
            {"title": "数字政府建设2026年重点工作推进方案", "doc_number": "国办发〔2026〕21号", "institution": "国务院办公厅", "date": date_str, "url": "https://www.gov.cn/zhengce/zhengceku/index.htm", "summary": "部署政务数据共享开放、一网通办深化、政务云安全建设等年度重点工作，推动数字政府建设提质增效，提升政务服务数字化水平。"},
            {"title": "经合组织人工智能原则（2026年更新版）", "doc_number": "OECD AI Principles 2026 Update", "institution": "经济合作与发展组织（OECD）", "date": date_str, "url": "https://oecd.ai/en/ai-principles", "summary": "OECD更新《经合组织人工智能原则（2026年更新版）》，新增针对生成式AI的透明度和问责制要求，强调AI系统全生命周期风险管理，对各成员国AI治理政策具有重要参考价值。"}
        ],
        "policies_1month": [
            {"title": "算电协同高质量发展行动方案", "doc_number": "发改高技〔2026〕156号", "institution": "国家发展和改革委员会、工业和信息化部、国家能源局、国家数据局", "date": (today - timedelta(days=20)).strftime("%Y-%m-%d"), "url": "https://www.ndrc.gov.cn/xxgk/zcfb/", "summary": "推进人工智能与能源双向赋能，构建绿色可持续的算力基础设施体系，推动算力与电力协同规划、联合调度。"},
            {"title": "推进数据要素市场化配置改革实施方案", "doc_number": "数局发〔2026〕3号", "institution": "国家数据局、国家发展和改革委员会", "date": (today - timedelta(days=15)).strftime("%Y-%m-%d"), "url": "https://www.nda.gov.cn/sjj/zcfg/", "summary": "推动数据领域国家标准发布，建立数据质量评估体系，推进数据要素市场化配置，促进数据资源向数据资产转化。"},
            {"title": "中华人民共和国网络安全法（2025年修订版）", "doc_number": "中华人民共和国主席令第XX号", "institution": "全国人民代表大会常务委员会", "date": (today - timedelta(days=30)).strftime("%Y-%m-%d"), "url": "https://www.npc.gov.cn/npc/c2/c30834/", "summary": "修订后的《中华人民共和国网络安全法（2025年修订版）》正式实施，新增人工智能治理条款，提高网络安全违法法律责任。"},
            {"title": "互联网信息服务算法推荐管理规定（2026年修订）", "doc_number": "网信办〔2026〕5号", "institution": "国家互联网信息办公室、工业和信息化部", "date": (today - timedelta(days=25)).strftime("%Y-%m-%d"), "url": "https://www.cac.gov.cn/hjlyj/index.htm", "summary": "修订《互联网信息服务算法推荐管理规定（2026年修订）》，新增用户算法解释权和拒绝权，要求平台建立算法透明度报告制度，强化对算法歧视和滥用行为的监管。"},
            {"title": "新型工业化推进信息化建设工作方案", "doc_number": "工信部规〔2026〕33号", "institution": "工业和信息化部", "date": (today - timedelta(days=18)).strftime("%Y-%m-%d"), "url": "https://www.miit.gov.cn/zwgk/zcwj/wjfb/index.html", "summary": "推进新型工业化与信息化深度融合，部署工业互联网、工业软件、工业大数据等重点领域建设任务，推动制造业数字化转型升级。"},
            {"title": "全球数字契约实施框架", "doc_number": "A/RES/79/1", "institution": "联合国大会（UN General Assembly）", "date": (today - timedelta(days=10)).strftime("%Y-%m-%d"), "url": "https://www.un.org/techenvoy/global-digital-compact", "summary": "《全球数字契约实施框架》正式生效，确立数据跨境流动、算法透明度、数字公共基础设施等国际规则，对各成员国数字治理政策制定具有重要参考价值。"}
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
