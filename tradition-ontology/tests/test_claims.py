"""The forbidden-claims scanner: deterministic, applied to every output field."""
import pytest

from insight import claims

BAD = [
    ("Meditation will cure your anxiety.", "health_cure"),
    ("This practice reduces stress and improves sleep.", "health_cure"),
    ("Studies show the brain changes with practice.", "health_cure"),
    ("This is a diagnosis of depression.", "diagnosis"),
    ("Your kundali shows a hard transit of Saturn.", "prediction"),
    ("Your horoscope says wealth is coming.", "prediction"),
    ("You will find peace in the next month.", "prediction"),
]
GOOD = [
    "The Gita advises bringing the mind back each time it wanders (BhG 6.26).",
    "You wrote that this happens most nights.",
    "This reading is not a diagnosis, not medical or psychological advice, and it does not predict anything.",
]


@pytest.mark.parametrize("text,cat", BAD)
def test_scan_catches(text, cat):
    hits = claims.scan(text)
    assert hits and cat in {h["category"] for h in hits}


@pytest.mark.parametrize("text", GOOD)
def test_scan_lets_plain_text_through(text):
    assert claims.scan(text) == []


def test_standing_notice_is_exempt():
    from insight.report import STANDING_NOTICE
    assert claims.scan(STANDING_NOTICE) == []


def test_strip_sentences_removes_only_the_bad_sentence():
    out = claims.strip_sentences("The text describes attachment. Meditation will cure your anxiety. Bring the mind back.")
    assert "cure" not in out and "attachment" in out and "Bring the mind back" in out


def test_scan_fields_walks_nested_objects_and_reports_paths():
    hits = claims.scan_fields({"a": [{"why": "This will cure your anxiety."}], "b": "fine"})
    assert len(hits) == 1 and hits[0]["path"] == "$.a[0].why"


def test_scan_fields_skips_verbatim_fields_only():
    obj = {"original": "It will cure your anxiety", "quote": "cure your anxiety", "evidence": ["cure your anxiety"],
           "person_words": "cure your anxiety", "text": "fine"}
    assert claims.scan_fields(obj) == []
    assert claims.scan_fields({"text": "It will cure your anxiety"})
    assert claims.scan_fields({"original": "x", "why": "It will cure your anxiety"})


def test_case_insensitive():
    assert claims.scan("MEDITATION WILL CURE YOUR ANXIETY")


def test_empty_and_none():
    assert claims.scan("") == [] and claims.scan(None) == []
    assert claims.strip_sentences("") == ""
