#!/usr/bin/env python3
"""Build a dependency-free, prerendered GitHub Pages site from source JSON."""
from __future__ import annotations
import html
import json
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs"
CREATORS = json.loads((ROOT / "data/creators.json").read_text(encoding="utf8"))
CFG = json.loads((ROOT / "data/site.json").read_text(encoding="utf8"))


def esc(x):
    return html.escape(str(x), quote=True)


def safe_url(url):
    if not isinstance(url,str) or not url.startswith("https://"):
        raise ValueError(f"Unsafe external URL: {url}")
    return esc(url)


def nav(home=False):
    prefix = "" if home else "../"
    return f'''<a class="skip" href="#main">跳过导航</a><header class="topbar"><div class="wrap nav">
      <a class="brand" href="{prefix}index.html" aria-label="返回首页"><span class="brandmark">X</span><span>中文 X 创作者图鉴</span></a>
      <nav class="navlinks" aria-label="主导航"><a href="{prefix}index.html#cases">案例库</a><a href="{prefix}index.html#method">研究方法</a><a href="{prefix}about.html">关于项目</a><a href="{prefix}evidence.html">收入证据</a><a href="{prefix}compare.html">双人对比</a><a href="{safe_url(CFG['otherOpenSource'])}" target="_blank" rel="noopener noreferrer">保姆级教程</a><a class="navcta" href="{safe_url(CFG['officialWebsite'])}" target="_blank" rel="noopener noreferrer">认识 Andy ↗</a></nav>
    </div></header>'''


def footer(home=False):
    prefix = "" if home else "../"
    return f'''<footer class="footer"><div class="wrap footer-inner"><span>© 2026 AI 酋长 Andy · 基于公开资料整理 · 收入不代表收益承诺</span>
      <div class="footer-links"><a href="{prefix}index.html#method">证据标准</a><a href="{prefix}evidence.html">收入证据</a><a href="{prefix}compare.html">双人对比</a><a href="{prefix}about.html">关于项目</a><a href="{safe_url(CFG['officialWebsite'])}" target="_blank" rel="noopener noreferrer">官方网站</a><a href="{safe_url(CFG['serviceUrl'])}" target="_blank" rel="noopener noreferrer">咨询 / 微信联系</a><a href="https://github.com/{esc(CFG['githubOwner'])}/{esc(CFG['repo'])}" target="_blank" rel="noopener noreferrer">GitHub</a></div>
    </div></footer>'''


def head(title, description, canonical, base=""):
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
      <title>{esc(title)}</title><meta name="description" content="{esc(description)}"><meta name="theme-color" content="#f7f8f4">
      <meta property="og:type" content="website"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}">
      <meta property="og:url" content="{safe_url(canonical)}"><meta property="og:site_name" content="{esc(CFG['projectName'])}"><meta property="og:locale" content="zh_CN">
      <meta property="og:image" content="{safe_url(CFG['siteUrl']+'assets/og-image.png')}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
      <meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(description)}"><meta name="twitter:image" content="{safe_url(CFG['siteUrl']+'assets/og-image.png')}"><meta name="twitter:creator" content="@AIPMAndy"><meta name="author" content="AI 酋长 Andy">
      <link rel="canonical" href="{safe_url(canonical)}"><link rel="icon" type="image/svg+xml" href="{base}assets/logo.svg"><link rel="apple-touch-icon" href="{base}assets/apple-touch-icon.png"><link rel="stylesheet" href="{base}assets/style.css">
      </head><body>'''


def card(c):
    stage = c['stage']; slug = c['id']
    key = ' '.join([c['name'],c.get('handle',''),c['focus'],c['category'],c['headline'],*c['businessModel']])
    badge = "chip" if stage in ('千万级候选','百万级实战','百万以下实战','海外对照') else "chip wait"
    model = ' · '.join(c['businessModel'][:2])
    return f'''<article class="creator-card" data-search="{esc(key)}" data-category="{esc(c['category'])}" data-stage="{esc(stage)}" data-tier="{esc(c.get('tier','observation'))}" data-grade="{esc(c.get('evidenceGrade','D'))}">
      <div class="card-top"><div class="avatar" aria-hidden="true">{esc(c['initials'])}</div><span class="{badge}">{esc(stage)}</span></div>
      <h3 class="card-name">{esc(c['name'])}</h3><p class="card-handle">{('@'+esc(c['handle'])) if c.get('handle') else 'X 账号身份待核对'}</p>
      <p class="card-focus">{esc(model)}</p><p class="card-headline">{esc(c['headline'])}</p>
      <p class="card-summary">{esc(c['summary'])}</p>
      <div class="card-foot"><span>更新于 {esc(c['updatedAt'])}</span><a href="cases/{esc(slug)}.html" aria-label="阅读{esc(c['name'])}案例">阅读案例 ↗</a></div>
    </article>'''


def home():
    complete=len({claim['creator_id'] for claim in json.loads((ROOT/'data/revenue_claims.json').read_text(encoding='utf8'))})
    candidates=len(CREATORS)-complete
    ten=sum(1 for c in CREATORS if c['stage']=='千万级候选')
    cards='\n'.join(card(c) for c in CREATORS)
    site_ld=json.dumps({"@context":"https://schema.org","@type":"WebSite","name":CFG['projectName'],"url":CFG['siteUrl'],"inLanguage":"zh-CN","description":"中文 X 创作者商业化研究库：公开证据、收入归因与商业模式拆解。","author":{"@type":"Person","name":"AI 酋长 Andy","alternateName":"AIPMAndy","url":"https://github.com/AIPMAndy","sameAs":["https://x.com/AIPMAndy","https://metaver.vip/"]},"sameAs":["https://github.com/AIPMAndy/chinese-x-creators"]},ensure_ascii=False).replace('<','\\u003c')
    return head(CFG['projectName']+'：中文 X（推特）创作者收入与商业模式研究 | AI 酋长 Andy',f'中文 X 创作者商业化研究库：用可追溯的公开来源研究 {len(CREATORS)} 位中文 X（推特）创作者的真实收入、流量增长与商业模式，逐项区分个人净收入、公司营收、产品流水和 X 的独立贡献，附收入证据账本与 CSV 下载。',CFG['siteUrl'])+f'<script type="application/ld+json">{site_ld}</script>'+nav(True)+f'''
    <main id="main">
      <div class="wrap"><section class="hero"><span class="eyebrow">OPEN SOURCE / CREATOR ECONOMY</span>
        <h1>找到千万级生意。<br><em>拆开每条收入证据。</em></h1>
        <p>中文 X 商业化研究库。重点追踪年营收千万级创作者，独立设置海外英文圈对照组。个人净收入、公司营收、产品流水、X 的独立贡献，逐项严格区分。</p>
        <div class="hero-actions"><a class="button primary" href="#cases">开始探索案例 <span aria-hidden="true">↗</span></a><a class="button secondary" href="https://github.com/{esc(CFG['githubOwner'])}/{esc(CFG['repo'])}" target="_blank" rel="noopener noreferrer">GitHub 开源仓库 ↗</a></div>
        <span class="hero-note">所有金额均标注来源、期间与归属。自述收入未经独立审计。</span>
        <div class="statbar"><div><strong>{len(CREATORS):02d}</strong><span>研究档案</span></div><div><strong>{ten:02d}</strong><span>千万营收候选 / 非审计认证</span></div><div><strong>{complete:02d}</strong><span>有收入主张的研究对象</span></div></div>
      </section></div>
      <section class="section" id="cases"><div class="wrap"><div class="section-header"><div><span class="eyebrow">CASE LIBRARY</span><h2 class="section-title">公开证据比头衔更重要。</h2><p class="section-subtitle">“年入千万”先过三道关：①收入是个人还是公司 ②实际年度还是年化估算 ③X贡献有无明确证据。当前没有独立审计支持的个人年净收千万案例。</p></div><span class="counter">显示 <span id="visible-count">{len(CREATORS)}</span> / {len(CREATORS)}</span></div>
      <div class="toolbar"><label class="searchbox"><svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m16 16 5 5"/></svg><input id="search" type="search" placeholder="搜索人名、账号、变现模式…" aria-label="搜索创作者"></label>
        <select class="select" id="category" aria-label="选择领域"><option value="">全部领域</option>{''.join(f'<option value="{esc(k)}">{esc(k)}</option>' for k in sorted(set(c['category'] for c in CREATORS)))}</select><select class="select" id="stage" aria-label="选择案例状态"><option value="">全部状态</option>{''.join(f'<option value="{esc(k)}">{esc(k)}</option>' for k in ['千万级候选','百万级实战','百万以下实战','海外对照','研究观察','身份待核'] if any(c['stage']==k for c in CREATORS))}</select><select class="select" id="grade" aria-label="证据等级"><option value="">全部证据等级</option><option value="B">B · 本人公开自述</option><option value="C">C · 第三方转述</option><option value="D">D · 暂无收入数据</option></select></div>
      <div class="cards" id="creator-grid">{cards}</div><div class="empty" id="empty" role="status">没有匹配的案例，试试其他关键词。</div>
      <p class="legend">收入证据等级：A 可独立核验 / B 本人自述 / C 第三方转述 / D 未披露。中文区的两个“千万级候选”都尚未通过个人年净收入核验；海外对照样本不计入中文区主榜。<a href="data/claims.csv" download>下载创作者研究 CSV ↗</a></p></div></section>
      <section class="section" id="method"><div class="wrap"><span class="eyebrow">OUR METHOD</span><h2 class="section-title">严格验证。公开纠错。每周更新。</h2><p class="section-subtitle">把公开事实与商业推断分开。我们关注可执行的方法，也认真记录失败与成本。</p>
      <div class="feature-grid" style="margin-top:26px"><div class="feature"><span class="feature-index">01 / EVIDENCE</span><h3>逐项核实收入</h3><p>每个数字都记录金额、币种、期间、收入口径与来源。产品营收、个人收入和利润绝不混用。</p></div><div class="feature"><span class="feature-index">02 / ATTRIBUTION</span><h3>区分 X 与其他渠道</h3><p>经营者通常有网站、私域和搜索流量。没有渠道证据，就诚实标注“X 贡献未知”。</p></div><div class="feature"><span class="feature-index">03 / REPLICATION</span><h3>提炼可以实践的步骤</h3><p>拆解内容定位、价值交付、获取第一位客户及后续复购，避免空泛地劝你“坚持输出”。</p></div><div class="feature"><span class="feature-index">04 / CORRECTION</span><h3>开源、持续纠错</h3><p>任何人都可以提交原始证据、反例和更新。争议数字优先标记不确定性，不制造神话。</p></div></div>
      <div class="quote-banner"><h2>看完案例，下一步就是自己做一次。</h2><p>这里有从选题、内容到获客与成交的实操思路。想结合你的行业经验做个人 AI + IP，也可以通过 Andy 的网站联系。</p><a class="button" href="{safe_url(CFG['serviceUrl'])}" target="_blank" rel="noopener noreferrer">了解 Andy 的服务 / 微信联系 ↗</a></div>
      </div></section>
    </main>'''+footer(True)+'''<script defer src="assets/app.js"></script></body></html>'''


def li(items):
    return '<ul>' + ''.join('<li>'+esc(x)+'</li>' for x in items)+'</ul>'


def detail(c):
    slug=c['id']
    info=c['revenue']
    vals=[('已公开收入',info['label']),('数据区间',info['period']),('统计口径',info['scope']),('X 贡献',info['attribution'])]
    vals.append(('证据等级', c.get('evidenceGrade','D')+' · '+c['stage']))
    facts=''.join(f'<div class="fact"><small>{esc(k)}</small><strong>{esc(v)}</strong></div>' for k,v in vals)
    sources=''.join(f'<li><a href="{safe_url(s["url"])}" target="_blank" rel="noopener noreferrer">{esc(s["title"])}</a><br><small>{esc(s["type"])} · 核验 {esc(s["checked"])}</small></li>' for s in c['sources'])
    desc=c['summary']
    structured={"@context":"https://schema.org","@type":"Article","inLanguage":"zh-CN","headline":f"{c['name']}：中文 X 创作者商业化案例","description":desc,"author":{"@type":"Person","name":"AI 酋长 Andy"},"dateModified":c['updatedAt'],"mainEntityOfPage":CFG['siteUrl']+f'cases/{slug}.html'}
    jsonld=json.dumps(structured,ensure_ascii=False).replace('<','\\u003c')
    return head(f"{c['name']}｜中文 X 商业化案例 - AI 酋长 Andy",desc,CFG['siteUrl']+f'cases/{slug}.html',"../")+f'<script type="application/ld+json">{jsonld}</script>'+nav()+f'''
    <main id="main"><div class="wrap"><section class="detail-hero"><div class="breadcrumb"><a href="../index.html">全部案例</a> / {esc(c['name'])}</div><span class="eyebrow">CREATOR FIELD NOTES / {esc(c['category'])}</span>
    <h1>{esc(c['name'])}：<br>{esc(c['focus'])}</h1><p class="detail-lead">{esc(c['headline'])}</p><div class="meta"><span>{esc(c['stage'])}</span><span>{('@'+esc(c['handle'])) if c.get('handle') else 'X 账号身份待核'}</span><span>{esc(c['readMinutes'])} 分钟阅读</span><span>核验 {esc(c['updatedAt'])}</span></div>
    </section><div class="detail-layout"><article class="article"><h2>01 / 先把数字说清楚</h2><div class="fact-grid">{facts}</div>
    <p class="callout">证据说明：{esc('本人公开自述，未经独立审计' if info['kind']=='self_report' else ('公开商业规模表述存在限制或不同报道口径，未核验个人年度净收入' if info['kind']=='business_claim' else '目前未找到可靠的公开年度收入数据'))}。本站不保证任何人能达到类似结果。</p>
    <h2>02 / 这个人做什么</h2><p>{esc(desc)}</p>
    <h2>03 / 商业链路</h2><p>{esc(c['mechanism'])}</p>
    <h2>04 / 最值得研究的 3 件事</h2>{li(c['insights'])}
    <h2>05 / 普通人怎么开始</h2>{li(c['actions'])}
    <h2>06 / 哪些结论不能直接照抄</h2>{li(c['limitations'])}
    <h2>07 / 公开来源</h2><ol class="sources">{sources}</ol>
    <p class="callout">纠错与补充：若发现金额、统计口径或来源有误，请在 GitHub 提交 Issue，并附公开原始链接。我们优先修正错误，不将未经证实的主张包装成成功案例。</p>
    </article><aside class="aside"><h3>读完了，开始实践。</h3><p>建议先完成一项可验证的产出，再研究营销。工具、咨询、课程各有不同成本，先算清楚。</p><a class="button primary" href="{safe_url(CFG['otherOpenSource'])}" target="_blank" rel="noopener noreferrer">X 保姆级赚钱指南 ↗</a><a class="button secondary" href="{safe_url(CFG['serviceUrl'])}" target="_blank" rel="noopener noreferrer">Andy 咨询 / 微信联系 ↗</a><div class="mini-note">由 AI 酋长 Andy 基于公开资料独立整理，未经案例当事人背书。网站与全部代码开源。</div></aside>
    </div></div></main>'''+footer()+'''</body></html>'''


def main():
    if len(set(c['id'] for c in CREATORS))!=len(CREATORS):
        raise ValueError('Duplicated creator id')
    for c in CREATORS:
        if not re.fullmatch(r'[a-z0-9-]+', c['id']):raise ValueError('Invalid slug')
        if not c['sources']:raise ValueError('Missing sources')
        if c.get('evidenceGrade') not in ('A','B','C','D'):raise ValueError('Invalid grade')
        if c['stage']=='千万级候选' and c['revenue']['value'] is not None:raise ValueError('Candidate cannot be machine-ranked')
        for s in c['sources']:safe_url(s['url'])
        if c['revenue']['value'] is not None and not c['revenue']['period']:
            raise ValueError('Revenue period must be known')
    import csv
    (OUT/'data').mkdir(parents=True,exist_ok=True)
    with (OUT/'data'/'claims.csv').open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.writer(f,lineterminator='\n')
        writer.writerow(['id','name','handle','stage','evidence_grade','claim','period','scope','x_attribution','value_CNY_if_observed','first_source','last_checked'])
        for c in CREATORS:
            r=c['revenue'];writer.writerow([c['id'],c['name'],c.get('handle',''),c['stage'],c.get('evidenceGrade','D'),r['label'],r['period'],r['scope'],r['attribution'],r['value'] if r['currency']=='CNY' and r['value'] is not None else '',c['sources'][0]['url'],c['updatedAt']])
    claims=json.loads((ROOT/'data/revenue_claims.json').read_text(encoding='utf8'))
    with (OUT/'data'/'revenue_claims.csv').open('w',encoding='utf-8-sig',newline='') as f:
        fieldnames=['id','creator_id','claim','amount','currency','comparator','period','metric_type','reporting_entity','evidence_grade','source_url','source_date','verified_at','x_attribution','caveat']
        writer=csv.DictWriter(f,fieldnames=fieldnames,extrasaction='ignore',lineterminator='\n')
        writer.writeheader()
        for claim in claims:writer.writerow(claim)
    for name in ('creators.json','revenue_claims.json'):
        (OUT/'data'/name).write_bytes((ROOT/'data'/name).read_bytes())
    (OUT/'index.html').write_text(home(),encoding='utf8')
    for extra in ('about.html','404.html','evidence.html','compare.html'):
        (OUT/extra).write_text((ROOT/'templates'/('site-'+extra)).read_text(encoding='utf8'),encoding='utf8')
    for c in CREATORS:
        (OUT/'cases'/f'{c["id"]}.html').write_text(detail(c),encoding='utf8')
    targets=[CFG['siteUrl'],CFG['siteUrl']+'about.html',CFG['siteUrl']+'evidence.html',CFG['siteUrl']+'compare.html',CFG['siteUrl']+'investigations.html']+[CFG['siteUrl']+f'cases/{c["id"]}.html' for c in CREATORS]
    xml='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{esc(u)}</loc><lastmod>2026-10-31</lastmod></url>\n' for u in targets)+'</urlset>\n'
    (OUT/'sitemap.xml').write_text(xml,encoding='utf8')
    (OUT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+CFG['siteUrl']+'sitemap.xml\n',encoding='utf8')
    print(f"Generated {len(CREATORS)} case pages, homepage, sitemap and robots.txt")

if __name__=='__main__':main()
