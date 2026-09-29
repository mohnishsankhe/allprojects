"""Build and validate layers/practices.json from entries.py. Run: python3 layers/_gen/practices/build.py
Writes layers/practices.json and layers/_gen/practices/build_report.json. Exits non-zero on any error."""
import collections, glob, json, os, re, sys
ROOT = '/home/user/allprojects/tradition-ontology'
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, ROOT); sys.path.insert(0, f'{ROOT}/layers/_gen/diagnosis')
from entries import ENTRIES
import vism
from insight import ontology as O

errors, warnings = [], []
TIERS = {'gentle', 'needs-teacher', 'never-recommend'}
STAGES = {'beginner', 'intermediate', 'advanced', 'all'}
LENSES = {'vedic-yogic', 'ascetic-buddhist', 'ascetic-jain'}
REQ = ["id", "name", "lens", "ontology_refs", "tradition", "summary", "steps", "targets", "stage", "duration", "warnings",
       "safety_tier", "tier_reason", "cites", "user_facing"]

# ---------- targets from the diagnosis pairings ----------
diag = json.load(open(f'{ROOT}/layers/diagnosis.json', encoding='utf-8'))
pairs = collections.OrderedDict()
for e in diag:
    for p in e.get('paired_practices', []):
        pairs.setdefault(p['practice'], [])
        if e['id'] not in pairs[p['practice']]: pairs[p['practice']].append(e['id'])
ids = [e['id'] for e in ENTRIES]
if len(ids) != len(set(ids)): errors.append(f"duplicate ids: {[i for i, n in collections.Counter(ids).items() if n > 1]}")
missing_px = sorted(set(pairs) - set(ids)); extra_px = sorted(set(ids) - set(pairs))
if missing_px: errors.append(f"px ids in diagnosis.json but not built: {missing_px}")
if extra_px: errors.append(f"px ids built but not referenced in diagnosis.json: {extra_px}")
for e in ENTRIES:
    e['targets'] = list(pairs.get(e['id'], []))

# ---------- reference data ----------
prc = {o['id']: o for o in json.load(open(f'{ROOT}/data/practices.json', encoding='utf-8'))}
lins = {o['id'] for o in json.load(open(f'{ROOT}/data/lineages.json', encoding='utf-8'))}
teach = {}
for f in glob.glob(f'{ROOT}/data/teachings/*.jsonl'):
    for line in open(f, encoding='utf-8'):
        if line.strip():
            t = json.loads(line); teach[t['id']] = t['verification']['level']
seg_refs = {}
for d in glob.glob(f'{ROOT}/sources_raw/prepared/*/segments.jsonl'):
    seg_refs[d.split('/')[-2]] = {json.loads(l)['ref'] for l in open(d, encoding='utf-8') if l.strip()}
SEG_SLUG = {'yoga-sutra': 'yoga-sutra', 'yoga-bhasya': 'yoga-sutra', 'bhagavad-gita': 'bhagavad-gita', 'katha-upanisad': 'katha-upanisad',
            'taittiriya-upanisad': 'taittiriya-upanisad', 'mandukya-upanisad': 'mandukya-upanisad', 'mandukya-karika': 'mandukya-karika',
            'satipatthana-sutta': 'satipatthana-sutta', 'mahasatipatthana-sutta': 'mahasatipatthana-sutta', 'anapanasati-sutta': 'anapanasati-sutta',
            'dhammapada': 'dhammapada', 'tattvartha-sutra': 'tattvartha-sutra'}
vpages = vism.pages()

def cite_status(c):
    """'data:<level>' if the id is in data; 'local' if not in data but the ref exists in the local source; None if unresolved."""
    if c in teach: return f"data:{teach[c]}"
    _, slug, ref = c.split(':', 2)
    if slug == 'visuddhimagga':
        m = re.fullmatch(r'(\d+)\.p(\d+)', ref)
        return 'local' if m and int(m.group(2)) in vpages else None
    if slug in SEG_SLUG:
        return 'local' if ref in seg_refs.get(SEG_SLUG[slug], set()) else None
    return None

# ---------- per-entry checks ----------
CLIN = re.compile(r"\b(cure[sd]?|curing|heal\w*|treat\w*|therap\w*|symptom\w*|anxiety|anxious|depress\w*|stress[- ]relief|lowers?|reduces?|"
                  r"diagnos\w*|disorder\w*|patient\w*|clinical\w*|medical\w*|health\w*|mental illness|wellness)\b", re.I)
DANGER_IN_STEPS = re.compile(r"\b(hold (the|your) breath|retention|retain|kumbhaka|fast(ing)?|abstain from food|corpse|charnel|death|dead|"
                             r"repulsive\w*|celiba\w*|inversion|headstand|mercury|cut)\b", re.I)
def strings(o, path=''):
    if isinstance(o, str): yield path, o
    elif isinstance(o, dict):
        for k, v in o.items(): yield from strings(v, f'{path}.{k}')
    elif isinstance(o, list):
        for i, v in enumerate(o): yield from strings(v, f'{path}[{i}]')

all_cites = collections.OrderedDict()
for e in ENTRIES:
    i = e['id']
    if list(e.keys()) != REQ: errors.append(f"{i}: keys {list(e.keys())} != schema order")
    if not re.fullmatch(r'px:[a-z0-9-]+', i): errors.append(f"{i}: bad id")
    if e['lens'] not in LENSES: errors.append(f"{i}: bad lens")
    if e['tradition'] not in lins: errors.append(f"{i}: tradition {e['tradition']} not in data/lineages.json")
    if e['stage'] not in STAGES: errors.append(f"{i}: bad stage {e['stage']}")
    if e['safety_tier'] not in TIERS: errors.append(f"{i}: bad tier {e['safety_tier']}")
    if not e['targets']: errors.append(f"{i}: no targets")
    if not e['summary'].strip() or not e['tier_reason'].strip(): errors.append(f"{i}: empty summary or tier_reason")
    if not e['cites']: errors.append(f"{i}: no cites")
    for r in e['ontology_refs']:
        if r not in prc: errors.append(f"{i}: ontology_ref {r} not in data/practices.json")
    for w in e['warnings']:
        if not w['text'].strip() or not w['cites']: errors.append(f"{i}: warning without text or cites")
    for c in e['cites'] + [c for w in e['warnings'] for c in w['cites']]:
        all_cites.setdefault(c, set()).add(i)
    d = e['duration']
    if set(d) != {"minutes_per_session", "sessions_per_day", "basis"}: errors.append(f"{i}: duration keys")
    if e['safety_tier'] == 'gentle':
        if not (3 <= len(e['steps']) <= 6): errors.append(f"{i}: gentle needs 3-6 steps, has {len(e['steps'])}")
        if not (isinstance(d['minutes_per_session'], list) and len(d['minutes_per_session']) == 2 and d['sessions_per_day']):
            errors.append(f"{i}: gentle needs a duration")
        if not e['warnings']: errors.append(f"{i}: gentle without a cited warning")
        for s in e['steps']:
            m = DANGER_IN_STEPS.search(s)
            if m: errors.append(f"{i}: gentle step contains '{m.group(0)}': {s}")
    else:
        if e['steps']: errors.append(f"{i}: non-gentle tier must have steps []")
    for p, s in strings(e):
        m = CLIN.search(s)
        if m: errors.append(f"{i}{p}: clinical/health word '{m.group(0)}'")

# ---------- citation resolution ----------
cite_levels = {}
for c, users in all_cites.items():
    st = cite_status(c)
    if st is None: errors.append(f"cite {c} (used by {sorted(users)}) resolves neither in data nor in the local source")
    cite_levels[c] = st

# user_facing (SCHEMA): an entry that cites any teaching that is not sourced/text-verified (after the app's mechanical
# range-covering resolution in insight/ontology.py) stays in the file with user_facing false.
uf_detail = {}
for e in ENTRIES:
    cs = e['cites'] + [c for w in e['warnings'] for c in w['cites']]
    bad = sorted({c for c in cs if not O.citable(c)})
    e['user_facing'] = not bad
    uf_detail[e['id']] = bad
    if e['safety_tier'] == 'gentle' and not any(O.citable(c) for w in e['warnings'] for c in w['cites']):
        warnings.append(f"{e['id']}: gentle, but no warning cite is citable yet (the app would drop every warning); user_facing is false")

# ---------- write ----------
out = f'{ROOT}/layers/practices.json'
with open(out, 'w', encoding='utf-8') as fh:
    fh.write(json.dumps(ENTRIES, ensure_ascii=False, indent=1) + '\n')
back = json.load(open(out, encoding='utf-8'))
assert [e['id'] for e in back] == ids

# the app's own loader, run on the written file
O.reset_caches()
app_all = O.practices(); app_gentle = O.gentle_practices()

by_tier = collections.defaultdict(list)
for e in back: by_tier[e['safety_tier']].append(e['id'])
refs_lvl = {r: {"level": prc[r]['verification']['level'], "restricted": prc[r].get('restricted')}
            for e in back for r in e['ontology_refs'] if r in prc}
report = {
    "entries": len(back), "px_in_diagnosis": len(pairs), "missing_px": missing_px, "extra_px": extra_px,
    "by_tier": {k: len(v) for k, v in by_tier.items()}, "tiers": dict(by_tier),
    "by_lens": dict(collections.Counter(e['lens'] for e in back)),
    "by_stage": dict(collections.Counter(e['stage'] for e in back)),
    "user_facing_true": [e['id'] for e in back if e['user_facing']],
    "user_facing_false": {k: v for k, v in uf_detail.items() if v},
    "gentle_user_facing": [e['id'] for e in back if e['safety_tier'] == 'gentle' and e['user_facing']],
    "app_loader_practices": len(app_all), "app_loader_gentle": sorted(app_gentle),
    "cites_distinct": len(all_cites),
    "cite_status_counts": dict(collections.Counter(v for v in cite_levels.values())),
    "cites_not_in_data": sorted(c for c, v in cite_levels.items() if v == 'local'),
    "ontology_refs": refs_lvl,
    "ontology_refs_levels": dict(collections.Counter(v['level'] for v in refs_lvl.values())),
    "ontology_refs_restricted": sorted(r for r, v in refs_lvl.items() if v['restricted']),
    "entries_without_ontology_refs": [e['id'] for e in back if not e['ontology_refs']],
    "errors": errors, "warnings": warnings,
}
json.dump(report, open(f'{HERE}/build_report.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps({k: report[k] for k in ['entries', 'px_in_diagnosis', 'by_tier', 'by_lens', 'cites_distinct', 'cite_status_counts',
                                          'ontology_refs_levels', 'app_loader_practices']}, ensure_ascii=False))
print('gentle:', by_tier['gentle'])
print('gentle user_facing:', report['gentle_user_facing'])
print('errors:', len(errors), '| warnings:', len(warnings))
for x in errors: print('ERR', x)
for x in warnings: print('WARN', x)
sys.exit(1 if errors else 0)
