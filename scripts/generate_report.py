#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日政策报告生成脚本 v3.8
DuckDuckGo + Bing + 12个官网抓取 + DeepSeek API
覆盖：算力/AI/数据/算法/网络/信息化/数字化，允许知识库补充兜底
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


import urllib.parse


def _html_get(url: str, timeout: int = 20, encoding: str = None) -> "BeautifulSoup | None":
    """通用 HTTP GET，返回 BeautifulSoup 对象，失败返回 None"""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,*/*;q=0.9",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }
    try:
        r = requests.get(url, headers=headers, timeout=timeout)
        r.encoding = encoding or r.apparent_encoding or "utf-8"
        return BeautifulSoup(r.text, "html.parser")
    except Exception as e:
        safe_print(f"    [warn] GET 失败 {url[:60]}: {e}")
        return None


def search_duckduckgo(query: str, max_results: int = 8) -> str:
    """DuckDuckGo HTML 搜索"""
    if not HAS_BS4:
        return f"[bs4 未安装: {query}]"
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}&kl=cn-zh"
    soup = _html_get(url)
    if not soup:
        return "(搜索失败)"
    items = []
    for div in soup.select(".result")[:max_results]:
        t = div.select_one(".result__a")
        s = div.select_one(".result__snippet")
        u = div.select_one(".result__url")
        if t:
            items.append(
                f"· {t.get_text(strip=True)}\n"
                f"  {u.get_text(strip=True) if u else ''}\n"
                f"  {s.get_text(strip=True) if s else ''}"
            )
    return "\n\n".join(items) if items else "(未找到结果)"


def search_bing(query: str, max_results: int = 8) -> str:
    """Bing 搜索（中文，补充 DuckDuckGo 盲区）"""
    if not HAS_BS4:
        return ""
    url = f"https://www.bing.com/search?q={urllib.parse.quote(query)}&setlang=zh-CN&cc=CN"
    soup = _html_get(url)
    if not soup:
        return "(Bing 搜索失败)"
    items = []
    for li in soup.select("li.b_algo")[:max_results]:
        h2 = li.select_one("h2 a")
        cap = li.select_one(".b_caption p")
        if h2:
            items.append(
                f"· {h2.get_text(strip=True)}\n"
                f"  {h2.get('href','')}\n"
                f"  {cap.get_text(strip=True) if cap else ''}"
            )
    return "\n\n".join(items) if items else "(Bing 未找到结果)"


def _resolve_url(redirect_url: str, timeout: int = 10) -> str:
    """跟随跳转链接，返回真实目标 URL"""
    try:
        r = requests.head(redirect_url, allow_redirects=True, timeout=timeout,
                          headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        return r.url
    except Exception:
        return redirect_url


def _scrape_page_excerpt(url: str, max_chars: int = 500) -> str:
    """抓取目标页面正文前 max_chars 字（提取日期和摘要用）"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept-Language": "zh-CN,zh;q=0.9",
        }
        r = requests.get(url, headers=headers, timeout=15)
        r.encoding = r.apparent_encoding or "utf-8"
        soup = BeautifulSoup(r.text, "html.parser")
        # 移除脚本/样式
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        text = soup.get_text(separator=" ", strip=True)
        # 取前 max_chars 字
        return text[:max_chars].replace("\n", " ")
    except Exception:
        return ""


def search_baidu(query: str, max_results: int = 8, resolve_links: int = 5) -> str:
    """百度搜索 + 自动解析跳转链接获取真实URL和摘要"""
    if not HAS_BS4:
        return ""
    url = f"https://www.baidu.com/s?wd={urllib.parse.quote(query)}&rn={max_results}"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Accept": "text/html,application/xhtml+xml,*/*;q=0.9",
        "Referer": "https://www.baidu.com/",
    }
    try:
        r = requests.get(url, headers=headers, timeout=20)
        r.encoding = "utf-8"
        soup = BeautifulSoup(r.text, "html.parser")
        raw_items = []
        for div in soup.select("div.result,div[class*='result-op']")[:max_results]:
            title_a = div.select_one("h3 a") or div.select_one("a[data-click]")
            # 尝试多个 snippet 选择器
            snippet_el = (div.select_one("div.c-abstract")
                          or div.select_one("[class*='abstract']")
                          or div.select_one("[class*='content']"))
            if title_a:
                raw_items.append({
                    "title": title_a.get_text(strip=True),
                    "href":  title_a.get("href", ""),
                    "snippet": snippet_el.get_text(strip=True) if snippet_el else "",
                })

        items = []
        for idx, item in enumerate(raw_items):
            title   = item["title"]
            href    = item["href"]
            snippet = item["snippet"]

            # 对前 resolve_links 条跟随跳转，获取真实URL + 页面摘要
            if idx < resolve_links and href.startswith("http://www.baidu.com/link"):
                real_url = _resolve_url(href)
                if not snippet:
                    snippet = _scrape_page_excerpt(real_url, 400)
                href = real_url
                time.sleep(0.5)

            items.append(
                f"· {title}\n"
                f"  {href}\n"
                f"  {snippet[:300] if snippet else '（无摘要）'}"
            )
        return "\n\n".join(items) if items else "(百度未找到结果)"
    except Exception as e:
        return f"(百度搜索异常: {e})"


def scrape_gov_sites() -> str:
    """直接抓取 12 个核心政府 / 官方媒体网站的最新政策列表"""
    if not HAS_BS4:
        return ""

    POL_KW = ("通知", "规定", "办法", "方案", "意见", "规划", "条例", "政策",
              "标准", "指南", "指导", "部署", "行动", "要求", "管理")

    sources = [
        # 国家级部委——政策文件专区
        {"name": "国家数据局-政策法规",   "url": "https://www.nda.gov.cn/sjj/zcfg/",                       "base": "https://www.nda.gov.cn"},
        {"name": "工信部-文件发布",        "url": "https://www.miit.gov.cn/zwgk/zcwj/wjfb/",               "base": "https://www.miit.gov.cn"},
        {"name": "网信办-政策法规",        "url": "https://www.cac.gov.cn/hjlyj/",                          "base": "https://www.cac.gov.cn"},
        {"name": "工信部-信息化司",        "url": "https://www.miit.gov.cn/jgsj/xxjss/gzdt/",              "base": "https://www.miit.gov.cn"},
        {"name": "工信部-大数据司",        "url": "https://www.miit.gov.cn/jgsj/dsjs/gzdt/",               "base": "https://www.miit.gov.cn"},
        {"name": "发改委-高技术",          "url": "https://www.ndrc.gov.cn/fggz/gjscy/",                   "base": "https://www.ndrc.gov.cn"},
        {"name": "国务院-数字政府",        "url": "https://www.gov.cn/zhengce/shuzizf/",                   "base": "https://www.gov.cn"},
        {"name": "科技部-政策",            "url": "https://www.most.gov.cn/xxgk/xinxifenlei/fdzdgknr/fgzc/zcfg/", "base": "https://www.most.gov.cn"},
        # 专项数字经济/数据政策渠道
        {"name": "新华网-科技",            "url": "https://www.xinhuanet.com/tech/",                       "base": "https://www.xinhuanet.com"},
        {"name": "人民网-IT",              "url": "http://it.people.com.cn/",                              "base": "http://it.people.com.cn"},
        {"name": "中国信通院动态",         "url": "http://www.caict.ac.cn/xwdt/gndt/",                     "base": "http://www.caict.ac.cn"},
        {"name": "工业互联网产业联盟",     "url": "https://www.aii-alliance.org/index/c188/",              "base": "https://www.aii-alliance.org"},
    ]

    results = []
    for src in sources:
        soup = _html_get(src["url"], timeout=15)
        if not soup:
            continue
        items = []
        for a in soup.find_all("a", href=True):
            text = a.get_text(strip=True)
            href = a["href"]
            if len(text) > 8 and any(kw in text for kw in POL_KW):
                if href.startswith("/"):
                    href = src["base"] + href
                elif not href.startswith("http"):
                    continue
                items.append(f"  - {text} | {href}")
        if items:
            results.append(f"【{src['name']}】\n" + "\n".join(items[:10]))

    return "\n\n".join(results)


def collect_all_data(today: datetime) -> str:
    """汇总所有搜索和抓取结果（扩展版：DuckDuckGo + Bing + 12 个官网）"""
    ym  = today.strftime("%Y年%m月")
    ymd = today.strftime("%Y年%m月%d日")

    # ── 搜索查询 ──
    ddg_queries = [
        "国务院 国家数据局 工信部 网信办 最新政策通知",
        "算力 算力网络 东数西算 算力枢纽 政策",
        "人工智能 大模型 生成式AI 监管 最新",
        "数据要素 数据安全 数据治理 数据资产 新规",
        "网络安全 等级保护 关键信息基础设施 最新规定",
        "数字政府 数字中国 信息化 政策",
        "数字化转型 工业互联网 数字经济 政策",
    ]
    bing_queries = [
        f"数据要素 算力 人工智能 政策 {ym} site:gov.cn",
        f"网络安全 信息化 数字化 规定 通知 {ym}",
        f"工业互联网 数字经济 算法 政策 {ym}",
    ]
    baidu_queries = [
        f"国家数据局 工信部 网信办 最新政策 {ym}",
        f"算力 人工智能 数据安全 政策文件 {ym} site:gov.cn",
        f"数字化转型 工业互联网 信息化 最新规定 {ym}",
        f"网络安全 数据要素 算法治理 通知 {ym}",
    ]

    parts = [f"今天是 {ymd}。以下为多渠道采集的原始政策信息：\n"]

    safe_print("  >[1] DuckDuckGo 搜索...")
    for i, q in enumerate(ddg_queries, 1):
        safe_print(f"    [{i}/{len(ddg_queries)}] {q[:50]}")
        parts.append(f"── DDG「{q[:45]}」──\n{search_duckduckgo(q)}")
        time.sleep(1.5)

    safe_print("  >[2] Bing 搜索...")
    for i, q in enumerate(bing_queries, 1):
        safe_print(f"    [{i}/{len(bing_queries)}] {q[:50]}")
        parts.append(f"── Bing「{q[:45]}」──\n{search_bing(q)}")
        time.sleep(1.5)

    safe_print("  >[3] 百度搜索...")
    for i, q in enumerate(baidu_queries, 1):
        safe_print(f"    [{i}/{len(baidu_queries)}] {q[:50]}")
        parts.append(f"── 百度「{q[:45]}」──\n{search_baidu(q)}")
        time.sleep(2)

    safe_print("  >[4] 抓取政府官网 / 官媒...")
    gov_text = scrape_gov_sites()
    if gov_text:
        parts.append(f"── 官网直接抓取 ──\n{gov_text}")
    else:
        parts.append("── 官网直接抓取 ── (均无响应或无匹配条目)")

    # 保存原始数据供调试
    raw = "\n\n".join(parts)
    try:
        debug_path = Path("reports") / f"raw_data_{today.strftime('%Y-%m-%d')}.txt"
        debug_path.write_text(raw, encoding="utf-8")
        safe_print(f"  [debug] 原始数据已保存: {debug_path}")
    except Exception:
        pass

    return raw


# ──────────────────────────────────────────────
# 2. Claude API 生成报告
# ──────────────────────────────────────────────

REPORT_PROMPT = """你是一名专注于中国政府政策的分析助手，今天是 {date_str}。

以下是从 DuckDuckGo、Bing 及多个政府官网采集的原始数据：

{raw_data}

━━━ 收录范围（必须与以下主题之一相关，否则排除）━━━
算力 · 智能计算 · 东数西算 · 算力枢纽 · 人工智能 · 大模型 · 生成式AI · 机器学习 · 数据要素 · 数据安全 · 数据治理 · 数据资产 · 数据跨境 · 算法治理 · 网络安全 · 等级保护 · 关键信息基础设施 · 信息化 · 数字政府 · 数字中国 · 数字经济 · 数字化转型 · 工业互联网 · 5G · 绿色算力 · 区块链 · 物联网 · 平台经济 · 隐私计算 · 云计算 · 大数据

不属于上述主题的政策（如民政、教育、农业、医疗、社保、劳动等）一律不收录。

━━━ 内容来源优先级 ━━━

【第一优先】搜索结果和官网抓取中明确出现的政策（标题、字号、日期均来自原始数据）
【第二优先】你已知的、在 {date_str} 前已公开发布的真实政策文件（知识库补充，date 填实际发布日期；doc_number 如不确定则填"暂无"）
【禁止】编造不存在的政策标题、虚构文件字号、捏造发布日期

━━━ 准确性要求 ━━━
- 文件字号（如"国办发〔2026〕15号"）：来源原文有则填写，不确定则填"暂无"
- 发布日期：来源有明确日期则用，否则根据你对该政策的了解填写，实在不确定填 {date_str}
- URL：有真实链接则填，没有一律填空字符串 ""，禁止填推测性链接
- summary：客观概括核心内容，50 字以内，不得添加无根据的推断

━━━ 时效性要求 ━━━
- policies_24h：优先收录 {date_3d_ago} 之后发布的政策（近 3 天）；搜索无近期结果时，可放宽至近 30 天内最重要的政策
- policies_1month：收录 {date_30d_ago} 之后发布的政策（近 30 天）；超过 60 天的条目一律不收录
- 两个分区均要求 4~6 条；如确实找不到足够的本领域政策，宁可少于 4 条，也不得用无关领域或过期内容凑数

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

仅返回以下格式的 JSON，不加任何 markdown 代码块：
{{
  "policies_24h": [
    {{
      "title": "政策标题（不含书名号）",
      "doc_number": "发文字号（不确定填暂无）",
      "institution": "发布机构全称",
      "date": "YYYY-MM-DD",
      "url": "官方来源链接（无则填空字符串）",
      "summary": "核心内容摘要，50 字以内"
    }}
  ],
  "policies_1month": [
    {{ 同上格式 }}
  ],
  "trends": [
    "趋势 1：基于已收录政策的客观判断（80字以内）",
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

    # ── 后处理 ──
    data = _validate_dates(data, today)   # 1. 日期校验 + 自动归类
    data = _filter_by_topic(data)         # 2. 主题硬过滤
    data = _resolve_baidu_urls(data)      # 3. 解析 Baidu 跳转链接
    return data


def _validate_dates(data: dict, today: datetime) -> dict:
    """
    日期校验 + 自动归类：
    - 未来日期 → 移除
    - policies_24h 中超过 5 天的条目 → 自动移入 policies_1month
    - policies_1month 中超过 60 天的条目 → 移除
    """
    today_date = today.date()
    overflow_to_1month = []   # 从 policies_24h 溢出的条目

    for key in ("policies_24h", "policies_1month"):
        original = data.get(key, [])
        cleaned = []
        for p in original:
            raw_date = p.get("date", "")
            try:
                pub = datetime.strptime(raw_date, "%Y-%m-%d").date()
            except ValueError:
                safe_print(f"  [warn] 日期格式异常，修正为今天: {p.get('title','?')[:35]}")
                p["date"] = today.strftime("%Y-%m-%d")
                cleaned.append(p)
                continue

            if pub > today_date:
                safe_print(f"  [!] 日期超前，移除: {p.get('title','?')[:35]} | {raw_date}")
                continue

            days_ago = (today_date - pub).days

            if key == "policies_24h" and days_ago > 5:
                # 超过5天 → 移入 policies_1month（不删）
                safe_print(f"  [move] 24h→1month ({days_ago}天): {p.get('title','?')[:35]}")
                overflow_to_1month.append(p)
                continue

            if key == "policies_1month" and days_ago > 60:
                safe_print(f"  [!] 超期移除 ({days_ago}天): {p.get('title','?')[:35]}")
                continue

            cleaned.append(p)

        data[key] = cleaned

    # 合并溢出条目到 policies_1month（去重）
    existing_titles = {p["title"] for p in data.get("policies_1month", [])}
    for p in overflow_to_1month:
        if p["title"] not in existing_titles:
            data["policies_1month"].append(p)
            existing_titles.add(p["title"])

    return data


# 主题关键词白名单（标题或摘要含其中之一才保留）
TOPIC_KEYWORDS = (
    "算力", "智能计算", "东数西算", "数据中心",
    "人工智能", "大模型", "生成式", "机器学习", "深度学习", "AI",
    "数据要素", "数据安全", "数据治理", "数据资产", "数据跨境", "数据共享",
    "数字经济", "数字化", "数字政府", "数字中国",
    "信息化", "信息安全", "信息技术",
    "网络安全", "等级保护", "关键信息基础设施",
    "工业互联网", "互联网平台", "5G", "物联网", "云计算",
    "算法", "区块链", "隐私计算",
)


def _filter_by_topic(data: dict) -> dict:
    """Python 层硬过滤：标题和摘要均不含主题关键词的条目直接移除"""
    for key in ("policies_24h", "policies_1month"):
        original = data.get(key, [])
        filtered = []
        for p in original:
            text = p.get("title", "") + p.get("summary", "")
            if any(kw in text for kw in TOPIC_KEYWORDS):
                filtered.append(p)
            else:
                safe_print(f"  [skip] 主题不符，已过滤: {p.get('title','?')[:40]}")
        data[key] = filtered
    return data


def _resolve_baidu_urls(data: dict) -> dict:
    """把 JSON 中残留的 baidu.com/link 跳转链接解析为真实目标 URL"""
    for key in ("policies_24h", "policies_1month"):
        for p in data.get(key, []):
            url = p.get("url", "")
            if url and "baidu.com/link" in url:
                real = _resolve_url(url)
                if real != url and "baidu.com" not in real:
                    p["url"] = real
                    safe_print(f"  [url] 已解析: {real[:70]}")
                else:
                    # 无法解析 → 清空（不留无效链接）
                    p["url"] = ""
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
