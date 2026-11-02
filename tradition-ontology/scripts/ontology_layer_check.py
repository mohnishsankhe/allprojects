"""Check ontology-layer shards against ontology_layer/SCHEMA.md.

  python3 scripts/ontology_layer_check.py shards/ontology_layer/S03-samkhya-yoga   # one unit
  python3 scripts/ontology_layer_check.py --all                                  # every unit

Errors make the exit code 1. Warnings do not.
"""
import collections
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHARDS = os.path.join(ROOT, 'shards', 'ontology_layer')
LAYER = os.path.join(ROOT, 'ontology_layer')

RELATIONS = {'causes', 'conditions', 'increases', 'decreases', 'obstructs', 'removes', 'opposes', 'evolves-into',
             'transforms-into', 'leads-to', 'sustains', 'seated-in', 'part-of', 'composed-of', 'is-a', 'has-quality',
             'sign-of', 'known-by'}
LAYERS = {'L0', 'L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L7', 'M', 'W'}
DOMAINS = {'exists', 'arising', 'mind', 'consciousness', 'body', 'karma', 'suffering', 'transformation', 'cosmology', 'living'}
CLAIMS = {'inner', 'body', 'cosmos', 'social', 'ultimate'}
BASES = {'stated', 'inferred', 'outline'}
CONF = {'high', 'moderate', 'low'}
KINDS = {'method', 'conduct', 'counsel', 'devotion', 'mantra', 'ritual', 'regimen', 'sign', 'warning'}
LINKS = {'same-text', 'same-tradition', 'other-tradition'}
NODE_KINDS = {'quality', 'faculty', 'substance', 'tissue', 'channel', 'wind', 'place', 'state', 'affliction',
              'latent-tendency', 'process', 'principle', 'being', 'practice', 'other'}
GRADES = {'exact', 'partial', 'analogous'}
FAMILIES = set('''vedic upanisad brahmana vedanga mantra-nada gita epic purana ramayana yoga-vasistha dharma samkhya yoga-sutra
nyaya-vaisesika mimamsa carvaka surveys vedanta advaita visistadvaita dvaita bhedabheda vallabha pancaratra bhagavata gaudiya
alvar varkari mahanubhava sant bhakti pasupata saiva-siddhanta tamil-saiva trika spanda pratyabhijna krama kaula virasaiva
sakta srividya hatha ayurveda rasa-sastra aesthetics music jyotisa vastu jain pali abhidharma madhyamaka yogacara
buddha-nature mahayana buddhist-logic vajrayana siddha tibetan zen tamil later'''.split())
ID_RE = re.compile(r'^(why|res|nd):([a-z0-9-]+):([a-z0-9][a-z0-9-]{0,59})$')
RESTRICT_WORDS = re.compile(r'kumbhaka|retention|retain(ing)? the breath|vajrol|khecar|mercury|metal|fast(ing)? for|'
                            r'sexual|maithuna|cutting|cut the|amaroli|sahajol', re.I)


def load_jsonl(p):
    out, errs = [], []
    if not os.path.exists(p):
        return out, errs
    for i, line in enumerate(open(p, encoding='utf-8'), 1):
        if not line.strip():
            continue
        try:
            out.append(json.loads(line))
        except Exception as e:  # noqa: BLE001
            errs.append(f'{os.path.basename(p)}:{i}: bad JSON ({e})')
    return out, errs


def repo_ids():
    ids = set()
    for k in ('concepts', 'terms', 'obstacles', 'practices', 'paths', 'phenomenology'):
        p = os.path.join(ROOT, 'data', k + '.json')
        if os.path.exists(p):
            ids.update(e['id'] for e in json.load(open(p)))
    teach = {}
    for f in glob.glob(os.path.join(ROOT, 'data', 'teachings', '*.jsonl')):
        for line in open(f):
            if line.strip():
                d = json.loads(line)
                teach[d['id']] = d['verification']['level']
    return ids, teach


def main(argv):
    units = json.load(open(os.path.join(LAYER, 'register', 'units.json')))
    rows = {}
    for line in open(os.path.join(LAYER, 'register', 'texts.jsonl')):
        x = json.loads(line)
        rows[x['n']] = x
    vocab, teach = repo_ids()
    all_dirs = sorted(d for d in glob.glob(os.path.join(SHARDS, '*')) if os.path.isdir(d) and not os.path.basename(d).startswith('_'))
    targets = all_dirs if argv[1:] == ['--all'] else [os.path.abspath(a) for a in argv[1:]]
    # global pools for resolution
    nodes_all, whys_all = {}, {}
    for d in all_dirs:
        for n in load_jsonl(os.path.join(d, 'nodes.jsonl'))[0]:
            if isinstance(n, dict) and 'id' in n:
                nodes_all[n['id']] = n
        for w in load_jsonl(os.path.join(d, 'whys.jsonl'))[0]:
            if isinstance(w, dict) and 'id' in w:
                whys_all[w['id']] = w
    total_err = 0
    for d in targets:
        unit = os.path.basename(d)
        uinfo = units.get(unit, {})
        urows = set(uinfo.get('rows', [])) | set(uinfo.get('extra_why_rows', []))
        scope = set()
        for n in urows:
            scope.update(rows[n]['teachings'])
        E, W = [], []
        whys, e1 = load_jsonl(os.path.join(d, 'whys.jsonl'))
        res, e2 = load_jsonl(os.path.join(d, 'results.jsonl'))
        nodes, e3 = load_jsonl(os.path.join(d, 'nodes.jsonl'))
        E += e1 + e2 + e3
        for x in whys:
            if isinstance(x, dict) and 'id' in x:
                whys_all.setdefault(x['id'], x)
        for x in nodes:
            if isinstance(x, dict) and 'id' in x:
                nodes_all.setdefault(x['id'], x)
        seen = collections.Counter(x.get('id') for x in whys + res + nodes if isinstance(x, dict))
        for i, c in seen.items():
            if c > 1:
                E.append(f'duplicate id {i} ({c}x)')

        def check_id(x, kind):
            i = x.get('id', '')
            m = ID_RE.match(i)
            if not m or m.group(1) != kind:
                E.append(f'bad id {i!r} (want {kind}:<family>:<slug>)')
            elif m.group(2) not in FAMILIES:
                W.append(f'{i}: family {m.group(2)!r} not in the SCHEMA list')

        def check_node(i, where):
            if i in vocab or i in nodes_all:
                return
            E.append(f'{where}: node {i!r} not found in data/ or any nodes.jsonl')

        def check_cites(x, where, need):
            cs = x.get('cites')
            if not isinstance(cs, list):
                E.append(f'{where}: cites must be a list')
                return
            for c in cs:
                if c not in teach:
                    E.append(f'{where}: cite {c!r} not in data/teachings')
                elif scope and c not in scope:
                    W.append(f'{where}: cite {c} is outside this unit\'s rows')
            b = x.get('basis')
            if b not in BASES and 'kind' not in x:
                E.append(f'{where}: basis {b!r}')
            if b in ('stated', 'inferred') and not cs:
                E.append(f'{where}: basis {b} needs cites')
            if b == 'outline' and not (x.get('ref_hint') or '').strip():
                E.append(f'{where}: outline needs ref_hint')
            if b == 'inferred' and not (x.get('notes') or '').strip():
                W.append(f'{where}: inferred link should say how in notes')

        def check_sub(x, where, key):
            v = x.get(key)
            if v in (None, '', [], {}):
                return
            items = v if isinstance(v, list) else [v]
            for it in items:
                if not isinstance(it, dict) or not (it.get('text') or '').strip():
                    E.append(f'{where}: {key} items need text')
                    continue
                for c in it.get('cites') or []:
                    if c not in teach:
                        E.append(f'{where}: {key} cite {c!r} not in data/teachings')

        for n in nodes:
            check_id(n, 'nd')
            for k in ('name', 'kind', 'gloss'):
                if not (n.get(k) or '').strip():
                    E.append(f"{n.get('id')}: node needs {k}")
            if n.get('kind') and n['kind'] not in NODE_KINDS:
                E.append(f"{n.get('id')}: node kind {n['kind']!r}")
            for s in n.get('same_as') or []:
                if s not in vocab:
                    W.append(f"{n.get('id')}: same_as {s} not in data/")
        for w in whys:
            i = w.get('id', '?')
            check_id(w, 'why')
            if not (w.get('statement') or '').strip():
                E.append(f'{i}: statement')
            if w.get('relation') not in RELATIONS:
                E.append(f"{i}: relation {w.get('relation')!r}")
            for k in ('subject', 'object'):
                v = w.get(k)
                if not isinstance(v, list) or not v:
                    E.append(f'{i}: {k} must be a non-empty list')
                else:
                    for nid in v:
                        check_node(nid, i)
            ls = w.get('layers') or []
            if not ls or any(l not in LAYERS for l in ls) or ('W' in ls and len(ls) > 1):
                E.append(f'{i}: layers {ls}')
            if not w.get('domain') or any(dm not in DOMAINS for dm in w.get('domain', [])):
                E.append(f"{i}: domain {w.get('domain')}")
            if w.get('claim') not in CLAIMS:
                E.append(f"{i}: claim {w.get('claim')!r}")
            if w.get('confidence') not in CONF:
                E.append(f"{i}: confidence {w.get('confidence')!r}")
            if w.get('basis') not in BASES:
                E.append(f"{i}: basis {w.get('basis')!r}")
            check_cites(w, i, True)
            for r in w.get('rows') or []:
                if r not in rows:
                    E.append(f'{i}: row {r} not in the register')
                elif urows and r not in urows:
                    W.append(f'{i}: row {r} is not one of this unit\'s rows')
            if not w.get('rows'):
                E.append(f'{i}: rows')
            check_sub(w, i, 'shows_as')
            check_sub(w, i, 'test')
            for c in w.get('corresponds') or []:
                if c.get('grade') not in GRADES:
                    E.append(f'{i}: corresponds grade {c.get("grade")!r}')
                if c.get('why') not in whys_all:
                    W.append(f"{i}: corresponds to unknown why {c.get('why')}")
        for x in res:
            i = x.get('id', '?')
            check_id(x, 'res')
            for k in ('statement', 'for'):
                if not (x.get(k) or '').strip():
                    E.append(f'{i}: {k}')
            if x.get('kind') not in KINDS:
                E.append(f"{i}: kind {x.get('kind')!r}")
            r = x.get('row')
            if r not in rows:
                E.append(f'{i}: row {r!r} not in the register')
            elif urows and r not in urows:
                W.append(f'{i}: row {r} is not one of this unit\'s rows')
            ls = x.get('layers') or []
            if not ls or any(l not in LAYERS for l in ls):
                E.append(f'{i}: layers {ls}')
            if x.get('basis') not in ('stated', 'outline', 'inferred'):
                E.append(f"{i}: basis {x.get('basis')!r}")
            check_cites(x, i, True)
            if x.get('confidence') not in CONF:
                E.append(f"{i}: confidence {x.get('confidence')!r}")
            ro = x.get('rests_on') or []
            if not ro and not (x.get('why_gap') or '').strip():
                E.append(f'{i}: needs rests_on or why_gap')
            for link in ro:
                if link.get('why') not in whys_all:
                    E.append(f"{i}: rests_on unknown why {link.get('why')!r}")
                if link.get('link') not in LINKS:
                    E.append(f"{i}: rests_on link {link.get('link')!r}")
            for nid in x.get('targets') or []:
                check_node(nid, i)
            if not isinstance(x.get('restricted'), bool):
                E.append(f'{i}: restricted must be true or false')
            elif not x['restricted'] and x.get('kind') == 'method' and RESTRICT_WORDS.search(x.get('statement', '')):
                W.append(f'{i}: looks like a restricted practice; check restricted=true and summary-only wording')
            check_sub(x, i, 'warnings')
            check_sub(x, i, 'test')
        # coverage of the unit's rows
        covered = collections.Counter()
        for w in whys:
            for r in w.get('rows') or []:
                covered[r] += 1
        for x in res:
            covered[x.get('row')] += 1
        empty = [n for n in sorted(uinfo.get('rows', [])) if not covered[n]]
        print(f'== {unit}: {len(whys)} whys, {len(res)} results, {len(nodes)} nodes; {len(E)} errors, {len(W)} warnings')
        if empty:
            print(f'   rows with nothing yet: {empty}')
        for e in E[:60]:
            print('   ERROR', e)
        if len(E) > 60:
            print(f'   ... {len(E) - 60} more errors')
        for w in W[:25]:
            print('   warn ', w)
        if len(W) > 25:
            print(f'   ... {len(W) - 25} more warnings')
        total_err += len(E)
    return 1 if total_err else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
