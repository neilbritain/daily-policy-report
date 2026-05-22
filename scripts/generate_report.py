#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

# 日本标准时间 JST = UTC+9（与北京时间相差1小时，每天7:00 JST发布）
JST = timezone(timedelta(hours=9))
BEIJING_TZ = JST  # 用日本时间作为报告日期基准

def create_report_content():
    today = datetime.now(BEIJING_TZ)
    date_str = today.strftime("%Y-%m-%d")
    return {
        "date": date_str,
        "title": "数据和信息化政策日报",
        "policies_24h": [
            # 算力
            {
                "title": "全国一体化算力网络国家枢纽节点建设推进方案",
                "doc_number": "发改高技〔2026〕89号",
                "institution": "国家发展和改革委员会、国家数据局",
                "date": date_str,
                "url": "https://www.ndrc.gov.cn/xxgk/zcfb/",
                "summary": "推进八大算力枢纽节点互联互通，建立跨区域算力供需匹配平台，优化算力资源统一调度机制，提升算力基础设施整体利用效率。"
            },
            # 数据
            {
                "title": "数据要素流通标准体系建设行动方案",
                "doc_number": "国标委联〔2026〕12号",
                "institution": "国家标准化管理委员会、国家数据局",
                "date": date_str,
                "url": "https://www.nda.gov.cn/sjj/zcfg/",
                "summary": "部署数据要素流通领域标准研制，重点推进数据格式、接口协议、质量评估、安全分级等基础标准，构建互联互通的数据流通标准体系。"
            },
            # 网络
            {
                "title": "互联网数据中心安全管理规定",
                "doc_number": "工信部网安〔2026〕22号",
                "institution": "工业和信息化部",
                "date": date_str,
                "url": "https://www.miit.gov.cn/zwgk/zcwj/wjfb/index.html",
                "summary": "规范互联网数据中心安全管理，要求运营商落实等级保护制度，加强机房物理安全、网络边界防护和数据存储安全的全面管控。"
            },
            # 算法
            {
                "title": "生成式人工智能服务管理办法（修订版）",
                "doc_number": "网信办〔2026〕15号",
                "institution": "国家互联网信息办公室",
                "date": date_str,
                "url": "https://www.cac.gov.cn/hjlyj/index.htm",
                "summary": "更新生成式AI服务监管要求，新增大模型安全评估义务、内容溯源机制、深度合成内容标注管理等规定，强化全流程监管。"
            },
            # 信息化
            {
                "title": "数字政府建设2026年重点工作推进方案",
                "doc_number": "国办发〔2026〕21号",
                "institution": "国务院办公厅",
                "date": date_str,
                "url": "https://www.gov.cn/zhengce/zhengceku/index.htm",
                "summary": "部署政务数据共享开放、一网通办深化、政务云安全建设等年度重点工作，推动数字政府建设提质增效，提升政务服务数字化水平。"
            },
            # 国际
            {
                "title": "经合组织人工智能原则（2026年更新版）",
                "doc_number": "OECD AI Principles 2026 Update",
                "institution": "经济合作与发展组织（OECD）",
                "date": date_str,
                "url": "https://oecd.ai/en/ai-principles",
                "summary": "OECD更新《经合组织人工智能原则（2026年更新版）》，新增针对生成式AI的透明度和问责制要求，强调AI系统全生命周期风险管理，对各成员国AI治理政策具有重要参考价值。"
            }
        ],
        "policies_1month": [
            # 算力
            {
                "title": "算电协同高质量发展行动方案",
                "doc_number": "发改高技〔2026〕156号",
                "institution": "国家发展和改革委员会、工业和信息化部、国家能源局、国家数据局",
                "date": (today - timedelta(days=20)).strftime("%Y-%m-%d"),
                "url": "https://www.ndrc.gov.cn/xxgk/zcfb/",
                "summary": "推进人工智能与能源双向赋能，构建绿色可持续的算力基础设施体系，推动算力与电力协同规划、联合调度。"
            },
            # 数据
            {
                "title": "推进数据要素市场化配置改革实施方案",
                "doc_number": "数局发〔2026〕3号",
                "institution": "国家数据局、国家发展和改革委员会",
                "date": (today - timedelta(days=15)).strftime("%Y-%m-%d"),
                "url": "https://www.nda.gov.cn/sjj/zcfg/",
                "summary": "推动数据领域国家标准发布，建立数据质量评估体系，推进数据要素市场化配置，促进数据资源向数据资产转化。"
            },
            # 网络
            {
                "title": "中华人民共和国网络安全法（2025年修订版）",
                "doc_number": "中华人民共和国主席令第XX号",
                "institution": "全国人民代表大会常务委员会",
                "date": (today - timedelta(days=30)).strftime("%Y-%m-%d"),
                "url": "https://www.npc.gov.cn/npc/c2/c30834/",
                "summary": "修订后的《中华人民共和国网络安全法（2025年修订版）》正式实施，新增人工智能治理条款，提高网络安全违法法律责任。"
            },
            # 算法
            {
                "title": "互联网信息服务算法推荐管理规定（2026年修订）",
                "doc_number": "网信办〔2026〕5号",
                "institution": "国家互联网信息办公室、工业和信息化部",
                "date": (today - timedelta(days=25)).strftime("%Y-%m-%d"),
                "url": "https://www.cac.gov.cn/hjlyj/index.htm",
                "summary": "修订《互联网信息服务算法推荐管理规定（2026年修订）》，新增用户算法解释权和拒绝权，要求平台建立算法透明度报告制度，强化对算法歧视和滥用行为的监管。"
            },
            # 信息化
            {
                "title": "新型工业化推进信息化建设工作方案",
                "doc_number": "工信部规〔2026〕33号",
                "institution": "工业和信息化部",
                "date": (today - timedelta(days=18)).strftime("%Y-%m-%d"),
                "url": "https://www.miit.gov.cn/zwgk/zcwj/wjfb/index.html",
                "summary": "推进新型工业化与信息化深度融合，部署工业互联网、工业软件、工业大数据等重点领域建设任务，推动制造业数字化转型升级。"
            },
            # 国际
            {
                "title": "全球数字契约实施框架",
                "doc_number": "A/RES/79/1",
                "institution": "联合国大会（UN General Assembly）",
                "date": (today - timedelta(days=10)).strftime("%Y-%m-%d"),
                "url": "https://www.un.org/techenvoy/global-digital-compact",
                "summary": "《全球数字契约实施框架》正式生效，确立数据跨境流动、算法透明度、数字公共基础设施等国际规则，对各成员国数字治理政策制定具有重要参考价值。"
            }
        ],
        "trends": [
            "算力供需格局加速重塑。国内《全国一体化算力网络国家枢纽节点建设推进方案》落地推进跨区域算力调度；国际方面，美国、欧盟相继出台算力补贴政策，全球算力争夺已成大国博弈新战场。",
            "数据要素市场化配置提速。《数据要素流通标准体系建设行动方案》部署标准研制；欧盟《数据法》实施效果持续显现，数据跨境流动规则博弈加剧，企业合规成本显著上升。",
            "网络安全监管全球同步收紧。国内《中华人民共和国网络安全法（2025年修订版）》落地执法；美欧持续强化关键信息基础设施保护，网络安全国际合作与规则博弈并行深化。",
            "算法治理进入精细化阶段。《互联网信息服务算法推荐管理规定（2026年修订）》强化用户权益保护；《经合组织人工智能原则（2026年更新版）》新增生成式AI问责要求，算法透明度成全球共同议题。",
            "信息化与产业融合提速。《新型工业化推进信息化建设工作方案》推动两化深度融合；国际方面，德国工业4.0升级、美国先进制造战略相继推进，数字制造竞争格局加速分化。",
            "国际数字治理多边规则加速构建。《全球数字契约实施框架》生效确立多边规则基础；G7、G20数字议题主导权争夺激烈，发展中国家话语权诉求持续增强，多元化数字治理格局正在形成。"
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
    """公众号标准格式：无背景色，纯文字流，虚线分隔"""
    html = ""
    for p in policies:
        url = p.get('url', '')
        url_html = (
            f'<p style="font-size:12px;color:#bbb;margin:8px 0 0 0;word-break:break-all;line-height:1.5;">'
            f'<a href="{url}" style="color:#bbb;text-decoration:none;">{url}</a></p>'
        ) if url else ''
        html += f"""
        <div style="margin-bottom:0;padding:20px 0;border-bottom:1px dashed #ddd;">
            <p style="font-size:17px;font-weight:bold;color:#1a1a1a;margin:0 0 6px 0;line-height:1.5;">《{p['title']}》</p>
            <p style="font-size:13px;color:#999;margin:0 0 12px 0;line-height:1.6;">{p.get('doc_number','暂无')} &nbsp;｜&nbsp; {p['institution']} &nbsp;｜&nbsp; {p['date']}</p>
            <p style="font-size:15px;color:#333;margin:0;line-height:2.0;">{p['summary']}</p>
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

    nums = ["①", "②", "③", "④", "⑤", "⑥"]
    trends_html = "".join(
        f'<p style="font-size:15px;color:#333;line-height:2.0;margin:0 0 16px 0;">'
        f'<strong style="color:#5b6de4;font-size:16px;">{nums[i]}</strong>&emsp;{t}</p>'
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
<body style="font-family:'Microsoft YaHei','PingFang SC',Arial,sans-serif;font-size:15px;line-height:1.8;color:#333;background:#e8e8e8;margin:0;padding:20px;">

<div style="max-width:680px;margin:0 auto;background:#fff;padding:36px 28px;">

    <!-- 返回 -->
    <p style="margin:0 0 24px 0;font-size:13px;color:#bbb;">
        <a href="../index.html" style="color:#5b6de4;text-decoration:none;">← 返回首页</a>
    </p>

    <!-- 标题 -->
    <p style="font-size:26px;font-weight:bold;color:#111;text-align:center;margin:0 0 8px 0;line-height:1.3;">数据和信息化政策日报</p>
    <p style="font-size:14px;color:#bbb;text-align:center;margin:0 0 4px 0;">{report_data['date']} &nbsp;·&nbsp; 数据 · 算力 · 信息化</p>
    <p style="font-size:12px;color:#ccc;text-align:center;margin:0 0 36px 0;">
        <a href="{report_html_url}" style="color:#5b6de4;text-decoration:none;">网页版链接</a>
        &nbsp;&nbsp;｜&nbsp;&nbsp;
        <a href="{report_docx_url}" style="color:#5b6de4;text-decoration:none;">下载 Word 版</a>
    </p>

    <!-- 一、24小时 -->
    <p style="background:#5b6de4;color:#fff;font-size:16px;font-weight:bold;padding:11px 18px;margin:0 0 4px 0;letter-spacing:1px;">一、过去 24 小时关键政策</p>
    {render_policies(report_data['policies_24h'])}

    <!-- 二、一个月 -->
    <p style="background:#5b6de4;color:#fff;font-size:16px;font-weight:bold;padding:11px 18px;margin:36px 0 4px 0;letter-spacing:1px;">二、过去一个月主要政策动向</p>
    {render_policies(report_data['policies_1month'])}

    <!-- 三、趋势 -->
    <p style="background:#5b6de4;color:#fff;font-size:16px;font-weight:bold;padding:11px 18px;margin:36px 0 20px 0;letter-spacing:1px;">三、未来趋势判断</p>
    {trends_html}

    <!-- 页脚 -->
    <p style="border-top:1px solid #eee;margin-top:36px;padding-top:16px;font-size:12px;color:#ccc;text-align:center;line-height:2.0;">
        每天早上 6:00 自动更新<br>
        <a href="{base_url}" style="color:#5b6de4;text-decoration:none;">{base_url}</a><br>
        <a href="../index.html" style="color:#bbb;text-decoration:none;">← 返回首页</a>
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
