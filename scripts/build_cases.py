#!/usr/bin/env python3
"""Generate transparent, source-linked markdown profiles from structured research."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
items=json.loads((R/'data/creators.json').read_text(encoding='utf8'))


def bullets(items):
    return '\n'.join('- '+x for x in items)

for c in items:
    r=c['revenue']
    level=c.get('evidenceGrade','D')+'｜'+('本人公开自述（未经审计）' if c.get('evidenceGrade')=='B' else ('第三方转述或身份待核' if c.get('evidenceGrade')=='C' else '收入未披露 / 待补证'))
    src='\n'.join(f'{idx}. [{s["title"]}]({s["url"]}) — {s["type"]}，上次正文检查 {s["checked"]}。{s.get("review_note", "")}' for idx,s in enumerate(c['sources'],1))
    content=f'''# {c['name']}：{c['focus']}

> **证据等级：{level}** · 最后核查：{c['updatedAt']} · {('[X 主页](https://x.com/'+c['handle']+')') if c.get('handle') else 'X 账号身份待核实'}

## 一句话看懂

{c['headline']}。

{c['summary']}

## 收入与证据

| 指标 | 公开信息 |
| --- | --- |
| 金额 / 规模 | {r['label']} |
| 数据期间 | {r['period']} |
| 口径 | {r['scope']} |
| X 归因 | {r['attribution']} |
| 证据等级 | {level} |

以上为公开主张或研究记录，**没有独立财务审计支持**。无法从营业收入推断个人利润，也无法将粉丝数量换算成收入。

## 商业化路径

{c['mechanism']}

### 需要记住的事实

{bullets(c['insights'])}

## 普通人可以实践的动作

{bullets(c['actions'])}

## 风险、失败与边界

{bullets(c['limitations'])}

## 原始来源

{src}

---

独立研究资料，未经创作者本人赞助或认可。发现错误欢迎 [提交更正](https://github.com/AIPMAndy/chinese-x-creators/issues/new/choose)。完整方法见 [收入证据与归因规则](../methodology/evidence-standard.md)。
'''
    (R/'cases'/f"{c['id']}.md").write_text(content,encoding='utf8')
print(f'Generated {len(items)} markdown dossiers')
