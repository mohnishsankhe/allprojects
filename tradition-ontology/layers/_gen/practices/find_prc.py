"""Search data/practices.json by id/name/method_summary regex. Usage: python3 find_prc.py <regex> [lineage-substr]"""
import json, re, sys
ROOT = '/home/user/allprojects/tradition-ontology'
d = json.load(open(f'{ROOT}/data/practices.json', encoding='utf-8'))
rx = re.compile(sys.argv[1], re.I); lin = sys.argv[2] if len(sys.argv) > 2 else ''
for e in d:
    hay = e['id'] + ' ' + e['name'] + ' ' + ' '.join(e.get('names', []) if isinstance(e.get('names'), list) and all(isinstance(x, str) for x in e.get('names', [])) else [])
    if rx.search(hay) and (not lin or any(lin in l for l in e['lineages'])):
        print(e['id'], '|', e['name'][:60], '|', ','.join(e['lineages'])[:60], '|', e['verification']['level'], '| restricted=', e.get('restricted'), '| stage=', e.get('stage'))
