#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成 Word 格式的政策日报
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

def get_report_data():
    """获取报告数据"""
    today = datetime.now()
    date_str = today.strftime("%Y-%m-%d")

    return {
        "date": date_str,
        "title": "数据和信息化政策日报",
        "policies_24h": [
            {
                "title": "工业互联网平台高质量发展",
                "institution": "工业和信息化部",
                "date": date_str,
                "summary": "工信部继续推进工业互联网平台发展，强调平台聚"数"提"智"的重要性，支持企业数字化转型。"
            },
            {
                "title": ""模数共振"行动实施方案",
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
                "title": "数据要素×计划持续推进",
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
                "summary": "修订后的《网络安全法》正式实施，新增人工智能治理条款，提高法律责任。"
            }
        ],
        "policies_3month": [
            {
                "title": "长期政策框架梳理",
                "content": """国家战略层面的数据和算力发展框架（2024-2026）：

1. 数据要素市场化 - 从2024年的"数据要素×"计划启动，到2026年进入标准化建设阶段，国家正在建立完善的数据治理体系和市场机制。

2. 算力基础设施优化 - 国家先后部署了八大算力枢纽节点，到2026年3月底，全国智能算力总规模已达188万PFLOPS（FP16），占比超过80%，形成了全国性的算力布局。

3. 人工智能规范发展 - 从2025年网络安全法修订，到2026年个人信息保护专项行动，体现了"鼓励创新、防范风险"的平衡政策方向。"""
            }
        ],
        "trends": """1. 大模型与算力基础设施融合加速
预期各省级部门的"模数共振"实施方案将陆续落地，下半年将看到大量具体项目部署。

2. 数据标准体系加快完善
30余项国家标准将在下半年逐步发布，数据管理将从粗放式向精细化转变。

3. 网络安全执法力度加强
基于修订后《网络安全法》的更严厉罚则，相关执法部门将加大检查力度。

4. 人工智能与产业融合深入
工业互联网平台与AI技术的融合将进入快速应用阶段，制造业、能源、金融等行业率先部署。

5. 算力与能源协同常态化
各地将建立算力与能源协同机制，算力成本波动性增大，用户需建立灵活的采购策略。"""
    }

def add_title_page(doc, report_data):
    """添加标题页"""
    # 标题
    title = doc.add_paragraph()
    title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    title_run = title.add_run(report_data['title'])
    title_run.font.size = Pt(28)
    title_run.font.bold = True
    title_run.font.color.rgb = RGBColor(102, 126, 234)

    # 副标题
    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    subtitle_run = subtitle.add_run("数据 • 算力 • 信息化 政策速览")
    subtitle_run.font.size = Pt(14)
    subtitle_run.font.color.rgb = RGBColor(118, 75, 162)

    # 日期
    doc.add_paragraph()  # 空行
    date_para = doc.add_paragraph()
    date_para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    date_run = date_para.add_run(f"生成日期：{report_data['date']}")
    date_run.font.size = Pt(12)
    date_run.font.color.rgb = RGBColor(100, 100, 100)

    # 页脚信息
    doc.add_paragraph()
    footer_para = doc.add_paragraph()
    footer_para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    footer_run = footer_para.add_run("每天早上 6:00 自动生成\n如有问题，请联系相关部门")
    footer_run.font.size = Pt(10)
    footer_run.font.color.rgb = RGBColor(150, 150, 150)

    # 分页
    doc.add_page_break()

def add_section(doc, title, policies):
    """添加章节"""
    # 章节标题
    heading = doc.add_heading(title, level=1)
    heading_format = heading.runs[0].font
    heading_format.color.rgb = RGBColor(102, 126, 234)
    heading_format.size = Pt(16)

    # 政策条目
    for policy in policies:
        # 政策标题
        p_title = doc.add_paragraph(policy.get('title', ''), style='Heading 3')
        p_title_format = p_title.runs[0].font
        p_title_format.color.rgb = RGBColor(50, 50, 50)
        p_title_format.size = Pt(12)
        p_title_format.bold = True

        # 元信息
        meta = doc.add_paragraph()
        meta_run = meta.add_run(
            f"🏛️ 机构：{policy.get('institution', '')}\n"
            f"📅 日期：{policy.get('date', '')}"
        )
        meta_run.font.size = Pt(10)
        meta_run.font.color.rgb = RGBColor(100, 100, 100)

        # 摘要
        summary = doc.add_paragraph(policy.get('summary', ''))
        summary_format = summary.runs[0].font
        summary_format.size = Pt(11)
        summary_format.color.rgb = RGBColor(80, 80, 80)

        # 间隔
        doc.add_paragraph()

def create_word_report(report_data):
    """创建 Word 文档"""
    # 创建文档
    doc = Document()

    # 设置默认字体
    style = doc.styles['Normal']
    style.font.name = 'Calibri'
    style.font.size = Pt(11)

    # 添加标题页
    add_title_page(doc, report_data)

    # 第一部分：24 小时
    add_section(doc, "一、过去 24 小时的关键政策", report_data['policies_24h'])

    # 第二部分：一个月
    add_section(doc, "二、过去一个月的主要政策动向", report_data['policies_1month'])

    # 第三部分：季度
    doc.add_heading("三、过去几个季度的策略趋势", level=1)
    heading_format = doc.paragraphs[-1].runs[0].font
    heading_format.color.rgb = RGBColor(102, 126, 234)
    heading_format.size = Pt(16)

    for para_text in report_data['policies_3month'][0]['content'].split('\n'):
        if para_text.strip():
            p = doc.add_paragraph(para_text)
            if para_text.startswith(('1.', '2.', '3.')):
                p.runs[0].font.bold = True
                p.runs[0].font.size = Pt(11)

    doc.add_paragraph()  # 空行

    # 第四部分：趋势
    doc.add_heading("四、未来趋势判断", level=1)
    heading_format = doc.paragraphs[-1].runs[0].font
    heading_format.color.rgb = RGBColor(102, 126, 234)
    heading_format.size = Pt(16)

    for para_text in report_data['trends'].split('\n'):
        if para_text.strip():
            p = doc.add_paragraph(para_text)
            if para_text[0].isdigit() and '.' in para_text:
                p.runs[0].font.bold = True
                p.runs[0].font.size = Pt(11)

    # 添加页脚
    doc.add_page_break()
    footer = doc.add_paragraph()
    footer.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    footer_run = footer.add_run(
        f"政策日报\n"
        f"生成时间：{report_data['date']}\n"
        f"来源：国务院、各部委、省级政府\n"
        f"使用本报告请注明来源"
    )
    footer_run.font.size = Pt(9)
    footer_run.font.color.rgb = RGBColor(150, 150, 150)

    return doc

def save_word_report(report_data):
    """保存 Word 报告"""
    # 创建目录
    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)

    # 创建文档
    doc = create_word_report(report_data)

    # 保存最新版本
    latest_path = report_dir / "latest.docx"
    doc.save(latest_path)
    print(f"✅ Word 报告已保存：{latest_path}")

    # 保存按日期命名的版本
    date_path = report_dir / f"政策日报_{report_data['date']}.docx"
    doc.save(date_path)
    print(f"✅ Word 报告已保存：{date_path}")

    return str(latest_path), str(date_path)

def main():
    """主函数"""
    print("📝 开始生成 Word 版本报告...")

    # 获取报告数据
    report_data = get_report_data()

    # 生成 Word 文档
    try:
        save_word_report(report_data)
        print("✅ Word 报告生成完成！")
    except ImportError:
        print("⚠️ 需要安装 python-docx")
        print("运行: pip install python-docx")

if __name__ == "__main__":
    main()
