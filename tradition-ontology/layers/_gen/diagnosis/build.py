"""Build layers/diagnosis.json from the entry modules, then validate by code.
Run: python3 layers/_gen/diagnosis/build.py   (writes layers/diagnosis.json and layers/_gen/diagnosis/build_report.json)
"""
import json, os, re, sys, glob, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = '/home/user/allprojects/tradition-ontology'
import entries_yoga, entries_gita_upa, entries_buddhist, entries_jain
import vism

ENTRIES = entries_yoga.ENTRIES + entries_gita_upa.ENTRIES + entries_buddhist.ENTRIES + entries_jain.ENTRIES
KINDS = {"affliction", "hindrance", "fetter", "passion", "guna", "mind-activity", "sheath", "vital-current", "state-of-consciousness", "obstacle", "state", "temperament"}
LENSES = {"vedic-yogic", "ascetic-buddhist", "ascetic-jain"}
GRADES = {"exact", "partial", "same-under-standpoint"}
errors, warnings = [], []

# ---------- ontology refs: keep only ids that exist ----------
known = set()
for f in ['obstacles', 'concepts', 'phenomenology', 'terms']:
    for x in json.load(open(f'{ROOT}/data/{f}.json', encoding='utf-8')):
        known.add(x['id'])
dropped_refs = collections.Counter()
for e in ENTRIES:
    keep = []
    for r in e['ontology_refs']:
        if r in known and r not in keep: keep.append(r)
        elif r not in known: dropped_refs[r] += 1
    e['ontology_refs'] = keep

# ---------- reverse equivalences ----------
by_id = {}
for e in ENTRIES:
    if e['id'] in by_id: errors.append(f"duplicate id {e['id']}")
    by_id[e['id']] = e
added_rev = 0
for e in list(ENTRIES):
    for q in e['equivalences']:
        t = by_id.get(q['id'])
        if t is None:
            errors.append(f"{e['id']}: equivalence target {q['id']} missing"); continue
        if not any(x['id'] == e['id'] for x in t['equivalences']):
            t['equivalences'].append({"id": e['id'], "grade": q['grade'], "note": q['note'], "cites": list(q['cites'])}); added_rev += 1
# grade consistency both ways
for e in ENTRIES:
    for q in e['equivalences']:
        back = [x for x in by_id[q['id']]['equivalences'] if x['id'] == e['id']]
        if back and back[0]['grade'] != q['grade']:
            errors.append(f"grade mismatch {e['id']} <-> {q['id']}: {q['grade']} vs {back[0]['grade']}")

# ---------- structural validation ----------
REQ = ["id", "name", "kind", "group", "lens", "ontology_refs", "definitions", "markers", "states", "equivalences", "paired_practices", "not_to_be_read_as", "user_facing"]
for e in ENTRIES:
    i = e['id']
    for k in REQ:
        if k not in e: errors.append(f"{i}: missing {k}")
    if not re.fullmatch(r'dx:[a-z0-9-]+', i): errors.append(f"{i}: bad id form")
    if e['kind'] not in KINDS: errors.append(f"{i}: bad kind {e['kind']}")
    if e['lens'] not in LENSES: errors.append(f"{i}: bad lens {e['lens']}")
    if not e['definitions']: errors.append(f"{i}: no definitions")
    if not e['markers']: errors.append(f"{i}: no markers")
    if not e['not_to_be_read_as'].strip(): errors.append(f"{i}: empty not_to_be_read_as")
    if e['user_facing'] is not True: errors.append(f"{i}: user_facing not true")
    for sect in ['definitions', 'markers', 'states', 'equivalences', 'paired_practices']:
        for n, it in enumerate(e[sect]):
            if not it.get('cites'): errors.append(f"{i}: {sect}[{n}] has no cites")
            for c in it.get('cites', []):
                if not re.fullmatch(r'tea:[a-z0-9-]+:[A-Za-z0-9.:/-]+', c): errors.append(f"{i}: bad cite form {c}")
    for d in e['definitions']:
        if not d['tradition'].startswith('lin:'): errors.append(f"{i}: bad tradition {d['tradition']}")
    for q in e['equivalences']:
        if q['grade'] not in GRADES: errors.append(f"{i}: bad grade {q['grade']}")
        if not q['note'].strip(): errors.append(f"{i}: equivalence to {q['id']} without note")
        if q['id'] == i: errors.append(f"{i}: self-equivalence")
    for p in e['paired_practices']:
        if not re.fullmatch(r'px:[a-z0-9-]+', p['practice']): errors.append(f"{i}: bad px id {p['practice']}")
    if len({p['practice'] for p in e['paired_practices']}) != len(e['paired_practices']): errors.append(f"{i}: duplicate px")
    for m in e['markers']:
        if not isinstance(m['cues'], list): errors.append(f"{i}: cues not a list")

# ---------- clinical / modern-psychology vocabulary scan ----------
CLIN = r"depress|anxiety|anxious|disorder|trauma|adhd|\bocd\b|ptsd|bipolar|psychiatr|psycholog|therap|clinical|neuro|symptom|syndrome|insomnia|addict|compulsi|obsessi|phobi|panic|burnout|\bstress|cognitive|dopamine|hormone|mental illness|mental health|patient|\bcure|\bheal|treatment|personality type|introvert|extrovert|self-esteem|diagnos"
ALLOW_IN_NOT = {"diagnos", "personality type"}   # allowed only inside not_to_be_read_as, as a negation
def strings(o, path=''):
    if isinstance(o, str): yield path, o
    elif isinstance(o, list):
        for n, x in enumerate(o): yield from strings(x, f'{path}[{n}]')
    elif isinstance(o, dict):
        for k, v in o.items(): yield from strings(v, f'{path}.{k}')
clin_hits = []
for e in ENTRIES:
    for p, s in strings(e):
        for m in re.finditer(CLIN, s, re.I):
            w = m.group(0).lower()
            if p == '.not_to_be_read_as' and any(w.startswith(a) for a in ALLOW_IN_NOT): continue
            clin_hits.append((e['id'], p, w, s[max(0, m.start()-40): m.end()+40]))
for h in clin_hits: errors.append(f"clinical/modern word {h}")

# ---------- citation resolution ----------
teach = {}
for f in glob.glob(f'{ROOT}/data/teachings/*.jsonl'):
    slug = os.path.basename(f)[:-6]
    for line in open(f, encoding='utf-8'):
        line = line.strip()
        if not line: continue
        t = json.loads(line)
        teach[t['id']] = (t['verification']['level'], t['location'].get('ref', ''), slug)
seg_refs = {}
for d in glob.glob(f'{ROOT}/sources_raw/prepared/*/segments.jsonl'):
    slug = d.split('/')[-2]
    seg_refs[slug] = {json.loads(l)['ref'] for l in open(d, encoding='utf-8') if l.strip()}
SEG_SLUG = {'yoga-sutra': 'yoga-sutra', 'yoga-bhasya': 'yoga-sutra', 'bhagavad-gita': 'bhagavad-gita', 'katha-upanisad': 'katha-upanisad',
            'taittiriya-upanisad': 'taittiriya-upanisad', 'mandukya-upanisad': 'mandukya-upanisad', 'mandukya-karika': 'mandukya-karika',
            'satipatthana-sutta': 'satipatthana-sutta', 'mahasatipatthana-sutta': 'mahasatipatthana-sutta', 'anapanasati-sutta': 'anapanasati-sutta',
            'dhammapada': 'dhammapada', 'tattvartha-sutra': 'tattvartha-sutra'}
def nums(r): return tuple(int(x) for x in re.findall(r'\d+', r))
def covering(slug, ref):
    """existing data ids of this slug whose (range) ref covers the cited ref"""
    out = []
    target = nums(ref)
    for tid, (lvl, r, s) in teach.items():
        if s != slug or '-' not in r: continue
        a, b = r.split('-', 1)
        na, nb = nums(a), nums(b)
        if len(nb) < len(na): nb = na[:len(na) - len(nb)] + nb
        if len(na) == len(target) and na <= target <= nb: out.append(f"{tid} ({lvl})")
    return out
vpages = vism.pages()
all_cites = collections.OrderedDict()
for e in ENTRIES:
    for sect in ['definitions', 'markers', 'states', 'equivalences', 'paired_practices']:
        for it in e[sect]:
            for c in it['cites']: all_cites.setdefault(c, set()).add(e['id'])
resolved, missing = {}, {}
for c in all_cites:
    _, slug, ref = c.split(':', 2)
    if c in teach:
        resolved[c] = teach[c][0]; continue
    # the cited ref must exist in the local source even if the teaching id does not yet
    if slug == 'visuddhimagga':
        m = re.fullmatch(r'(\d+)\.p(\d+)', ref)
        ok = bool(m) and int(m.group(2)) in vpages
        if not ok: errors.append(f"Vism cite {c}: page not in e-text")
    elif slug in SEG_SLUG:
        ok = ref in seg_refs.get(SEG_SLUG[slug], set())
        if not ok: errors.append(f"cite {c}: ref not in prepared segments of {SEG_SLUG[slug]}")
    else:
        errors.append(f"cite {c}: not in data and no local segment check"); ok = False
    missing[c] = covering(slug, ref) if slug != 'visuddhimagga' else []

# ---------- output ----------
_pos = {e['id']: n for n, e in enumerate(ENTRIES)}
ENTRIES.sort(key=lambda e: ({'vedic-yogic': 0, 'ascetic-buddhist': 1, 'ascetic-jain': 2}[e['lens']], _pos[e['id']]))
out = f'{ROOT}/layers/diagnosis.json'
with open(out, 'w', encoding='utf-8') as fh:
    fh.write(json.dumps(ENTRIES, ensure_ascii=False, indent=1) + '\n')
# re-read and re-validate the written file
back = json.load(open(out, encoding='utf-8'))
assert len(back) == len(ENTRIES) and len({e['id'] for e in back}) == len(back)

px = collections.OrderedDict()
for e in back:
    for p in e['paired_practices']: px.setdefault(p['practice'], []).append(e['id'])
report = {
    "entries": len(back),
    "by_kind": dict(collections.Counter(e['kind'] for e in back)),
    "by_lens": dict(collections.Counter(e['lens'] for e in back)),
    "equivalences_total": sum(len(e['equivalences']) for e in back), "reverse_equivalences_added": added_rev,
    "grades": dict(collections.Counter(q['grade'] for e in back for q in e['equivalences'])),
    "cites_distinct": len(all_cites), "cites_resolved_in_data": len(resolved),
    "cites_resolved_levels": dict(collections.Counter(resolved.values())),
    "cites_not_in_data": {c: {"covered_by_existing_range_ids": v, "used_by": sorted(all_cites[c])} for c, v in missing.items()},
    "px_ids": {k: sorted(set(v)) for k, v in px.items()},
    "ontology_refs_dropped_missing": dict(dropped_refs),
    "entries_without_ontology_refs": [e['id'] for e in back if not e['ontology_refs']],
    "empty_cue_markers": [e['id'] for e in back for m in e['markers'] if not m['cues']],
    "errors": errors, "warnings": warnings,
}
json.dump(report, open(f'{HERE}/build_report.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps({k: report[k] for k in ['entries', 'by_kind', 'by_lens', 'equivalences_total', 'reverse_equivalences_added', 'grades', 'cites_distinct', 'cites_resolved_in_data', 'cites_resolved_levels']}, ensure_ascii=False))
print('not in data:', len(missing), '| px ids:', len(px), '| dropped refs:', len(dropped_refs), '| errors:', len(errors))
for x in errors[:60]: print('ERR', x)

# The P3 cue expansion (add_cues.py) must survive any rebuild of diagnosis.json.
import subprocess as _sp, sys as _sys, os as _os
_ac = _os.path.join(HERE, "add_cues.py")
if _os.path.exists(_ac):
    _sp.run([_sys.executable, _ac], check=True)
