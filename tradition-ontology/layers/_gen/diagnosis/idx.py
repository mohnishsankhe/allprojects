"""Index helper: teachings and prepared segments for the diagnosis layer.
Usage: python3 idx.py teach <slug> [refprefix...]   -> list ids, level, paraphrase[:N]
       python3 idx.py seg <slug> <ref> [field] [maxchars]   -> print segment text
       python3 idx.py segrefs <slug>              -> list refs
"""
import json, sys, os
ROOT = '/home/user/allprojects/tradition-ontology'
def teachings(slug):
    p = f'{ROOT}/data/teachings/{slug}.jsonl'
    out = []
    if not os.path.exists(p): return out
    for line in open(p, encoding='utf-8'):
        line = line.strip()
        if line: out.append(json.loads(line))
    return out
def segments(slug):
    p = f'{ROOT}/sources_raw/prepared/{slug}/segments.jsonl'
    return [json.loads(l) for l in open(p, encoding='utf-8') if l.strip()]
if __name__ == '__main__':
    cmd, slug = sys.argv[1], sys.argv[2]
    if cmd == 'teach':
        pre = sys.argv[3:] or ['']
        N = int(os.environ.get('N', '110'))
        for t in teachings(slug):
            r = t['location']['ref']
            if any(r.startswith(p) for p in pre):
                print(t['id'], t['verification']['level'], (t.get('paraphrase') or '')[:N].replace('\n', ' '))
    elif cmd == 'segrefs':
        print(' '.join(s['ref'] for s in segments(slug)))
    elif cmd == 'seg':
        ref = sys.argv[3]; field = sys.argv[4] if len(sys.argv) > 4 else None
        mx = int(sys.argv[5]) if len(sys.argv) > 5 else 3000
        for s in segments(slug):
            if s['ref'] == ref:
                if field: print(str(s.get(field, ''))[:mx])
                else: print(json.dumps({k: (v[:mx] if isinstance(v, str) else v) for k, v in s.items()}, ensure_ascii=False))
