import pytest

from anonymize import LIMIT_NOTE, PLACEHOLDERS, anonymize, is_profile_url

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


# --------------------------------------------------------------------------- dates with times, versions, IPs, @-times
DATED_TIMES = [
    "Posted 2024-12-05 18:30 by a member", "exam on 2024-11-30 09:00, results 2024-12-15 10:30:45",
    "26-09-2026 10:30 - fee paid", "12.05.2024 10:30 slot", "05/12/2024 18:30 posted", "2024-12-05 18:30:00",
    "build 10.0.19041.1234 crashed", "ip 192.168.1.100 is down", "version 1.2.3.4567 broke it",
    "meet @2pm or @10:30 tomorrow", "join @ 5pm sharp", "Posted 2024-12-05 18:30 my GRE coaching refund story",
]


@pytest.mark.parametrize("text", DATED_TIMES)
def test_dates_with_times_versions_ips_and_at_times_untouched(text):
    """The README promise: the anonymizer never changes dates, times, prices or scores. A date glued to an
    hour is not a phone number; @2pm is not a handle."""
    assert anonymize(text) == text


def test_phones_next_to_times_are_still_caught():
    assert anonymize("call +91 98765 43210 after 18:30") == "call [phone] after 18:30"
    assert anonymize("ping @rahul_s at 10:30") == "ping [user] at 10:30"
    assert anonymize("ring 9876543210 tomorrow at 2pm") == "ring [phone] tomorrow at 2pm"


# --------------------------------------------------------------------------- known names: roles and acronyms survive
def test_known_name_parts_that_are_roles_acronyms_or_lowercase_survive():
    """Saved contact names carry descriptors ("Rahul GRE Tutor"). Only the person goes: the given name in any
    case, the other capitalised parts, and the whole name; never GRE, tutor, coaching, centre or a word that
    happens to be a first name ("grant")."""
    known = ("Rahul GRE Tutor", "Priya Mehta", "Amit Sir Coaching", "Neha Delhi Centre", "Grant Lee", "sam lowercase")
    assert anonymize("GRE prep is expensive, my tutor charged 40k", known_names=known) == "GRE prep is expensive, my tutor charged 40k"
    assert anonymize("my GRE tutor was worse, I paid 50k and got 300", known_names=known) == "my GRE tutor was worse, I paid 50k and got 300"
    assert anonymize("the coaching centre in Delhi said sir is busy", known_names=known) == "the coaching centre in Delhi said sir is busy"
    assert anonymize("the scholarship grant covers fees", known_names=known) == "the scholarship grant covers fees"
    assert anonymize("Rahul GRE Tutor: ask rahul or RAHUL; Priya Mehta, priya_mehta, MEHTA and Mehta", known_names=known) == \
        "[name]: ask [name] or [name]; [name], [name], [name] and [name]"
    assert anonymize("Amit said the Delhi centre is fine; Neha Delhi Centre agreed; Grant Lee; Lee; grant", known_names=known) == \
        "[name] said the Delhi centre is fine; [name] agreed; [name]; [name]; grant"
    # a part not capitalised in the contact string is never removed on its own (it could be any word); the
    # whole name still is, in any letter case
    assert anonymize("sam lowercase wrote; Sam Lowercase too; sam; lowercase", known_names=known) == "[name] wrote; [name] too; sam; lowercase"
    # the file label of a chat export is anonymized the same way
    assert anonymize("gre-batch.txt", known_names=("Rahul GRE Tutor",)) == "gre-batch.txt"


# --------------------------------------------------------------------------- profile pages
PROFILE_URLS = [
    "https://in.linkedin.com/in/priya-sharma-1a2b3c", "https://www.linkedin.com/in/rahul-sharma-123/",
    "https://www.quora.com/profile/Priya-Sharma-12", "https://x.com/priya_s", "https://twitter.com/priya_s/with_replies",
    "https://www.youtube.com/@rahulverma", "https://www.youtube.com/channel/UCabc123/videos", "https://youtube.com/c/somebody",
    "https://youtube.com/user/somebody", "https://www.facebook.com/some.person", "https://www.facebook.com/profile.php?id=100001",
    "https://www.instagram.com/some.one/", "https://www.tiktok.com/@someone", "https://medium.com/@someone",
    "https://www.reddit.com/user/someone123/", "https://old.reddit.com/u/abc", "https://stackoverflow.com/users/12345/rahul",
    "https://math.stackexchange.com/users/999", "https://news.ycombinator.com/user?id=pg", "https://github.com/damien5314",
    "https://t.me/rahul123", "https://wa.me/919876543210", "https://www.threads.net/@someone",
]
POST_URLS = [
    "https://x.com/priya_s/status/123", "https://www.youtube.com/watch?v=abc123", "https://www.reddit.com/r/GRE/comments/abc/title/",
    "https://github.com/damien5314/RxReddit", "https://www.quora.com/What-is-the-best-GRE-coaching/answer/Priya-Sharma-12",
    "https://www.linkedin.com/pulse/gre-prep-tips-x", "https://www.linkedin.com/posts/priya_gre-activity-1234",
    "https://medium.com/@someone/my-gre-story-abc", "https://www.instagram.com/p/abc123/", "https://www.facebook.com/groups/gre/posts/1",
    "https://www.tiktok.com/@someone/video/123", "https://stackoverflow.com/questions/1/how", "https://news.ycombinator.com/item?id=1",
    "https://x.com/i/flow/login", "https://forum.test/t/thread/1", "",
]


@pytest.mark.parametrize("url", PROFILE_URLS)
def test_is_profile_url_on_profile_pages(url):
    assert is_profile_url(url) is True


@pytest.mark.parametrize("url", POST_URLS)
def test_is_profile_url_on_posts_and_other_pages(url):
    assert is_profile_url(url) is False


def test_social_page_titles_lose_the_persons_name():
    """Web-search titles of social pages carry the person's name in a fixed shape (rule 5)."""
    cases = {
        "Priya Sharma - GRE Verbal Tutor - Magoosh | LinkedIn": "[name] - GRE Verbal Tutor - Magoosh | LinkedIn",
        "Priya Sharma on LinkedIn: GRE coaching fees are a scam": "[name] on LinkedIn: GRE coaching fees are a scam",
        "Priya Sharma's answer to What is the best GRE coaching in Hyderabad? - Quora": "[name]'s answer to What is the best GRE coaching in Hyderabad? - Quora",
        "Priya Sharma (@priya_s) / X": "[name] ([user]) / X",
        "Rahul Verma on X: \"paid 40k for coaching, scored 300\"": "[name] on X: \"paid 40k for coaching, scored 300\"",
        "My GRE story by Rahul Verma | Medium": "My GRE story by [name] | Medium",
        "Rahul Verma on Instagram: GRE prep tips": "[name] on Instagram: GRE prep tips",
    }
    for title, expected in cases.items():
        assert anonymize(title) == expected, title
        assert anonymize(anonymize(title)) == expected, title
    # ordinary titles with the same words survive
    for title in ["How To Prepare on X: a thread", "Best GRE Prep Courses in 2026 | Compared & Reviewed", "GRE Verbal Tutor - Magoosh | LinkedIn"]:
        assert anonymize(title) == title, title
