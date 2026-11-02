"""Ontology layer, step 1: the register.

Links the 604 Study and Read rows of the tier catalog (ontology_layer/catalog/text-tiers-described.csv)
to their texts in data/sources.json, gathers the teachings in each row's scope from data/teachings/,
assigns every row to a work unit, and writes:

  ontology_layer/register/texts.jsonl     one line per row (604)
  ontology_layer/register/units.json      unit -> rows, family, model
  ontology_layer/_inputs/<unit>/          rows.json, teachings.jsonl, vocab.jsonl (agent inputs)

Run from tradition-ontology/:  python3 scripts/ontology_layer_register.py
Reads data/ only; never writes to it.
"""
import collections
import csv
import glob
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from ontology_layer_overrides import O, NOTES, NOT  # noqa: E402

LAYER = os.path.join(ROOT, 'ontology_layer')
CATALOG = os.path.join(LAYER, 'catalog', 'text-tiers-described.csv')
CANDS = os.path.join(LAYER, 'catalog', 'match_candidates.json')


def norm(s):
    s = unicodedata.normalize('NFKD', str(s))
    return ''.join(c for c in s if not unicodedata.combining(c)).lower()


def toks(ref):
    out = []
    for p in str(ref).split('.'):
        p = p.strip()
        m = re.match(r'^(\d+)(?:\s*[-–]\s*(\d+))?', p)
        if m:
            a = int(m.group(1))
            b = int(m.group(2)) if m.group(2) else a
            out.append((a, b))
        else:
            out.append(norm(p))
    return out


def spec_match(ref, spec):
    """True if a teaching ref falls inside a scope spec ('2', '3.27-28', 'su', '~substring')."""
    if spec.startswith('~'):
        return norm(spec[1:]) in norm(ref)
    rt, st = toks(ref), toks(spec)
    if not rt:
        return False
    for i, s in enumerate(st):
        if i >= len(rt):
            return True
        r = rt[i]
        if isinstance(s, tuple) and isinstance(r, tuple):
            if i < len(st) - 1:
                if s != r:
                    return False
            elif r[1] < s[0] or r[0] > s[1]:
                return False
        elif isinstance(s, str) and isinstance(r, str):
            if s != r:
                return False
        else:
            return False
    return True


# ---- units: (unit id, family label, model) and the rule that assigns a row to it
UNITS = {
    'S01-vedic': ('Vedic hymns, principal Upaniṣads, Vedāṅga', 'opus'),
    'S02-epic-purana-dharma': ('Epics, Gītās, Purāṇas, dharma, Vaiṣṇava theology', 'opus'),
    'S03-samkhya-yoga': ('Sāṃkhya and the Yoga Sūtra', 'opus'),
    'S04-nyaya-mimamsa-surveys': ('Nyāya-Vaiśeṣika, Mīmāṃsā, surveys, grammar and sound', 'opus'),
    'S05-vedanta': ('Vedānta: Advaita, Viśiṣṭādvaita, Dvaita, Bhedābheda', 'opus'),
    'S06-saiva-sakta': ('Śaiva and Śākta', 'opus'),
    'S07-hatha-nath': ('Haṭha, Nāth and breath', 'opus'),
    'S08-ayurveda-arts': ('Āyurveda, aesthetics, music, Jyotiṣa', 'opus'),
    'S09-jain': ('Jain', 'opus'),
    'S10-pali': ('Pali canon and Theravāda', 'opus'),
    'S11-mahayana-vajrayana': ('Abhidharma, Madhyamaka, Yogācāra, buddha-nature, logic, Vajrayāna', 'opus'),
    'R01-minor-upanisads': ('Minor Upaniṣads and Vedāṅga', 'sonnet'),
    'R02-mahabharata': ('Mahābhārata: the Gītā and its companions', 'sonnet'),
    'R03-gitas-puranas-dharma': ('Other Gītās, Purāṇas, Rāmāyaṇa, dharma', 'sonnet'),
    'R04-schools-vedanta-bhakti': ('Six schools, Vedānta, Vaiṣṇava and devotional movements', 'sonnet'),
    'R05-hatha-nath': ('Haṭha and Nāth practice', 'sonnet'),
    'R06-saiva-sakta': ('Śaiva and Śākta practice', 'sonnet'),
    'R07-jain-sciences-later': ('Jain, sciences and arts, later layers', 'sonnet'),
    'R08-pali-khuddaka': ('Pali Khuddaka Nikāya (Dhammapada and others)', 'sonnet'),
    'R09-pali-nikayas': ('Pali Nikāyas, Abhidhamma, Visuddhimagga', 'sonnet'),
    'R10-mahayana-tibet': ('Mahāyāna, Vajrayāna, siddhas, Tibet', 'sonnet'),
}


def unit_of(r):
    sec, grp, tier = r['Section'], r['Tradition / group'], r['Tier']
    S = tier == 'Study'
    if sec.startswith('I.1 '):
        return 'S01-vedic' if S else 'R01-minor-upanisads'
    if sec.startswith('I.2 ') or sec.startswith('I.3 '):
        if S:
            return 'S02-epic-purana-dharma'
        return 'R02-mahabharata' if grp == 'Mahābhārata' else 'R03-gitas-puranas-dharma'
    if sec.startswith('I.4 '):
        if S:
            if grp in ('Sāṃkhya', 'Yoga'):
                return 'S03-samkhya-yoga'
            if grp in ('Nyāya', 'Vaiśeṣika', 'Mīmāṃsā'):
                return 'S04-nyaya-mimamsa-surveys'
            return 'S05-vedanta'
        return 'R04-schools-vedanta-bhakti'
    if sec.startswith('I.5 '):
        return 'S07-hatha-nath' if S else 'R05-hatha-nath'
    if sec.startswith('I.6 ') or sec.startswith('I.7 '):
        return 'S06-saiva-sakta' if S else 'R06-saiva-sakta'
    if sec.startswith('I.8 ') or sec.startswith('I.9 ') or sec.startswith('I.14 '):
        return 'S02-epic-purana-dharma' if S else 'R04-schools-vedanta-bhakti'
    if sec.startswith('I.10 '):
        return 'S09-jain' if S else 'R07-jain-sciences-later'
    if sec.startswith('I.11 '):
        pali = grp.startswith('Pali')
        if S:
            return 'S10-pali' if pali else 'S11-mahayana-vajrayana'
        if pali:
            return 'R08-pali-khuddaka' if 'Khuddaka' in grp else 'R09-pali-nikayas'
        return 'R10-mahayana-tibet'
    if sec.startswith('I.12 '):
        return 'S04-nyaya-mimamsa-surveys' if S else 'R04-schools-vedanta-bhakti'
    if sec.startswith('I.13 '):
        if S:
            return 'S04-nyaya-mimamsa-surveys' if grp.startswith('Grammar') else 'S08-ayurveda-arts'
        return 'R07-jain-sciences-later'
    if sec.startswith('Part IV'):
        if grp in ('Tibet', 'East Asia'):
            return 'R10-mahayana-tibet'
        return 'R07-jain-sciences-later'
    raise ValueError((sec, grp))


# Read rows whose catalog note marks a passage as Study: those passages go to the Study unit as extra why passages.
STUDY_PASSAGES_IN_READ = {
    53: 'S01-vedic', 316: 'S04-nyaya-mimamsa-surveys', 324: 'S05-vedanta', 362: 'S05-vedanta',
    867: 'S09-jain', 1025: 'S10-pali', 1033: 'S10-pali', 1092: 'S11-mahayana-vajrayana',
}


EXTRA_SCOPE = {1033: ['3'], 1025: ['6', '~paticca', '~dependent'], 324: ['~intro', '~upodghata'], 867: ['~ganadhara']}


def extra_ok(n, ref):
    specs = EXTRA_SCOPE.get(n)
    return True if not specs else any(spec_match(ref, sp) for sp in specs)


def main():
    src = json.load(open(os.path.join(ROOT, 'data', 'sources.json')))
    SRC = {s['id']: s for s in src}
    rows_all = list(csv.DictReader(open(CATALOG, encoding='utf-8-sig')))
    rows = [r for r in rows_all if r['Tier'] in ('Study', 'Read')]
    cands = {str(o['n']): o['cands'] for o in json.load(open(CANDS))}
    T = collections.defaultdict(list)
    TID = {}
    for f in glob.glob(os.path.join(ROOT, 'data', 'teachings', '*.jsonl')):
        for line in open(f):
            if line.strip():
                d = json.loads(line)
                T[d['source']].append(d)
                TID[d['id']] = d
    # sources that have their own catalog row (any tier), used to compute the 'other discourses' groups
    explicit = set()
    for r in rows_all:
        c = cands.get(r['#']) or []
        if c and c[0][0] >= 0.9:
            explicit.add(c[0][1])
    for v in O.values():
        if isinstance(v, list):
            for it in v:
                explicit.add(it if isinstance(it, str) else it[0])

    def kids(parent):
        return [s['id'] for s in src if s.get('part_of') == parent]

    special = {
        'SANKARA_UP': [s['id'] for s in src if s['id'].endswith('-bhasya-sankara') and 'upanisad' in s['id']],
        'MADHVA_UP': [s['id'] for s in src if s['id'].endswith('-bhasya-madhva') and 'upanisad' in s['id']],
        'DN_OTHERS': [k for k in kids('src:digha-nikaya') if k not in explicit],
        'MN_OTHERS': [k for k in kids('src:majjhima-nikaya') if k not in explicit],
        'AN_OTHERS': [k for k in kids('src:anguttara-nikaya') if k not in explicit]
        + [('src:anguttara-nikaya', NOT, ['3.65', '6.63'])],
    }
    out = []
    missing = collections.Counter()
    for r in rows:
        n = int(r['#'])
        spec = O.get(n)
        how = 'checked by hand'
        if spec is None:
            c = cands.get(r['#']) or []
            spec = [c[0][1]] if c else []
            how = 'exact title match' if c and c[0][0] >= 0.99 else 'title match, unchecked'
        if isinstance(spec, str):
            spec = special[spec]
            how = 'group, computed'
        items = []
        for it in spec:
            if isinstance(it, str):
                items.append({'src': it, 'mode': 'all', 'specs': []})
            elif len(it) == 2:
                items.append({'src': it[0], 'mode': 'include', 'specs': it[1]})
            else:
                items.append({'src': it[0], 'mode': 'exclude', 'specs': it[2]})
        tids, lv, found = [], collections.Counter(), []
        for it in items:
            sid = it['src']
            if sid not in SRC:
                missing[sid] += 1
                it['missing'] = True
                continue
            found.append(sid)
            for t in T.get(sid, []):
                ref = t['location']['ref']
                ok = True
                if it['mode'] == 'include':
                    ok = any(spec_match(ref, s) for s in it['specs'])
                elif it['mode'] == 'exclude':
                    ok = not any(spec_match(ref, s) for s in it['specs'])
                if ok:
                    tids.append(t['id'])
                    lv[t['verification']['level']] += 1
        unit = unit_of(r)
        out.append({
            'n': n, 'tier': r['Tier'], 'section': r['Section'], 'group': r['Tradition / group'], 'text': r['Text'],
            'what': r['What it talks about'], 'role': r['Role'], 'why_this_tier': r['Why this tier'],
            'why_lives_in': r['Its why lives in (Study source)'], 'passages_tiered_differently': r['Passages tiered differently'],
            'tags': r['Tags'], 'checked_against_source_database': r['Checked against source database'],
            'feeds_layer': r['Feeds layer'], 'also_feeds': r['Also feeds'],
            'sources': items, 'found_sources': found, 'mapping': how, 'scope_note': NOTES.get(n, ''),
            'teachings': tids, 'teaching_levels': dict(lv), 'unit': unit,
            'study_passages_unit': STUDY_PASSAGES_IN_READ.get(n, ''),
        })
    os.makedirs(os.path.join(LAYER, 'register'), exist_ok=True)
    with open(os.path.join(LAYER, 'register', 'texts.jsonl'), 'w') as f:
        for x in out:
            f.write(json.dumps(x, ensure_ascii=False) + '\n')
    units = {u: {'family': UNITS[u][0], 'model': UNITS[u][1], 'rows': [], 'extra_why_rows': []} for u in UNITS}
    for x in out:
        units[x['unit']]['rows'].append(x['n'])
        if x['study_passages_unit']:
            units[x['study_passages_unit']]['extra_why_rows'].append(x['n'])
    # inputs per unit
    vocab_files = {}
    for k in ('concepts', 'terms', 'obstacles', 'practices'):
        for e in json.load(open(os.path.join(ROOT, 'data', k + '.json'))):
            vocab_files[e['id']] = (k, e)
    byn = {x['n']: x for x in out}
    for u, info in units.items():
        d = os.path.join(LAYER, '_inputs', u)
        os.makedirs(d, exist_ok=True)
        rws = [byn[n] for n in info['rows']] + [byn[n] for n in info['extra_why_rows']]
        json.dump([{k: v for k, v in x.items() if k != 'teachings'} | {'teaching_count': len(x['teachings']),
                   'extra_why_passages_only': x['n'] in info['extra_why_rows']} for x in rws],
                  open(os.path.join(d, 'rows.json'), 'w'), ensure_ascii=False, indent=1)
        seen, refs = set(), set()
        with open(os.path.join(d, 'teachings.jsonl'), 'w') as f:
            for x in rws:
                for tid in x['teachings']:
                    if x['n'] in info['extra_why_rows'] and not extra_ok(x['n'], TID[tid]['location']['ref']):
                        continue
                    if (x['n'], tid) in seen:
                        continue
                    seen.add((x['n'], tid))
                    t = TID[tid]
                    links = {k: t.get(k) or [] for k in ('concepts', 'terms', 'obstacles', 'practices')}
                    for v in links.values():
                        refs.update(v)
                    rec = {'row': x['n'], 'id': tid, 'ref': t['location']['ref'], 'level': t['verification']['level'],
                           'types': t.get('types') or []}
                    if t.get('speaker'):
                        rec['speaker'] = t['speaker']
                    rec['paraphrase'] = t.get('paraphrase') or (t.get('original') or {}).get('text', '')
                    rec.update({k: v for k, v in links.items() if v})
                    f.write(json.dumps(rec, ensure_ascii=False) + '\n')
        with open(os.path.join(d, 'vocab.jsonl'), 'w') as f:
            for i in sorted(refs):
                if i not in vocab_files:
                    continue
                k, e = vocab_files[i]
                name = e.get('name') or e.get('term') or i
                defs = e.get('definitions') or []
                df = (defs[0].get('definition') if defs else '') or e.get('description') or e.get('method_summary') or ''
                f.write(json.dumps({'id': i, 'kind': k, 'name': name, 'gloss': df[:140]}, ensure_ascii=False) + '\n')
        info['teaching_count'] = sum(len(x['teachings']) for x in rws)
    json.dump(units, open(os.path.join(LAYER, 'register', 'units.json'), 'w'), ensure_ascii=False, indent=1)
    print('rows', len(out), 'missing source ids', dict(missing))
    for u, info in units.items():
        print(f"{u:28} rows {len(info['rows']):3} +{len(info['extra_why_rows'])} teachings {info['teaching_count']:5} {info['model']}")


if __name__ == '__main__':
    main()
