#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日政策报告生成脚本 v3.2
搜索引擎抓取 + DeepSeek API 生成真实内容
覆盖主题：算力、人工智能、数据、算法、网络、信息化、数字化
"""
import os
import json
import re
import time
import requests
from datetime import datetime, timedelta, timezone
from pathlib import Path

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False

BEIJING_TZ = timezone(timedelta(hours=8))

# ──────────────────────────────────────────────
# 0. 工具函数
# ──────────────────────────────────────────────

import sys
import io

# 强制 stdout 使用 UTF-8（Windows 兼容）
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

def safe_print(msg: str):
    try:
        print(msg, flush=True)
    except Exception:
        print(msg.encode("ascii", "replace").decode("ascii"), flush=True)


def search_duckduckgo(query: str, max_results: int = 6) -> str:
    """DuckDuckGo HTML 搜索（无需 API Key）"""
    if not HAS_BS4:
        return f"[bs4 未安装，跳过搜索: {query}]"

    import urllib.parse
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "Chrome/122.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "zh-CN,zh;q=0.9",
    }
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}&kl=cn-zh"
    try:
        r = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(r.text, "html.parser")
        items = []
        for div in soup.select(".result")[:max_results]:
            title = div.select_one(".result__a")
            snippet = div.select_one(".result__snippet")
            link = div.select_one(".result__url")
            if title:
                t = title.get_text(strip=True)
                s = snippet.get_text(strip=True) if snippet else ""
                u = link.get_text(strip=True) if link else ""
                items.append(f"· {t}\n  {u}\n  {s}")
        return "\n\n".join(items) if items else "(未找到结果)"
    except Exception as e:
        return f"(搜索异常: {e})"


def scrape_gov_news(today: datetime) -> str:
    """抓取主要政府官网新闻列表"""
    if not HAS_BS4:
        return ""

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; PolicyMonitor/3.0)",
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }
    sources = [
        {
            "name": "国家数据局",
            "url": "https://www.nda.gov.cn/sjj/zcfg/",
            "base": "https://www.nda.gov.cn",
        },
        {
            "name": "工业和信息化部",
            "url": "https://www.miit.gov.cn/zwgk/zcwj/wjfb/index.html",
            "base": "https://www.miit.gov.cn",
        },
        {
            "name": "国家互联网信息办公室",
            "url": "https://www.cac.gov.cn/hjlyj/index.htm",
            "base": "https://www.cac.gov.cn",
        },
    ]
    results = []
    keywords = ("通知", "规定", "办法", "方案", "意见", "规划", "条例", "政策", "标准")
    for src in sources:
        try:
            r = requests.get(src["url"], headers=headers, timeout=15)
            r.encoding = r.apparent_encoding or "utf-8"
            soup = BeautifulSoup(r.text, "html.parser")
            items = []
            for a in soup.find_all("a", href=True):
                text = a.get_text(strip=True)
                href = a["href"]
                if len(text) > 8 and any(kw in text for kw in keywords):
                    if href.startswith("/"):
                        href = src["base"] + href
                    items.append(f"  - {text} | {href}")
            if items:
                results.append(f"【{src['name']}】\n" + "\n".join(items[:8]))
        except Exception as e:
            results.append(f"【{src['name']}】抓取失败: {e}")
    return "\n\n".join(results)


def collect_all_data(today: datetime) -> str:
    """汇总所有搜索和抓取结果"""
    ym = today.strftime("%Y年%m月")
    ymd = today.strftime("%Y年%m月%d日")

    # 多关键词搜索，覆盖：算力、人工智能、数据、算法、网络、信息化、数字化
    queries = [
        f"国务院 国家数据局 工信部 网信办 最新政策通知 {ym}",
        f"算力 算力网络 东数西算 算力基础设施 政策 {ym}",
        f"人工智能 大模型 生成式AI 监管 政策 {ym}",
        f"数据要素 数据安全 数据治理 数据资产 政策 {ym}",
        f"算法治理 算法推荐 算法备案 规定 {ym}",
        f"网络安全 等级保护 关键信息基础设施 政策 {ym}",
        f"信息化 数字政府 数字中国 政务数据 {ym}",
        f"数字化转型 工业互联网 数字经济 政策 {ym}",
        f"site:gov.cn 通知 规定 办法 {ym}",
    ]

    parts = [f"今天是 {ymd}。\n"]

    safe_print("  >搜索政策关键词...")
    for i, q in enumerate(queries, 1):
        safe_print(f"    [{i}/{len(queries)}] {q[:50]}")
        result = search_duckduckgo(q)
        parts.append(f"── 搜索「{q[:40]}」──\n{result}")
        time.sleep(2)

    safe_print("  >抓取政府官网...")
    gov_text = scrape_gov_news(today)
    if gov_text:
        parts.append(f"── 官网抓取 ──\n{gov_text}")

    return "\n\n".join(parts)


# ──────────────────────────────────────────────
# 2. Claude API 生成报告
# ──────────────────────────────────────────────

REPORT_PROMPT = """你是一名严谨的政策分析助手，今天是 {date_str}。

以下是从网络搜索到的原始数据：

{raw_data}

━━━ 收录范围 ━━━
以下主题均可纳入（不限于）：
算力 · 人工智能 · 数据要素 · 数据安全 · 算法治理 · 网络安全 · 信息化 · 数字化转型 · 数字政府 · 数字经济 · 工业互联网 · 5G · 物联网 · 区块链 · 智能计算 · 绿色算力

━━━ 真实性要求（违反则整条删除）━━━

【真实性】
- 只能收录搜索数据中明确出现的政策，禁止根据"常识"或"推断"补充任何未在搜索结果中出现的政策
- 文件字号（如"国办发〔2026〕15号"）必须来自搜索结果原文，搜索结果未提及字号时，doc_number 填"暂无"，禁止编造
- 发文日期必须来自搜索结果，搜索结果未明确日期时，date 填报告日期 {date_str}，禁止推算或捏造

【时效性】
- policies_24h：仅收录发布日期在 {date_3d_ago} 之后的政策（即近 3 天内）
- policies_1month：仅收录发布日期在 {date_30d_ago} 之后的政策（即近 30 天内）
- 日期早于上述范围的政策一律移除，不得填入

【URL】
- 能找到来源链接则填写，找不到一律填空字符串 ""，禁止填写推测性链接

【数量】
- policies_24h：3~6 条（搜索结果不足时可少于 6 条，禁止凑数）
- policies_1month：3~6 条（同上）
- trends：基于已收录政策客观分析，共 6 条，每条 80 字以内

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

仅返回以下格式的 JSON，不加任何 markdown 代码块：
{{
  "policies_24h": [
    {{
      "title": "政策标题（不含书名号）",
      "doc_number": "发文字号（来源中无字号则填暂无）",
      "institution": "发布机构全称",
      "date": "YYYY-MM-DD",
      "url": "官方来源链接（无则填空字符串）",
      "summary": "核心内容摘要，50 字以内，不得虚构"
    }}
  ],
  "policies_1month": [
    {{ 同上格式 }}
  ],
  "trends": [
    "趋势 1：基于已收录政策的客观判断",
    "趋势 2：", "趋势 3：", "趋势 4：", "趋势 5：", "趋势 6："
  ]
}}"""


def call_llm_api(raw_data: str, today: datetime) -> dict:
    """
    调用大模型 API 生成报告 JSON
    优先使用 DEEPSEEK_API_KEY，没有则自动切换到 ANTHROPIC_API_KEY
    """
    date_str    = today.strftime("%Y-%m-%d")
    date_3d_ago  = (today - timedelta(days=3)).strftime("%Y-%m-%d")
    date_30d_ago = (today - timedelta(days=30)).strftime("%Y-%m-%d")
    prompt = REPORT_PROMPT.format(
        raw_data     = raw_data[:12000],
        date_str     = date_str,
        date_3d_ago  = date_3d_ago,
        date_30d_ago = date_30d_ago,
    )

    deepseek_key = os.environ.get("DEEPSEEK_API_KEY")
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")

    if deepseek_key:
        safe_print("  >使用 DeepSeek API")
        text = _call_deepseek(deepseek_key, prompt)
    elif anthropic_key:
        safe_print("  >未找到 DEEPSEEK_API_KEY，切换到 Anthropic API")
        text = _call_anthropic(anthropic_key, prompt)
    else:
        raise RuntimeError("未设置 DEEPSEEK_API_KEY 或 ANTHROPIC_API_KEY，至少需要其中一个")

    # 提取 JSON（去掉 markdown 代码块包裹）
    m = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
    if m:
        text = m.group(1)
    else:
        m = re.search(r"```\s*(.*?)\s*```", text, re.DOTALL)
        if m:
            text = m.group(1)

    # 截取最外层 { }
    start = text.find("{")
    end = text.rfind("}") + 1
    if 0 <= start < end:
        text = text[start:end]

    data = json.loads(text)
    data["date"] = today.strftime("%Y-%m-%d")
    data["title"] = "数据和信息化政策日报"

    # ── 后处理：自动清理超期 / 日期异常条目 ──
    data = _validate_dates(data, today)
    return data


def _validate_dates(data: dict, today: datetime) -> dict:
    """
    日期校验：只删除明确超前（日期在今天之后）的条目，其余只打警告不删除。
    算力、AI、数据、算法、网络、信息化、数字化等相关政策均可纳入，不做时效截断。
    """
    today_date = today.date()

    for key in ("policies_24h", "policies_1month"):
        original = data.get(key, [])
        cleaned = []
        for p in original:
            raw_date = p.get("date", "")
            try:
                pub = datetime.strptime(raw_date, "%Y-%m-%d").date()
            except ValueError:
                # 日期格式错误 → 用报告日期兜底，保留条目
                safe_print(f"  [warn] 日期格式异常，已修正为今天: {p.get('title','?')}")
                p["date"] = today.strftime("%Y-%m-%d")
                cleaned.append(p)
                continue

            if pub > today_date:
                # 未来日期 → 唯一真正删除的情况
                safe_print(f"  [!] 日期超前，已移除: {p.get('title','?')} | {raw_date}")
                continue

            days_ago = (today_date - pub).days
            if key == "policies_24h" and days_ago > 14:
                safe_print(f"  [warn] {key} 条目距今 {days_ago} 天，建议核查: {p.get('title','?')}")
            elif key == "policies_1month" and days_ago > 60:
                safe_print(f"  [warn] {key} 条目距今 {days_ago} 天，建议核查: {p.get('title','?')}")

            cleaned.append(p)   # 只警告，不删除

        data[key] = cleaned

    return data


def _call_deepseek(api_key: str, prompt: str) -> str:
    """DeepSeek Chat API（OpenAI 兼容格式）"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 4096,
        "temperature": 0.3,
    }
    for attempt in range(1, 3):
        try:
            resp = requests.post(
                "https://api.deepseek.com/chat/completions",
                headers=headers, json=payload, timeout=120,
            )
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:
            safe_print(f"  [!] DeepSeek 调用失败（第 {attempt} 次）: {e}")
            if attempt == 2:
                raise
            time.sleep(5)


def _call_anthropic(api_key: str, prompt: str) -> str:
    """Anthropic Claude API"""
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    payload = {
        "model": "claude-3-5-sonnet-20241022",
        "max_tokens": 4096,
        "messages": [{"role": "user", "content": prompt}],
    }
    for attempt in range(1, 3):
        try:
            resp = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers, json=payload, timeout=120,
            )
            resp.raise_for_status()
            return resp.json()["content"][0]["text"].strip()
        except Exception as e:
            safe_print(f"  [!] Anthropic 调用失败（第 {attempt} 次）: {e}")
            if attempt == 2:
                raise
            time.sleep(5)


# ──────────────────────────────────────────────
# 3. HTML 渲染
# ──────────────────────────────────────────────

def render_policies(policies: list) -> str:
    html = ""
    for p in policies:
        url = p.get("url", "")
        url_html = (
            f'<p style="font-size:12px;color:#bbb;margin:8px 0 0;word-break:break-all;">'
            f'<a href="{url}" style="color:#bbb;text-decoration:none;">{url}</a></p>'
        ) if url else ""
        html += f"""
<div style="padding:20px 0;border-bottom:1px dashed #ddd;">
  <p style="font-size:17px;font-weight:bold;color:#1a1a1a;margin:0 0 6px;">《{p["title"]}》</p>
  <p style="font-size:13px;color:#999;margin:0 0 12px;">{p.get("doc_number","暂无")} ｜ {p["institution"]} ｜ {p["date"]}</p>
  <p style="font-size:15px;color:#333;margin:0;line-height:2.0;">{p["summary"]}</p>
  {url_html}
</div>"""
    return html


def save_reports(data: dict):
    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)
    date = data["date"]
    base_url = "https://neilbritain.github.io/daily-policy-report"

    # JSON
    for path in [report_dir / "latest.json", report_dir / f"report-{date}.json"]:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # 趋势段落
    nums = ["①", "②", "③", "④", "⑤", "⑥"]
    trends_html = "".join(
        f'<p style="font-size:15px;color:#333;line-height:2.0;margin:0 0 16px;">'
        f'<strong style="color:#5b6de4;font-size:16px;">{nums[i]}</strong>&emsp;{t}</p>'
        for i, t in enumerate(data.get("trends", []))
    )

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1.0">
  <title>政策日报 - {date}</title>
</head>
<body style="font-family:'Microsoft YaHei','PingFang SC',Arial,sans-serif;background:#e8e8e8;margin:0;padding:20px;">
<div style="max-width:680px;margin:0 auto;background:#fff;padding:36px 28px;">

  <p style="margin:0 0 24px;font-size:13px;">
    <a href="../index.html" style="color:#5b6de4;text-decoration:none;">← 返回首页</a>
  </p>

  <p style="font-size:26px;font-weight:bold;color:#111;text-align:center;margin:0 0 8px;">{data["title"]}</p>
  <p style="font-size:14px;color:#bbb;text-align:center;margin:0 0 4px;">{date} · 数据 · 算力 · 信息化</p>
  <p style="font-size:12px;color:#ccc;text-align:center;margin:0 0 36px;">
    <a href="{base_url}/reports/report-{date}.html" style="color:#5b6de4;text-decoration:none;">网页版链接</a>
    &nbsp;｜&nbsp;
    <a href="{base_url}/reports/report-{date}.docx" style="color:#5b6de4;text-decoration:none;">下载 Word 版</a>
  </p>

  <p style="background:#5b6de4;color:#fff;font-size:16px;font-weight:bold;padding:11px 18px;margin:0 0 4px;letter-spacing:1px;">一、过去 24 小时关键政策</p>
  {render_policies(data.get("policies_24h", []))}

  <p style="background:#5b6de4;color:#fff;font-size:16px;font-weight:bold;padding:11px 18px;margin:36px 0 4px;letter-spacing:1px;">二、过去一个月主要政策动向</p>
  {render_policies(data.get("policies_1month", []))}

  <p style="background:#5b6de4;color:#fff;font-size:16px;font-weight:bold;padding:11px 18px;margin:36px 0 20px;letter-spacing:1px;">三、未来趋势判断</p>
  {trends_html}

  <p style="border-top:1px solid #eee;margin-top:36px;padding-top:16px;font-size:12px;color:#ccc;text-align:center;line-height:2.0;">
    每天早上 6:00 自动更新 · 由 Claude AI 生成<br>
    <a href="{base_url}" style="color:#5b6de4;text-decoration:none;">{base_url}</a>
  </p>

</div>
</body>
</html>"""

    for path in [report_dir / "latest.html", report_dir / f"report-{date}.html"]:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)

    safe_print(f"[OK] 报告已保存: {date}")


# ──────────────────────────────────────────────
# 4. 入口
# ──────────────────────────────────────────────

def main():
    today = datetime.now(BEIJING_TZ)
    safe_print(f"\n{'='*50}")
    safe_print(f"  政策日报生成  {today.strftime('%Y-%m-%d %H:%M')} CST")
    safe_print(f"{'='*50}")

    safe_print("\n[1/3] 采集数据...")
    raw_data = collect_all_data(today)

    safe_print("\n[2/3] 调用大模型生成报告...")
    data = call_llm_api(raw_data, today)

    safe_print("\n[3/3] 保存文件...")
    save_reports(data)
    safe_print("\n完成！")


if __name__ == "__main__":
    main()
