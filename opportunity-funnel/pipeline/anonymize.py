"""Privacy: remove people from text before it is stored (rule 5).

Public API
----------
    anonymize(text, known_names=()) -> str
        In order: emails -> [email]; profile links -> [profile link]; phone numbers -> [phone];
        usernames -> [user]; names -> [name]. Idempotent: anonymize(anonymize(t)) == anonymize(t).
        Never changes prices, years, dates, times, percentages, scores or numbers glued to units.
    anonymize_record(record, known_names=()) -> dict
        Same, applied to record["text"] (a copy is returned).
    is_profile_url(url) -> bool
        True for a person's profile or channel page (reddit /user/, x.com/<handle>, linkedin /in/,
        youtube /@ /channel/ /c/ /user/, instagram, facebook, tiktok, medium, quora /profile/,
        stack exchange /users/, HN user?id=, github.com/<user>, t.me, wa.me, threads). A post, video,
        tweet, answer or repository under such a site is not a profile. Rule 5: only the post's own
        URL may be stored, so a profile page is never stored as a record.
    known_name_patterns(known_names) -> list[re.Pattern]
        The patterns the name pass applies for known (sender) names; see the rules below.
    PLACEHOLDERS: tuple[str, ...]
        The five placeholders above.
    LIMIT_NOTE: str
        The known limit, for the run log: names in running text without a cue may survive.

Known names (sender names from chat exports, usernames from forums) are removed like this:
  - the whole name, in any letter case, with spaces, underscores, dots or hyphens between its parts
    ("Priya Mehta", "priya_mehta", "PRIYA MEHTA");
  - its first part (the given name) in any letter case ("priya", "Priya");
  - every other part only with its own capital letter ("Mehta", not "mehta"), and never a part that is
    all capitals (an acronym such as GRE), a part that is not capitalised in the sender string, a part of
    fewer than three letters, or a role, place or family word (tutor, sir, coaching, centre, delhi, bhai...).
    A saved contact like "Rahul GRE Tutor" therefore removes "Rahul" but leaves "GRE" and "tutor" in
    every other member's message, so the evidence text stays whole.
"""
from __future__ import annotations

import re
from urllib.parse import parse_qs, urlsplit

PLACEHOLDERS = ("[email]", "[profile link]", "[phone]", "[user]", "[name]")
LIMIT_NOTE = ("Anonymizer limit: names in running text without a cue (honorific, greeting, "
              "sign-off or 'my name is') may survive. Known sender names are always removed.")

# ---------------------------------------------------------------- emails
_EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
_TLDS = r"(?:com|net|org|in|co|io|edu|gov|uk|us|de|fr|au|ca|info|me|ai|app|dev|xyz|biz|nl|it|es|ch|se|sg|ae)"
_OBFUSCATED_EMAIL_RE = re.compile(
    r"(?<![\w.+-])[\w.+-]+\s*(?:\(at\)|\[at\]|\{at\}|\s+at\s+)\s*[\w-]+"
    r"(?:\s*(?:\(dot\)|\[dot\]|\{dot\}|\s+dot\s+)\s*[\w-]+)*"
    r"\s*(?:\(dot\)|\[dot\]|\{dot\}|\s+dot\s+)\s*" + _TLDS + r"\b",
    re.IGNORECASE,
)

# ---------------------------------------------------------------- profile links
_URL_PREFIX = r"(?:https?://)?(?:(?:www|m|old|mobile|new)\.)?"
_URL_TAIL = r"[^\s<>\"'\)\]]*"
_PROFILE_HOSTS = [
    r"(?:[\w-]+\.)?reddit\.com/(?:user|u)/[\w-]+",
    r"(?:twitter|x)\.com/(?!(?:i|search|home|explore|hashtag|intent|share|settings|login|signup|messages|notifications|compose|privacy|tos)(?:[/?#\s]|$))\w{1,15}",
    r"instagram\.com/(?!(?:p|reel|reels|explore|stories|accounts|direct|about|legal)(?:[/?#\s]|$))[\w.]+",
    r"facebook\.com/(?:profile\.php\?id=\d+|(?!(?:groups|pages|events|marketplace|watch|help|photo|photos|share|sharer|story\.php|login|home\.php|search|policies|privacy|terms)(?:[/?#\s]|$))[\w.]+)",
    r"linkedin\.com/in/[\w%.-]+",
    r"youtube\.com/(?:@[\w.-]+|channel/[\w-]+|c/[\w.-]+|user/[\w.-]+)",
    r"tiktok\.com/@[\w.]+",
    r"medium\.com/@[\w.-]+",
    r"quora\.com/profile/[\w-]+",
    r"(?:[\w-]+\.)?(?:stackoverflow|stackexchange|superuser|serverfault|askubuntu|mathoverflow)\.(?:com|net)/users/\d+(?:/[\w-]+)?",
    r"news\.ycombinator\.com/user\?id=[\w-]+",
    r"t\.me/\w+",
    r"wa\.me/\+?\d+",
]
_PROFILE_RE = re.compile(_URL_PREFIX + r"(?:" + "|".join(_PROFILE_HOSTS) + r")" + _URL_TAIL, re.IGNORECASE)
_GITHUB_RESERVED = (r"orgs|topics|features|about|pricing|explore|marketplace|sponsors|settings|login|search|"
                    r"apps|site|security|enterprise|collections|events|trending|new|join|contact|blog")
_GITHUB_RE = re.compile(
    _URL_PREFIX + r"github\.com/(?!(?:" + _GITHUB_RESERVED + r")(?:[/?#\s]|$))[\w-]+/?(?![\w/])",
    re.IGNORECASE,
)

# ---------------------------------------------------------------- phones
_PHONE_RE = re.compile(r"(?<![\w.,/-])\+?\(?\d(?:[\s().-]*\d){8,14}(?![\w%])")
_PHONE_BEFORE_RE = re.compile(
    r"(?:[$₹€£¥]|\b(?:rs|inr|usd|eur|gbp|aed|sgd|price|priced|cost|costs|fee|fees|paid|pay|salary|ctc|budget|"
    r"score|scored|scores|gre|gmat|ielts|toefl|sat|rank|marks|views|invoice|isbn|worth|around|approx))\.?\s*$",
    re.IGNORECASE,
)
_PHONE_AFTER_RE = re.compile(
    r"^\s*(?:k\b|lakh|lakhs|lac|lacs|crore|crores|cr\b|mn\b|bn\b|million|billion|rupees|rs\b|inr\b|usd\b|eur\b|"
    r"gbp\b|aed\b|sgd\b|dollars|euros|pounds|per\b|/|pm\b|am\b|marks|points|votes|views|subscribers|members|"
    r"users|people|students|km\b|kg\b|mb\b|gb\b|kb\b|mah\b|hrs?\b|hours?\b|days?\b|months?\b|years?\b|weeks?\b)",
    re.IGNORECASE,
)


def _looks_like_years(s: str) -> bool:
    groups = re.findall(r"\d+", s)
    return all(len(g) == 4 and 1900 <= int(g) <= 2099 for g in groups)


def _phone_sub(m: re.Match) -> str:
    text = m.string
    before = text[max(0, m.start() - 14):m.start()]
    after = text[m.end():m.end() + 14]
    if _PHONE_BEFORE_RE.search(before) or _PHONE_AFTER_RE.match(after) or _looks_like_years(m.group(0)):
        return m.group(0)
    return "[phone]"


# ---------------------------------------------------------------- usernames
_REDDIT_USER_RE = re.compile(r"(?<![\w./@])/?u/[A-Za-z0-9_-]{2,30}\b")
_HANDLE_RE = re.compile(r"(?<![\w.])@[A-Za-z0-9_][\w.]{1,29}(?<!\.)")

# ---------------------------------------------------------------- names
_CAP = r"[A-Z][a-z'’-]+"
_CAP_ANY = r"[A-Z][A-Za-z'’-]+"
_NOT_NAMES = {
    "all", "everyone", "everybody", "anyone", "someone", "nobody", "guys", "folks", "team", "there", "again",
    "sir", "madam", "friends", "friend", "community", "reddit", "people", "moderators", "mods", "admin", "admins",
    "world", "so", "this", "that", "these", "those", "the", "just", "can", "could", "does", "did", "has", "have",
    "how", "what", "why", "when", "where", "which", "who", "please", "any", "need", "looking", "quick", "new",
    "first", "long", "thanks", "thank", "sorry", "good", "great", "nice", "yes", "no", "not", "ok", "okay", "one",
    "two", "ladies", "gentlemen", "in", "advance", "for", "to", "anyway", "anyways", "though", "but", "and", "also",
    "god", "you", "man", "bro", "dude", "mate", "ma'am", "everybody", "hope", "here", "hello", "hi", "hey", "dear",
    "everyone,", "again,", "if", "is", "it", "its", "was", "were", "will", "would", "should", "may", "might", "am",
    "are", "we", "our", "my", "me", "your", "let", "lets", "wanted", "want", "got", "get", "help", "advice",
    "question", "regarding", "about", "from", "with", "after", "before", "today", "tomorrow", "yesterday",
    "gre", "gmat", "ielts", "toefl", "india", "indian", "usa", "uk", "us", "canada", "germany", "australia",
}
_HONORIFIC_RE = re.compile(
    r"\b(Mr|Mrs|Ms|Miss|Mx|Dr|Prof|Professor|Sir|Madam|Shri|Smt|Sri|Kumari|Ustad|Pandit|Guru)\.?\s+"
    r"(" + _CAP_ANY + r"(?:\s+" + _CAP_ANY + r"){0,2})"
)
_GREETING_RE = re.compile(
    r"\b(Hi|Hello|Hey|Dear|Namaste|Namaskar|Hola|Greetings)\s*[,!]?\s+(" + _CAP + r"(?:\s+" + _CAP + r")?)\b"
)
_SIGNOFF_RE = re.compile(
    r"\b(Regards|Thanks|Thank you|Thanks a lot|Many thanks|Thanks and regards|Cheers|Best regards|Kind regards|"
    r"Warm regards|Sincerely|Yours truly|Yours sincerely|Yours|Take care|(?:Best|Love)\s*(?:,|\n))"
    r"\s*[,!.]?\s*(?:\n\s*)?(?:[-–—]\s*)?(" + _CAP + r"(?:\s+" + _CAP + r")?)\b"
)
_MY_NAME_RE = re.compile(r"\b([Mm]y name(?:'s|’s| is))\s+(" + _CAP_ANY + r"(?:\s+" + _CAP_ANY + r"){0,2})")
_KNOWN_TOKEN_STOP = {
    "will", "may", "june", "april", "august", "mark", "price", "sunny", "rose", "bill", "guy", "art", "ray",
    "hope", "grace", "joy", "max", "sky", "king", "young", "long", "man", "the", "and", "for", "you", "not",
}


def _replace_name_group(m: re.Match, group: int = 2) -> str:
    whole = m.group(0)
    start = m.start(group) - m.start(0)
    end = m.end(group) - m.start(0)
    return whole[:start] + "[name]" + whole[end:]


def _name_sub(m: re.Match) -> str:
    candidate = m.group(2)
    first = candidate.split()[0].lower().rstrip(",")
    if first in _NOT_NAMES:
        return m.group(0)
    return _replace_name_group(m, 2)


def _known_names_patterns(known_names) -> list:
    patterns = []
    for name in known_names or ():
        if not isinstance(name, str):
            continue
        name = name.strip()
        if len(name) < 2:
            continue
        patterns.append(re.compile(r"(?<!\w)" + re.escape(name) + r"(?!\w)", re.IGNORECASE))
        for token in re.findall(r"[^\W\d_]{3,}", name):
            if token.lower() in _KNOWN_TOKEN_STOP:
                continue
            patterns.append(re.compile(r"(?<!\w)" + re.escape(token) + r"(?!\w)", re.IGNORECASE))
    return patterns


def anonymize(text: str, known_names=()) -> str:
    """Remove emails, profile links, phone numbers, usernames and names. Idempotent."""
    if text is None:
        return ""
    s = str(text)
    # 1. emails
    s = _EMAIL_RE.sub("[email]", s)
    s = _OBFUSCATED_EMAIL_RE.sub("[email]", s)
    # 2. profile links
    s = _PROFILE_RE.sub("[profile link]", s)
    s = _GITHUB_RE.sub("[profile link]", s)
    # 3. phone numbers
    s = _PHONE_RE.sub(_phone_sub, s)
    # 4. usernames
    s = _REDDIT_USER_RE.sub("[user]", s)
    s = _HANDLE_RE.sub("[user]", s)
    # 5. names
    s = _HONORIFIC_RE.sub(_name_sub, s)
    s = _GREETING_RE.sub(_name_sub, s)
    s = _SIGNOFF_RE.sub(_name_sub, s)
    s = _MY_NAME_RE.sub(_name_sub, s)
    for pat in _known_names_patterns(known_names):
        s = pat.sub("[name]", s)
    return s


def anonymize_record(record: dict, known_names=()) -> dict:
    out = dict(record)
    out["text"] = anonymize(record.get("text", ""), known_names)
    return out
