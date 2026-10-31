import json
import unittest
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'data/creators.json').read_text(encoding='utf8'))
DOCS=ROOT/'docs'

class HrefParser(HTMLParser):
    def __init__(self): super().__init__();self.refs=[]
    def handle_starttag(self,tag,attrs):
        if tag=='a':self.refs.extend(v for k,v in attrs if k=='href')

class TestProject(unittest.TestCase):
    def test_minimum_twenty_profiles_and_unique_ids(self):
        self.assertGreaterEqual(len(DATA),20)
        self.assertEqual(len(DATA),len(set(x['id'] for x in DATA)))
    def test_evidence_categories_and_strict_million_rules(self):
        for c in DATA:
            self.assertIn(c['evidenceGrade'],('A','B','C','D'))
            self.assertIn('tier',c)
            if c['stage']=='千万级候选':
                self.assertIsNone(c['revenue']['value'])
                self.assertNotEqual(c['evidenceGrade'],'A')

    def test_claim_ledger_has_differences(self):
        claims=json.loads((ROOT/'data/revenue_claims.json').read_text(encoding='utf8'))
        self.assertGreaterEqual(len(claims),10)
        self.assertTrue({'liu-video','liu-infoq'} <= set(x['id'] for x in claims))
        self.assertTrue(all(x['source_url'].startswith('https://') for x in claims))

    def test_export_claims_csv(self):
        import csv
        f=DOCS/'data'/'claims.csv'
        with f.open(encoding='utf-8-sig',newline='') as h:
            rows=list(csv.DictReader(h))
        self.assertEqual(len(rows),len(DATA))
        self.assertTrue(all(r['first_source'].startswith('https://') for r in rows))

    def test_claim_level_csv_export_and_metric_integrity(self):
        import csv
        claims=json.loads((ROOT/'data/revenue_claims.json').read_text(encoding='utf8'))
        with (DOCS/'data'/'revenue_claims.csv').open(encoding='utf-8-sig',newline='') as h:
            rows=list(csv.DictReader(h))
        self.assertEqual(len(rows),len(claims))
        self.assertTrue(any(r['metric_type']=='arr_run_rate' for r in rows))
        self.assertTrue(any(r['creator_id']=='indexsy' and r['period'].startswith('2025') for r in rows))
        self.assertTrue(all(r['caveat'] and r['reporting_entity'] for r in rows))

    def test_weekly_review_workflow_present(self):
        workflow=(ROOT/'.github/workflows/weekly-research.yml').read_text(encoding='utf8')
        self.assertIn('schedule:',workflow)
        self.assertIn('issues: write',workflow)

    def test_revenue_provenance(self):
        for c in DATA:
            self.assertTrue(c['sources'],c['id'])
            r=c['revenue']
            for key in ('label','period','scope','attribution','kind'):
                self.assertTrue(r.get(key),f'{c["id"]}: {key}')
            if r['value'] is not None:
                self.assertGreater(r['value'],0)
                self.assertEqual(r['currency'],'CNY')
                self.assertNotEqual(r['period'],'未披露')
            for s in c['sources']:
                self.assertEqual(urlparse(s['url']).scheme,'https')
                self.assertTrue(s['title'])
                self.assertRegex(s['checked'],r'^2026-\d\d-\d\d$')
    def test_generated_dossiers_exist(self):
        for c in DATA:
            self.assertTrue((ROOT/'cases'/f"{c['id']}.md").exists())

    def test_generated_pages_exist(self):
        self.assertTrue((DOCS/'index.html').exists())
        for c in DATA:
            self.assertTrue((DOCS/'cases'/f"{c['id']}.html").exists())
    def test_local_links_resolve(self):
        for path in [DOCS/'index.html',*(DOCS/'cases').glob('*.html')]:
            parser=HrefParser();parser.feed(path.read_text(encoding='utf8'))
            for href in parser.refs:
                if href.startswith(('https://','http://','#','mailto:')):continue
                self.assertTrue((path.parent/href.split('#')[0]).exists(),f'{path}: {href}')
    def test_index_mentions_provenance(self):
        page=(DOCS/'index.html').read_text(encoding='utf8')
        self.assertIn('自述收入未经独立审计',page)
        self.assertIn('id="search"',page)

if __name__=='__main__':unittest.main()
