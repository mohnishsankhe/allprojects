"""Print passages. Usage: python3 fetch.py <slug> <ref>[,<ref>...] [maxchars] [fields]
Also prints data/teachings paraphrase + level for tea:<slug>:<ref> (or covering, via insight.ontology)."""
import json, sys
sys.path.insert(0, '/home/user/allprojects/tradition-ontology')
ROOT = '/home/user/allprojects/tradition-ontology'
from insight import ontology as O
slug, refs = sys.argv[1], sys.argv[2].split(',')
mx = int(sys.argv[3]) if len(sys.argv) > 3 else 1200
fields = sys.argv[4].split(',') if len(sys.argv) > 4 else ['iast', 'commentary_iast', 'pali', 'en_sujato']
segs = {json.loads(l)['ref']: json.loads(l) for l in open(f'{ROOT}/sources_raw/prepared/{slug}/segments.jsonl', encoding='utf-8') if l.strip()}
tslug = {'yoga-sutra': 'yoga-sutra'}.get(slug, slug)
for r in refs:
    s = segs.get(r)
    print(f'--- {slug} {r}', '(MISSING SEGMENT)' if not s else '')
    if s:
        for f in fields:
            if s.get(f): print(f'  [{f}]', s[f][:mx].replace('\n', ' '))
    for ts in ([tslug, 'yoga-bhasya'] if slug == 'yoga-sutra' else [tslug]):
        tid = f'tea:{ts}:{r}'
        t = O.teaching(tid)
        if t: print(f'  <{tid} -> {t["id"]} {t["level"]} citable={O.citable(tid)}>', (t['paraphrase'] or '')[:int(__import__('os').environ.get('PL','450'))].replace('\n', ' '))
        else: print(f'  <{tid} not in data>')
