"""Ontology layer, step 3: merge the unit shards into the layer.

  python3 scripts/ontology_layer_merge.py            # merge every unit in shards/ontology_layer/
  python3 scripts/ontology_layer_merge.py --index    # only write ontology_layer/_inputs/WHY_INDEX.tsv

Writes ontology_layer/whys.jsonl, results.jsonl, nodes.jsonl, gaps.jsonl and graph/nodes.csv, graph/edges.csv.
Each entry gets a computed `verification` block from the teachings it cites, and a `unit` field.
Never writes to data/.
"""
import collections
import csv
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHARDS = os.path.join(ROOT, 'shards', 'ontology_layer')
LAYER = os.path.join(ROOT, 'ontology_layer')
RANK = {'skeleton': 0, 'sourced': 1, 'text-verified': 2}


def load_jsonl(p):
    out = []
    if os.path.exists(p):
        for line in open(p, encoding='utf-8'):
            if line.strip():
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return out


def teaching_levels():
    lv = {}
    for f in glob.glob(os.path.join(ROOT, 'data', 'teachings', '*.jsonl')):
        for line in open(f):
            if line.strip():
                d = json.loads(line)
                lv[d['id']] = d['verification']['level']
    return lv


def vocab_names():
    names = {}
    for k in ('concepts', 'terms', 'obstacles', 'practices', 'paths', 'phenomenology'):
        p = os.path.join(ROOT, 'data', k + '.json')
        if os.path.exists(p):
            for e in json.load(open(p)):
                names[e['id']] = e.get('name') or e.get('term') or e['id']
    return names


def verification(entry, lv):
    cites = [c for c in entry.get('cites') or [] if c in lv]
    if entry.get('basis') == 'outline' or not cites:
        return {'level': 'outline', 'cited': len(cites), 'by_level': {}}
    counts = collections.Counter(lv[c] for c in cites)
    low = min(RANK[lv[c]] for c in cites)
    level = {0: 'skeleton', 1: 'sourced', 2: 'text-verified'}[low]
    return {'level': level, 'cited': len(cites), 'by_level': dict(counts)}


def units():
    return sorted(d for d in glob.glob(os.path.join(SHARDS, '*')) if os.path.isdir(d) and not os.path.basename(d).startswith('_'))


def write_index(whys, names):
    p = os.path.join(LAYER, '_inputs', 'WHY_INDEX.tsv')
    with open(p, 'w', encoding='utf-8') as f:
        f.write('id\tfamily\tlayers\trelation\tsubject\tobject\tstatement\n')
        for w in sorted(whys, key=lambda x: x['id']):
            fam = w['id'].split(':')[1]
            subj = '; '.join(f"{s} ({names.get(s, s)})" for s in w.get('subject') or [])
            obj = '; '.join(f"{o} ({names.get(o, o)})" for o in w.get('object') or [])
            st = (w.get('statement') or '').replace('\t', ' ').replace('\n', ' ')
            f.write(f"{w['id']}\t{fam}\t{','.join(w.get('layers') or [])}\t{w.get('relation')}\t{subj}\t{obj}\t{st}\n")
    return p


def main(argv):
    lv = teaching_levels()
    names = vocab_names()
    whys, results, nodes = [], [], []
    for d in units():
        u = os.path.basename(d)
        for n in load_jsonl(os.path.join(d, 'nodes.jsonl')):
            n['unit'] = u
            nodes.append(n)
        for w in load_jsonl(os.path.join(d, 'whys.jsonl')):
            w['unit'] = u
            whys.append(w)
        for r in load_jsonl(os.path.join(d, 'results.jsonl')):
            r['unit'] = u
            results.append(r)
    for n in nodes:
        names.setdefault(n['id'], n.get('name', n['id']))
    if argv[1:] == ['--index']:
        p = write_index(whys, names)
        print('wrote', p, len(whys), 'whys')
        return 0
    # de-duplicate by id (first wins; later duplicates logged)
    dup = []

    def dedupe(xs):
        seen, out = set(), []
        for x in xs:
            if x.get('id') in seen:
                dup.append((x.get('id'), x.get('unit')))
                continue
            seen.add(x.get('id'))
            out.append(x)
        return out
    whys, results, nodes = dedupe(whys), dedupe(results), dedupe(nodes)
    for x in whys + results:
        x['verification'] = verification(x, lv)
    why_ids = {w['id'] for w in whys}
    gaps = []
    for r in results:
        bad = [link['why'] for link in r.get('rests_on') or [] if link.get('why') not in why_ids]
        if bad:
            r['rests_on'] = [link for link in r['rests_on'] if link.get('why') in why_ids]
        if not r.get('rests_on'):
            gaps.append({'kind': 'result-without-why', 'id': r['id'], 'row': r.get('row'), 'unit': r['unit'],
                         'for': r.get('for'), 'why_gap': r.get('why_gap') or '', 'dropped_links': bad})
    for x in whys + results:
        if x['verification']['level'] == 'outline':
            gaps.append({'kind': 'needs-passage', 'id': x['id'], 'rows': x.get('rows') or [x.get('row')],
                         'unit': x['unit'], 'ref_hint': x.get('ref_hint') or ''})
    os.makedirs(os.path.join(LAYER, 'graph'), exist_ok=True)
    for name, xs in (('whys', whys), ('results', results), ('nodes', nodes), ('gaps', gaps)):
        with open(os.path.join(LAYER, name + '.jsonl'), 'w', encoding='utf-8') as f:
            for x in xs:
                f.write(json.dumps(x, ensure_ascii=False) + '\n')
    # graph export
    node_rows = {}

    def add_node(i, kind, label, extra=''):
        if i not in node_rows:
            node_rows[i] = (i, kind, label, extra)
    edges = []
    for w in whys:
        add_node(w['id'], 'why', w['statement'][:160], ','.join(w.get('layers') or []))
        for s in w.get('subject') or []:
            add_node(s, s.split(':')[0], names.get(s, s))
            edges.append((s, w['id'], 'subject-of', w['verification']['level']))
        for o in w.get('object') or []:
            add_node(o, o.split(':')[0], names.get(o, o))
            edges.append((w['id'], o, w.get('relation'), w['verification']['level']))
        for c in w.get('cites') or []:
            edges.append((w['id'], c, 'cites', lv.get(c, '')))
        for c in w.get('corresponds') or []:
            if c.get('why') in why_ids:
                edges.append((w['id'], c['why'], 'corresponds-' + c.get('grade', ''), ''))
    for r in results:
        add_node(r['id'], 'result', r['statement'][:160], ','.join(r.get('layers') or []))
        for link in r.get('rests_on') or []:
            edges.append((r['id'], link['why'], 'rests-on-' + link.get('link', ''), r['verification']['level']))
        for t in r.get('targets') or []:
            add_node(t, t.split(':')[0], names.get(t, t))
            edges.append((r['id'], t, 'targets', ''))
        for c in r.get('cites') or []:
            edges.append((r['id'], c, 'cites', lv.get(c, '')))
    with open(os.path.join(LAYER, 'graph', 'nodes.csv'), 'w', newline='', encoding='utf-8') as f:
        wr = csv.writer(f)
        wr.writerow(['id', 'kind', 'label', 'layers'])
        wr.writerows(sorted(node_rows.values()))
    with open(os.path.join(LAYER, 'graph', 'edges.csv'), 'w', newline='', encoding='utf-8') as f:
        wr = csv.writer(f)
        wr.writerow(['source', 'target', 'type', 'verification'])
        wr.writerows(edges)
    write_index(whys, names)
    print(f'whys {len(whys)}, results {len(results)}, nodes {len(nodes)}, gaps {len(gaps)}, edges {len(edges)}; duplicates dropped {len(dup)}')
    if dup:
        print('  duplicate ids:', dup[:20])
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
