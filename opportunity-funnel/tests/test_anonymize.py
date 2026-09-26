import pytest

from anonymize import LIMIT_NOTE, PLACEHOLDERS, anonymize

UNTOUCHED = [
    "$1,200", "Rs 15,000", "₹1,50,000", "INR 45000", "€99.99", "40k", "2 lakh", "in 2024", "2019 2020 2021",
    "2024-09-26", "26/09/2024", "at 10:30", "99.5%", "GRE 320", "IELTS 7.5", "Q170 V160", "scored 320 in 2024",
    "Rs 15000-20000", "15000-20000 per month", "10000000 rupees", "1234567890mAh", "50% off", "3.5 GPA",
]
PHONES = ["+91 98765 43210", "9876543210", "(555) 123-4567", "555-123-4567", "+44 7700 900123", "555.123.4567"]


@pytest.mark.parametrize("sample", UNTOUCHED)
def test_prices_years_dates_scores_untouched(sample):
    text = f"I paid {sample} for it"
    assert anonymize(text) == text


@pytest.mark.parametrize("phone", PHONES)
def test_phone_numbers_caught(phone):
    out = anonymize(f"call me on {phone} today")
    assert out == "call me on [phone] today"
    assert not any(ch.isdigit() for ch in out)


def test_emails_plain_and_obfuscated():
    assert anonymize("mail rahul.sharma+x@example.co.in now") == "mail [email] now"
    assert anonymize("write to name at gmail dot com please") == "write to [email] please"
    assert anonymize("x (at) y (dot) org") == "[email]"


@pytest.mark.parametrize("link", [
    "https://www.reddit.com/user/someone123/", "reddit.com/u/abc", "old.reddit.com/user/abc/comments",
    "twitter.com/elonmusk", "https://x.com/jack/status/123", "https://www.instagram.com/some.one/",
    "https://www.facebook.com/profile.php?id=100001", "facebook.com/some.person", "https://www.linkedin.com/in/rahul-sharma-123/",
    "https://youtube.com/@mrbeast", "https://www.youtube.com/channel/UCabc123", "youtube.com/c/somebody", "youtube.com/user/somebody",
    "https://www.tiktok.com/@someone", "https://medium.com/@someone", "https://www.quora.com/profile/Some-One",
    "https://stackoverflow.com/users/12345/rahul", "https://math.stackexchange.com/users/999", "https://news.ycombinator.com/user?id=pg",
    "https://github.com/damien5314", "github.com/someone/", "https://t.me/rahul123", "https://wa.me/919876543210",
])
def test_profile_links(link):
    out = anonymize(f"see {link} here")
    assert out == "see [profile link] here", out


def test_non_profile_urls_survive():
    keep = ["https://www.reddit.com/r/GRE/comments/abc/title/", "https://github.com/damien5314/RxReddit",
            "https://x.com/i/flow/login", "https://www.youtube.com/watch?v=abc123", "https://facebook.com/groups/gre"]
    for url in keep:
        assert anonymize(f"see {url} here") == f"see {url} here"


def test_usernames():
    assert anonymize("thanks u/bob and /u/xyz_1 and @rahul_s") == "thanks [user] and [user] and [user]"
    assert anonymize("meet @ 5pm") == "meet @ 5pm"


def test_names_with_cues():
    text = "Hi Rahul, my name is Priya Sharma. Regards, Amit. Dr. Shah said Mr Kumar is fine."
    assert anonymize(text) == "Hi [name], my name is [name]. Regards, [name]. Dr. [name] said Mr [name] is fine."
    assert anonymize("Best,\nRahul") == "Best,\n[name]"
    assert anonymize("Thanks Rahul") == "Thanks [name]"


def test_greetings_to_groups_and_titles_survive():
    for text in ["Hello Everyone need help", "Thanks In Advance", "Best GRE Prep Courses in 2026 | Compared & Reviewed",
                 "Hi All, GRE coaching worth it?", "Dear Sir"]:
        assert anonymize(text) == text


def test_known_names_always_removed():
    out = anonymize("Rahul Sharma: hello rahul, ask SHARMA about it. Will you come?", known_names=["Rahul Sharma", "Will Smith"])
    assert out == "[name]: hello [name], ask [name] about it. Will you come?"


@pytest.mark.parametrize("text", [
    "Hi Rahul, call +91 98765 43210 or mail name at gmail dot com; see reddit.com/u/abc and @handle. Regards, Amit",
    "https://github.com/someone https://wa.me/919876543210 u/bob",
    "Dr. Shah paid $1,200 in 2024 for GRE 320. My name is Priya Sharma.",
])
def test_idempotent(text):
    once = anonymize(text)
    assert anonymize(once) == once
    for p in PLACEHOLDERS:
        if p in once:
            assert anonymize(once).count(p) == once.count(p)


def test_placeholders_and_limit_note():
    assert PLACEHOLDERS == ("[email]", "[profile link]", "[phone]", "[user]", "[name]")
    assert "cue" in LIMIT_NOTE
