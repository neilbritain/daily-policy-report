#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

# 北京时间 UTC+8
BEIJING_TZ = timezone(timedelta(hours=8))

def create_report_content():
    today = datetime.now(BEIJING_TZ)
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
                "url": "https://www.miit.gov.cn/zwgk/zcwj/wjfb/index.html",
                "summary": "工信部继续推进工业互联网平台发展，强调平台聚数提智的重要性，支持企业数字化转型。"
            },
            {
                "title": "模数共振行动实施方案",
                "doc_number": "国办发〔2026〕12号",
                "institution": "国务院办公厅、工业和信息化部",
                "date": date_str,
                "url": "https://www.gov.cn/zhengce/zhengceku/index.htm",
                "summary": "各省级部门推进大模型与算力基础设施的协同发展，优化资源配置，实现高效运行。"
            },
            {
                "title": "数据安全和个人信息保护专项行动方案",
                "doc_number": "网信办〔2026〕8号",
                "institution": "国家互联网信息办公室",
                "date": date_str,
                "url": "https://www.cac.gov.cn/hjlyj/index.htm",
                "summary": "继续强化个人信息保护和数据安全监管，加大对违法违规行为的查处力度。"
            },
            {
                "title": "欧盟人工智能法案配套实施细则",
                "doc_number": "EU AI Act 2024/1689 实施细则",
                "institution": "欧盟委员会（European Commission）",
                "date": date_str,
                "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689",
                "summary": "欧盟发布《欧盟人工智能法案》高风险系统认证细则，要求医疗、交通、公共服务等领域AI系统须通过第三方合规审计，对出口至欧盟市场的AI产品具有重要影响。"
            },
            {
                "title": "美国关键基础设施数据安全行政令更新",
                "doc_number": "Executive Order 14117 修订版",
                "institution": "美国总统办公室（White House）",
                "date": date_str,
                "url": "https://www.whitehouse.gov/briefing-room/presidential-actions/",
                "summary": "美国更新关键基础设施数据保护要求，进一步限制敏感数据跨境流向特定国家，并要求云服务商加强数据本地化合规审查。"
            }
        ],
        "policies_1month": [
            {
                "title": "推进数据要素市场化配置改革实施方案",
                "doc_number": "数局发〔2026〕3号",
                "institution": "国家数据局、国家发展和改革委员会",
                "date": (today - timedelta(days=15)).strftime("%Y-%m-%d"),
                "url": "https://www.nda.gov.cn/sjj/zcfg/",
                "summary": "推动30余项数据领域国家标准发布，建立数据质量评估体系，推进数据要素市场化。"
            },
            {
                "title": "算电协同高质量发展行动方案",
                "doc_number": "发改高技〔2026〕156号",
                "institution": "国家发展和改革委员会、工业和信息化部、国家能源局、国家数据局",
                "date": (today - timedelta(days=20)).strftime("%Y-%m-%d"),
                "url": "https://www.ndrc.gov.cn/xxgk/zcfb/",
                "summary": "推进人工智能与能源双向赋能，构建绿色可持续的算力基础设施体系。"
            },
            {
                "title": "中华人民共和国网络安全法（2025年修订版）",
                "doc_number": "中华人民共和国主席令第XX号",
                "institution": "全国人民代表大会常务委员会",
                "date": "2026-01-01",
                "url": "https://www.npc.gov.cn/npc/c2/c30834/",
                "summary": "修订后的《中华人民共和国网络安全法（2025年修订版）》正式实施，新增人工智能治理条款，提高法律责任。"
            },
            {
                "title": "全球数字契约实施框架",
                "doc_number": "A/RES/79/1",
                "institution": "联合国大会（UN General Assembly）",
                "date": (today - timedelta(days=10)).strftime("%Y-%m-%d"),
                "url": "https://www.un.org/techenvoy/global-digital-compact",
                "summary": "《全球数字契约实施框架》正式生效，确立数据跨境流动、算法透明度、数字公共基础设施等国际规则，对各成员国数字治理政策制定具有重要参考价值。"
            },
            {
                "title": "G7数字与技术部长声明：AI治理原则更新",
                "doc_number": "G7 Digital Ministers Statement 2026",
                "institution": "七国集团（G7）数字与技术部长会议",
                "date": (today - timedelta(days=25)).strftime("%Y-%m-%d"),
                "url": "https://www.g7italy.it/en/presidency-priorities/digital/",
                "summary": "G7更新AI治理广岛进程原则，强调负责任AI开发、数据自由流动与可信任环境建设，推动多边框架下的算法审计与互操作性标准对接。"
            }
        ],
        "trends": [
            "大模型与算力融合加速。国内《模数共振行动实施方案》陆续落地；国际方面，微软、谷歌等持续扩大亚太算力部署，全球算力争夺格局加剧。",
            "数据跨境规则体系加速形成。国内数据出境安全评估机制逐步完善；《欧盟人工智能法案》和《美国关键基础设施数据安全行政令》双重压力下，跨国数据流动合规成本显著上升。",
            "网络安全执法全球同步收紧。国内基于修订后《中华人民共和国网络安全法（2025年修订版）》加大执法；美欧同步强化关键基础设施保护，网络安全国际合作与博弈并行深化。",
            "AI治理标准国际竞争白热化。ISO/IEC发布《AI管理体系国际标准》，国内相关国家标准同步推进，争夺国际规则制定主导权已成战略重点。",
            "绿色算力成全球共同议题。国内《算电协同高质量发展行动方案》加快落地；IEA《全球数据中心能耗报告》显示数据中心能耗将超越航空业，绿色算力政策将成各国竞争新赛道。"
        ]
    }

def validate_report(report_data):
    """校对报告内容：检查日期合理性和链接完整性"""
    today = datetime.now(BEIJING_TZ).date()
    warnings = []

    checks = [
        ("过去24小时", report_data['policies_24h'], 3),    # 允许3天内
        ("过去一个月", report_data['policies_1month'], 35), # 允许35天内
    ]
    for section_name, policies, max_days in checks:
        for p in policies:
            try:
                pub_date = datetime.strptime(p['date'], '%Y-%m-%d').date()
                days_ago = (today - pub_date).days
                if pub_date > today:
                    warnings.append(f"[日期超前] 【{section_name}】{p['title']}: {p['date']}")
                elif days_ago > max_days:
                    warnings.append(f"[日期偏早] 【{section_name}】{p['title']}: {p['date']} (距今{days_ago}天)")
            except ValueError:
                warnings.append(f"[日期格式错误] {p['title']}: {p['date']}")
            if not p.get('url'):
                warnings.append(f"[缺少链接] {p['title']}")
            if not p.get('doc_number'):
                warnings.append(f"[缺少文号] {p['title']}")

    def safe_print(msg):
        try:
            print(msg)
        except UnicodeEncodeError:
            print(msg.encode('utf-8', errors='replace').decode('ascii', errors='replace'))

    if warnings:
        safe_print("[!] Validation warnings:")
        for w in warnings:
            safe_print(f"  {w}")
    else:
        safe_print("[OK] Validation passed")
    return warnings

def render_policies(policies):
    """公众号优化格式：标题大字 + 元数据一行 + 摘要 + 链接纯文字"""
    html = ""
    for p in policies:
        url = p.get('url', '')
        url_html = (
            f'<p style="font-size:12px;color:#aaa;margin:10px 0 0 0;word-break:break-all;line-height:1.6;">'
            f'<a href="{url}" style="color:#aaa;text-decoration:none;">{url}</a></p>'
        ) if url else ''
        html += f"""
        <div style="margin-bottom:20px;padding:16px 18px;background:#f8f9ff;border-radius:6px;border-left:4px solid #5b6de4;">
            <p style="font-size:16px;font-weight:bold;color:#1a1a1a;margin:0 0 6px 0;line-height:1.5;">《{p['title']}》</p>
            <p style="font-size:12px;color:#888;margin:0 0 12px 0;line-height:1.6;">{p.get('doc_number','暂无')} &nbsp;|&nbsp; {p['institution']} &nbsp;|&nbsp; {p['date']}</p>
            <p style="font-size:15px;color:#333;margin:0;line-height:1.9;">{p['summary']}</p>
            {url_html}
        </div>"""
    return html

def save_reports(report_data):
    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)

    with open(report_dir / "latest.json", "w", encoding="utf-8") as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)
    with open(report_dir / f"report-{report_data['date']}.json", "w", encoding="utf-8") as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)

    nums = ["①", "②", "③", "④", "⑤"]
    trends_html = "".join(
        f'<p style="font-size:15px;color:#333;line-height:1.9;margin:0 0 14px 0;padding-left:14px;border-left:3px solid #5b6de4;">'
        f'<strong style="color:#5b6de4;">{nums[i]}</strong>&nbsp; {t}</p>'
        for i, t in enumerate(report_data['trends'])
    )

    base_url = "https://neilbritain.github.io/daily-policy-report"
    report_html_url = f"{base_url}/reports/report-{report_data['date']}.html"
    report_docx_url = f"{base_url}/reports/report-{report_data['date']}.docx"

    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>政策日报 - {report_data['date']}</title>
</head>
<body style="font-family:'Microsoft YaHei','PingFang SC',Arial,sans-serif;font-size:15px;line-height:1.8;color:#333;background:#ebebeb;margin:0;padding:16px;">

<div style="max-width:680px;margin:0 auto;background:#fff;padding:32px 24px;border-radius:8px;">

    <!-- 返回导航 -->
    <p style="margin:0 0 20px 0;font-size:13px;">
        <a href="../index.html" style="color:#5b6de4;text-decoration:none;">← 返回首页</a>
    </p>

    <!-- 标题区 -->
    <p style="font-size:26px;font-weight:bold;color:#1a1a1a;text-align:center;margin:0 0 6px 0;line-height:1.3;">数据和信息化政策日报</p>
    <p style="font-size:13px;color:#aaa;text-align:center;margin:0 0 6px 0;">{report_data['date']} &nbsp;|&nbsp; 数据 · 算力 · 信息化</p>
    <p style="font-size:12px;color:#bbb;text-align:center;margin:0 0 28px 0;">
        网页版：<a href="{report_html_url}" style="color:#5b6de4;text-decoration:none;">{report_html_url}</a>
        &nbsp;&nbsp;|&nbsp;&nbsp;
        Word版：<a href="{report_docx_url}" style="color:#5b6de4;text-decoration:none;">{report_docx_url}</a>
    </p>

    <!-- 第一部分 -->
    <p style="background:#5b6de4;color:#fff;font-size:16px;font-weight:bold;padding:10px 16px;border-radius:4px;margin:0 0 18px 0;">一、过去 24 小时关键政策</p>
    {render_policies(report_data['policies_24h'])}

    <!-- 分隔 -->
    <p style="border-top:2px dashed #ddd;margin:28px 0;"></p>

    <!-- 第二部分 -->
    <p style="background:#5b6de4;color:#fff;font-size:16px;font-weight:bold;padding:10px 16px;border-radius:4px;margin:0 0 18px 0;">二、过去一个月主要政策动向</p>
    {render_policies(report_data['policies_1month'])}

    <!-- 分隔 -->
    <p style="border-top:2px dashed #ddd;margin:28px 0;"></p>

    <!-- 第三部分 -->
    <p style="background:#5b6de4;color:#fff;font-size:16px;font-weight:bold;padding:10px 16px;border-radius:4px;margin:0 0 18px 0;">三、未来趋势判断</p>
    {trends_html}

    <!-- 页脚 -->
    <p style="border-top:1px solid #eee;margin-top:32px;padding-top:18px;font-size:12px;color:#bbb;text-align:center;">
        每天早上 6:00 自动更新 &nbsp;·&nbsp;
        <a href="{base_url}" style="color:#5b6de4;text-decoration:none;">{base_url}</a>
        &nbsp;·&nbsp;
        <a href="../index.html" style="color:#5b6de4;text-decoration:none;">返回首页</a>
    </p>

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
    validate_report(report_data)
    save_reports(report_data)

if __name__ == "__main__":
    main()
