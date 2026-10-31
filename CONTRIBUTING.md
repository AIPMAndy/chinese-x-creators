# 贡献指南

本项目欢迎研究者、创作者本人和读者提交新线索与纠错。目标是**保留能复核的商业事实**。

1. 提名请使用 [千万级候选 Issue](.github/ISSUE_TEMPLATE/ten-million-lead.md)，尽量链接创作者自己的原话、完整采访或公开账本。
2. 先阅读 [收入证据标准](methodology/evidence-standard.md)；不能通过粉丝数量、产品月流水简单年化推断个人净利润。
3. 如果存在“年营收超千万”和“接近千万”之类差异，保留两条独立主张，不做平均。
4. 具体数据编辑 `data/creators.json` 和 `data/revenue_claims.json`；没有可靠证据必须填“未知”并解释原因。
5. 运行 `python3 scripts/validate_research.py && python3 scripts/build.py && python3 scripts/build_cases.py && python3 -m unittest discover -s tests -v`。
6. 提交 PR 时说明新增/更改了哪条收入主张、来源更新日期、是否影响榜单和原结论。
7. 禁止提交未经授权的收入后台截图、个人联系方式、身份证、银行凭证和受版权保护的整篇文章。
8. 创作者本人可申请更正；项目在可确认来源后及时更新并保留公开修改记录。

## 接受标准

- 同一创作者 X 账号可核验，或明确标记身份未核。
- 每一条收入主张都有原文链接、原文时间、币种、业务主体、口径和反例。
- 千万级必须记录完整自然年或注明为何无法验证，**候选身份绝不等于独立认证**。
- 报告有具体可复制步骤、失败边界与经营风险。
