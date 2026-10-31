#!/usr/bin/env python3
"""Conservative evidence validation: never infer annual profits from topline claims."""
import json
from pathlib import Path
r=Path(__file__).resolve().parents[1]
creators=json.loads((r/'data/creators.json').read_text(encoding='utf8'))
claims=json.loads((r/'data/revenue_claims.json').read_text(encoding='utf8'))
ids={c['id'] for c in creators}
assert len(ids)==len(creators)
assert len({x['id'] for x in claims})==len(claims)
for c in creators:
    assert c['evidenceGrade'] in ('A','B','C','D'),c['id']
    if c['stage']=='千万级候选':
        assert c['evidenceGrade']!='A' and c['revenue']['value'] is None,c['id']
    assert c['sources'] and all(x['url'].startswith('https://') for x in c['sources']),c['id']
for x in claims:
    assert x['creator_id'] in ids,x['id']
    assert x['source_url'].startswith('https://'),x['id']
    assert x['evidence_grade'] in ('A','B','C','D'),x['id']
    assert x['metric_type'] and x['period'] and x['reporting_entity'] and x['caveat'],x['id']
    assert x['x_attribution'] in ('unknown','not_established','related_unquantified','creator_claimed','verified'),x['id']
    if x['comparator'] in ('>','~<') and x['amount']>=10000000:
        assert x['metric_type']!='personal_net_income' and x['x_attribution']!='verified', x['id']
print(f'Validated {len(creators)} creators and {len(claims)} claim records; no certified personal 10m net income asserted.')
