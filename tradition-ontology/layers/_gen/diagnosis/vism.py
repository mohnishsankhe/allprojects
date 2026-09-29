"""Visuddhimagga (PTS ed., GRETIL Devanagari annotated e-text) -> IAST, with PTS page tracking.
Usage: python3 vism.py find <iast-regex> [context_chars]  -> page + snippet
       python3 vism.py page <n> [maxchars]                -> IAST text of PTS page n
"""
import re, sys, functools
ROOT = '/home/user/allprojects/tradition-ontology'
F = ROOT + '/sources_raw/raw_etexts/mixed/gretil_devanAgarI/2_pali/4_comm/buddhaghosa_visuddhimagga_annotated_version.md'
V = {'अ':'a','आ':'ā','इ':'i','ई':'ī','उ':'u','ऊ':'ū','ए':'e','ओ':'o','ऋ':'ṛ','ऐ':'ai','औ':'au'}
M = {'ा':'ā','ि':'i','ी':'ī','ु':'u','ू':'ū','े':'e','ो':'o','ृ':'ṛ','ै':'ai','ौ':'au'}
C = {'क':'k','ख':'kh','ग':'g','घ':'gh','ङ':'ṅ','च':'c','छ':'ch','ज':'j','झ':'jh','ञ':'ñ','ट':'ṭ','ठ':'ṭh','ड':'ḍ','ढ':'ḍh','ण':'ṇ',
     'त':'t','थ':'th','द':'d','ध':'dh','न':'n','प':'p','फ':'ph','ब':'b','भ':'bh','म':'m','य':'y','र':'r','ल':'l','व':'v','स':'s','ह':'h','ळ':'ḷ','ऌ':'ḷ','श':'ś','ष':'ṣ'}
D = {'०':'0','१':'1','२':'2','३':'3','४':'4','५':'5','६':'6','७':'7','८':'8','९':'9'}
def tr(s):
    out = []; i = 0; n = len(s)
    while i < n:
        ch = s[i]
        if ch in C:
            out.append(C[ch]); nx = s[i+1] if i+1 < n else ''
            if nx == '्': i += 2; continue
            if nx in M: out.append(M[nx]); i += 2; continue
            out.append('a'); i += 1; continue
        if ch in V: out.append(V[ch])
        elif ch == 'ं': out.append('ṃ')
        elif ch in D: out.append(D[ch])
        elif ch in M: out.append(M[ch])
        elif ch == '्': pass
        else: out.append(ch)
        i += 1
    return ''.join(out)
@functools.lru_cache(None)
def pages():
    txt = open(F, encoding='utf-8').read()
    parts = re.split(r'\[पगे ([०-९]+)\]', txt)
    res = {0: tr(parts[0])}
    for k in range(1, len(parts), 2):
        res[int(tr(parts[k]))] = tr(parts[k+1])
    return res
def clean(t):
    t = re.sub(r'-\s*\n\s*', '', t)      # join hyphenated line breaks
    t = re.sub(r'\s*\n\s*', ' ', t)
    return re.sub(r'\s+', ' ', t)
if __name__ == '__main__':
    P = pages()
    if sys.argv[1] == 'page':
        print(clean(P[int(sys.argv[2])])[:int(sys.argv[3]) if len(sys.argv) > 3 else 5000])
    elif sys.argv[1] == 'find':
        rx = re.compile(sys.argv[2]); ctx = int(sys.argv[3]) if len(sys.argv) > 3 else 150
        for p, t in sorted(P.items()):
            ct = clean(t)
            for m in rx.finditer(ct):
                print(p, '::', ct[max(0, m.start()-ctx): m.end()+ctx]); print()
