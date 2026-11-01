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

# V4 secondary lead queue: deliberately excluded from the X creator ranking.
leads=json.loads((r/'data/investigation_leads.json').read_text(encoding='utf8'))
assert len({item['id'] for item in leads})==len(leads)
assert not ({item['id'] for item in leads} & ids)
for item in leads:
    assert item['admission'] in ('overseas_comparison_pending','company_research_only','existing_overseas_comparison'),item['id']
    assert item['evidence_grade'] in ('A','B','C','D'),item['id']
    assert item['amount']>0 and item['currency'] in ('CNY','USD'),item['id']
    assert item['metric_type'] in ('arr_run_rate','company_revenue','business_revenue'),item['id']
    assert item['period'] and item['reporting_entity'] and item['caveat'] and item['next_check'],item['id']
    assert item['source_urls'] and all(x['url'].startswith('https://') for x in item['source_urls']),item['id']
    assert item['x_attribution']!='verified',item['id']
    if item['x_identity']=='unverified':
        assert not item['x_handle'] and item['admission']=='company_research_only',item['id']
    if item['x_handle']:
        assert item['x_identity']=='matched' and item['x_handle'].replace('_','').isalnum(),item['id']
    if item['metric_type']=='arr_run_rate':
        assert 'ARR' in item['claim'] and '年化' in item['caveat'],item['id']
print(f'Validated {len(leads)} supplementary research leads, excluded from the formal X roster.')
