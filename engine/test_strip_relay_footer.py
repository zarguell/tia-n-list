#!/usr/bin/env python3
"""Collector relay-scaffolding contract (audit 2026-11-15).

The Mastodon and Reddit collectors append their own provenance lines to every
event body, and ssg's delta_body renders the body as article prose, so
/stories/<id>/ published sentences like "Citizen Lab found forensic evidence
that … on the via Mastodon https://english.mathrubhumi.com/…". 25,921 masto
bodies carried a "via Mastodon <url>" trailer on 2026-11-15.

  1. a trailing "via Mastodon <url>" line is removed, with or without a blank
     line before it;
  2. Reddit's "submitted by /u/… [link] [comments]" line is removed, but the
     "via reddit r/<sub>: <post text>" line survives because it carries the
     post's own text;
  3. a body that is nothing but scaffolding becomes empty, not "\\n";
  4. prose that merely mentions the phrase mid-paragraph survives;
  5. clean bodies are returned untouched;
  6. the strip is idempotent.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ssg

FAILS = []


def check(name, cond, detail=""):
    if cond:
        print(f"ok   {name}")
    else:
        print(f"FAIL {name} {detail}")
        FAILS.append(name)


strip = ssg.strip_relay_footer

check("masto trailer after blank line is dropped",
      strip("Citizen Lab found forensic evidence that ...\n\n"
            "via Mastodon https://english.mathrubhumi.com/technology/x\n")
      == "Citizen Lab found forensic evidence that ...\n")
check("masto trailer with no blank line is dropped",
      strip("Toot body text here.\nvia Mastodon https://example.org/a\n")
      == "Toot body text here.\n")
check("inline (truncated-body) masto trailer is dropped",
      strip("Update your sites immediately.\nvia Mastodon https://x.example/a\n")
      == "Update your sites immediately.\n")
check("wrap-around inline masto trailer is dropped",
      strip("Why I switched to static hosting without inline scripts. "
            "I have a 24-hour... via Mastodon https://habr.com/ru/articles/1\n")
      == "Why I switched to static hosting without inline scripts. "
         "I have a 24-hour...\n")
check("label-only masto trailer is dropped",
      strip("A toot about M365 data theft.\nvia Mastodon https://example.org/a"
            "\n\nvia Mastodon\n") == "A toot about M365 data theft.\n")
check("repeated masto trailer is dropped",
      strip("Toot text.\n\nvia Mastodon https://a.example/x\n\n\n"
            "via Mastodon https://b.example/y\n") == "Toot text.\n")
check("omitted-link variant is dropped",
      strip("Toot text.\n\nvia Mastodon (original link omitted in snippet)\n")
      == "Toot text.\n")
check("reddit submitter line is dropped, post text survives",
      strip("submitted by /u/someone [link] [comments]\n\n"
            "via reddit r/netsec: Something happened\n")
      == "via reddit r/netsec: Something happened\n")
check("inline reddit wrapper on a long post is dropped",
      strip("A long post body that runs to the cap. submitted by /u/x "
            "[link] [comments]\n\nvia reddit r/netsec: Post title\n")
      == "A long post body that runs to the cap.\n\n"
         "via reddit r/netsec: Post title\n")
check("scaffolding-only body becomes empty",
      strip("via Mastodon https://example.org/a\n") == "")
check("truncated masto trailer is dropped",
      strip("Nvidia released an open-weight model.\n\nvia Mastodon ...\n")
      == "Nvidia released an open-weight model.\n")
check("mid-text mention survives",
      strip("Attackers used Mastodon to coordinate.\n\n"
            "Despite the via Mastodon links cited by researchers, the campaign "
            "continued.\n")
      == "Attackers used Mastodon to coordinate.\n\n"
         "Despite the via Mastodon links cited by researchers, the campaign "
         "continued.\n")
clean = "A normal article body.\n\nWith a second paragraph.\n"
check("clean body is untouched", strip(clean) == clean)
check("empty body is untouched", strip("") == "")
body = strip("Body.\n\nvia Mastodon https://example.org/a\n")
check("strip is idempotent", strip(body) == body)

print()
if FAILS:
    print(f"{len(FAILS)} FAILED: {', '.join(FAILS)}")
    sys.exit(1)
print("all relay-scaffolding checks pass")
