#!/usr/bin/env python3
"""Build the Elements privacy-policy site (English authoritative + condensed locale pages).

English root = full policy. Locale pages = condensed convenience translations
(uniform template), each carrying the "English controls" note + trademark.
Run with no args to (re)build index.html. If translations.json exists, also
writes every <locale>/index.html.
"""
import json, os, pathlib, re

ROOT = pathlib.Path(__file__).parent
EMAIL = "rizkcorsight@rizkcorsight.com"
UPDATED = "2026-06-14"
# App name. STORE_TITLE is the full listing title; BRAND is the distinctive
# short form used throughout the policy body + trademark (and across locales,
# verbatim — brand names are not translated).
STORE_TITLE = "Periodic Table: Elements"
BRAND = "Elements"

def brandize(s):
    """Substitute the placeholder app token 'Elements' with the real brand."""
    return re.sub(r"\bElements\b", BRAND, s)

# (code, native name) — every language the app ships in. en is the root.
LOCALES = [
    ("en", "English"), ("ar", "العربية"), ("bg", "Български"), ("bn", "বাংলা"),
    ("ca", "Català"), ("cs", "Čeština"), ("da", "Dansk"), ("de", "Deutsch"),
    ("el", "Ελληνικά"), ("en-GB", "English (UK)"), ("es", "Español"),
    ("es-419", "Español (Latinoamérica)"), ("et", "Eesti"), ("fa", "فارسی"),
    ("fi", "Suomi"), ("fil", "Filipino"), ("fr", "Français"),
    ("fr-CA", "Français (Canada)"), ("gu", "ગુજરાતી"), ("he", "עברית"),
    ("hi", "हिन्दी"), ("hr", "Hrvatski"), ("hu", "Magyar"), ("id", "Indonesia"),
    ("it", "Italiano"), ("ja", "日本語"), ("kn", "ಕನ್ನಡ"), ("ko", "한국어"),
    ("lt", "Lietuvių"), ("lv", "Latviešu"), ("ml", "മലയാളം"), ("mr", "मराठी"),
    ("ms", "Melayu"), ("nl", "Nederlands"), ("no", "Norsk"), ("pl", "Polski"),
    ("pt-BR", "Português (Brasil)"), ("pt-PT", "Português (Portugal)"),
    ("ro", "Română"), ("ru", "Русский"), ("sk", "Slovenčina"),
    ("sl", "Slovenščina"), ("sr", "Српски"), ("sv", "Svenska"), ("ta", "தமிழ்"),
    ("te", "తెలుగు"), ("th", "ไทย"), ("tr", "Türkçe"), ("uk", "Українська"),
    ("ur", "اردو"), ("vi", "Tiếng Việt"), ("zh-Hans", "简体中文"),
    ("zh-Hant", "繁體中文"),
]
RTL = {"ar", "he", "fa", "ur"}

CSS = """:root{--parchment:#f4efe6;--parchment-deep:#ece5d9;--ink:#1b1f29;--ink-soft:#50586d;--ink-faint:#8d949d;--rule:#d4cabb;--accent:#3f6e7e}
@media (prefers-color-scheme:dark){:root{--parchment:#14161b;--parchment-deep:#1d2027;--ink:#f1ece2;--ink-soft:#b7bccb;--ink-faint:#8a909c;--rule:#343a45;--accent:#8fc2d0}}
*{box-sizing:border-box}html,body{margin:0;padding:0;background:var(--parchment);color:var(--ink);font-family:ui-rounded,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,system-ui,sans-serif;font-size:16px;line-height:1.65;-webkit-font-smoothing:antialiased}
.wrap{max-width:720px;padding:64px 24px 96px;margin:0 auto}header{margin-bottom:40px}
.eyebrow{font-size:11px;letter-spacing:1.4px;text-transform:uppercase;color:var(--accent);font-weight:600;margin-bottom:8px}
h1{font-family:"Iowan Old Style","Palatino Linotype",Palatino,"Hoefler Text",Georgia,serif;font-size:36px;font-weight:600;letter-spacing:-.4px;margin:0 0 12px;line-height:1.15}
.lede{color:var(--ink-soft);font-size:17px;margin:8px 0 0}
.rule{height:1px;background:var(--rule);margin:32px 0}
h2{font-family:"Iowan Old Style","Palatino Linotype",Palatino,"Hoefler Text",Georgia,serif;font-size:22px;font-weight:600;letter-spacing:-.2px;margin:40px 0 12px}
p{margin:0 0 16px}ul,ol{margin:0 0 20px;padding-left:22px}[dir=rtl] ul,[dir=rtl] ol{padding-left:0;padding-right:22px}li{margin:6px 0}strong{color:var(--ink)}
a{color:var(--accent);text-decoration:underline;text-underline-offset:2px;text-decoration-thickness:.5px}a:hover{text-decoration-thickness:1px}
.meta{color:var(--ink-faint);font-size:13px;margin-top:8px}
.note{margin:0 0 28px;padding:14px 16px;border:1px solid var(--rule);border-radius:10px;background:var(--parchment-deep);color:var(--ink-soft);font-size:.95em}
.langs{margin:0 0 26px;padding:14px 16px;border:1px solid var(--rule);border-radius:10px;font-size:.93em;color:var(--ink-soft)}
.langs a{display:inline-block;margin:0 10px 6px 0}[dir=rtl] .langs a{margin:0 0 6px 10px}
footer{margin-top:64px;padding-top:24px;border-top:1px solid var(--rule);color:var(--ink-faint);font-size:13px}
@media(max-width:600px){.wrap{padding:40px 20px 64px}h1{font-size:30px}h2{font-size:20px}}"""


def nav(prefix):
    """Language switcher. prefix='' on root, '../' on locale pages."""
    parts = []
    for code, name in LOCALES:
        href = prefix if code == "en" else f"{prefix}{code}/"
        parts.append(f'<a href="{href}">{name}</a>')
    return '<nav class="langs"><strong>Languages:</strong> ' + " ".join(parts) + "</nav>"


ENGLISH_BODY = f"""<div class="rule"></div>

<h2>What Elements does not do</h2>
<ul>
<li><strong>No accounts.</strong> Elements never asks for a username, email, phone number, or login of any kind. There is no server-side account, because there is no server.</li>
<li><strong>No analytics.</strong> Elements includes no Firebase, Google Analytics, Mixpanel, Amplitude, Sentry, Crashlytics, or any other analytics or telemetry SDK. There are no tracking pixels, no install pings, no usage counters.</li>
<li><strong>No advertising.</strong> Elements shows no ads and links to no ad networks.</li>
<li><strong>No network from Elements.</strong> The app has no server of its own and makes no network requests of its own — no endpoint to call, no sync service, no remote logging. The entire periodic table, every element page, the artwork, and the spectra ship inside the app. Your study data never leaves your device. The one exception is the optional in-app purchase, which Apple&rsquo;s App Store or Google Play handle on their own servers (see <em>Purchases</em>).</li>
<li><strong>No cloud service.</strong> Elements does not use iCloud sync, Google Drive, or any third-party cloud. Your decks and study history live in the app&rsquo;s private sandbox on your device. (If you back up your device to iCloud or Google, your Elements data is included in your own private device backup; the developer has no access to it.)</li>
<li><strong>No third-party sharing.</strong> Elements does not share, sell, or rent your data to anyone, because Elements has no data to share. There is no cross-app or cross-site tracking.</li>
</ul>

<h2>What Elements stores on your device</h2>
<p>The following lives in Elements&rsquo;s sandboxed app storage and is visible only to Elements on your device:</p>
<ol>
<li><strong>Your study material</strong> — the decks and flashcards you study or build, including any custom drills.</li>
<li><strong>Study history</strong> — your review records and each card&rsquo;s spaced-repetition schedule (the data needed to decide when to show a card next), plus your study streak.</li>
<li><strong>Starred elements</strong> — the elements you mark as favorites.</li>
<li><strong>Settings</strong> — your preferences, such as the appearance (dark/light) and the optional study-reminder time, plus a flag that records you have seen the welcome screens.</li>
</ol>
<p>The home-screen widget renders from the app&rsquo;s own bundled element data on your device; it needs no shared account and makes no network request. Deleting a deck removes it; uninstalling Elements removes everything Elements ever wrote.</p>

<h2>Spoken element names</h2>
<p>Elements can read an element&rsquo;s name aloud using your device&rsquo;s built-in text-to-speech. This is audio <em>output</em> only — Elements does not use the microphone, does not listen, and records nothing. No audio is saved or sent anywhere.</p>

<h2>Notifications</h2>
<p>If you turn on the optional study reminder, Elements schedules a local notification on your device at the time you choose. It is scheduled and delivered entirely on-device — no notification content leaves your device, and Elements sends no push notifications from any server.</p>

<h2>Watch apps</h2>
<p>If you use the Apple Watch app, your study progress is exchanged directly between your iPhone and your paired Watch using Apple&rsquo;s on-device device-to-device connection. This sync does not pass through any server or cloud belonging to the developer. The Wear OS app uses bundled element data on the watch and does not use a developer server or cloud sync.</p>

<h2>On-device explainer (Apple Foundation Models)</h2>
<p>On a device that supports Apple&rsquo;s Foundation Models framework (iOS 26+ with Apple Intelligence enabled, on a capable iPhone), Elements may use the on-device model to phrase a short plain-language explanation of an element. This processing happens entirely on your device: your request is not uploaded, and the result is not stored or sent. If Apple Intelligence is not available, Elements simply uses its bundled written content instead — no network is involved either way.</p>

<h2>Purchases</h2>
<p>Elements is free to download with <strong>3 days of full access</strong>. Starting that 3-day access window happens locally on your device and does not create a subscription or charge. After the 3 days, a single optional <strong>one-time purchase</strong> unlocks the whole app permanently — there is no subscription and nothing auto-renews or auto-charges. That purchase or restore action is handled entirely by <strong>Apple&rsquo;s App Store</strong> (iOS) or <strong>Google Play</strong> (Android) through their own in-app purchase systems. Elements never sees or receives your name, payment card, or billing details. The developer receives only anonymous, aggregate sales figures from Apple and Google — never anything tied to you. Apple&rsquo;s and Google&rsquo;s handling of the transaction is governed by their own privacy policies.</p>

<h2>Children</h2>
<p>Elements does not knowingly collect any data from anyone of any age, because it collects nothing. The app contains no objectionable content and is rated 4+ (and the equivalent &ldquo;everyone&rdquo; rating on Google Play).</p>

<h2>Your rights</h2>
<p>Because Elements collects no data and keeps everything on your device, exercising rights under the GDPR, CCPA/CPRA, LGPD, or similar laws is straightforward: open the app to access your data; delete a deck or uninstall the app to erase it; there is nothing to opt out of, because nothing is sold, shared, or transmitted.</p>

<h2>Changes to this policy</h2>
<p>If Elements ever changes a privacy-affecting behaviour, this document will be updated and the change summarised here with the effective date. Elements&rsquo;s current design does not permit collecting, transmitting, or sharing your data; adding any such behaviour would require new code.</p>

<!-- trademarks -->
<h2>Trademarks</h2>
<p>Elements is a trademark of Rizk Corsight, LLC. Apple and App Store are trademarks of Apple Inc.; Google Play, Android, and Wear OS are trademarks of Google LLC. All other product and company names are used for identification only and remain the property of their respective owners.</p>

<h2>Contact</h2>
<p>Privacy questions or requests:<br>
<strong>Rizk Corsight</strong> — <a href="mailto:{EMAIL}">{EMAIL}</a></p>"""


def page(lang, dir_attr, title, head_extra, body, footer):
    return f"""<!DOCTYPE html>
<html lang="{lang}"{' dir="rtl"' if dir_attr else ''}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="referrer" content="strict-origin-when-cross-origin">
<title>{title}</title>
<style>
{CSS}
</style>
</head>
<body>
<main class="wrap">
{head_extra}
{body}
<footer>{footer}</footer>
</main>
</body>
</html>
"""


def build_english():
    head = (
        '<header>\n'
        '<div class="eyebrow">Privacy</div>\n'
        f'<h1>{STORE_TITLE} — Privacy Policy</h1>\n'
        f'<p class="lede">{STORE_TITLE} is a local-only periodic-table study app. '
        'The architecture below is the policy — the app cannot do otherwise, because the '
        'code does not contain the means to.</p>\n'
        f'<p class="meta">Last updated: {UPDATED} · Rizk Corsight · '
        f'<a href="mailto:{EMAIL}">{EMAIL}</a></p>\n'
        '</header>\n' + nav("")
    )
    html = page("en", False, f"{STORE_TITLE} · Privacy Policy", head, brandize(ENGLISH_BODY),
                f"{BRAND} · Periodic table study · No accounts · No analytics · No cloud · Everything on your device")
    (ROOT / "index.html").write_text(html, encoding="utf-8")
    print("wrote index.html (English)")


def build_locales():
    tpath = ROOT / "translations.json"
    if not tpath.exists():
        print("translations.json not found — skipping locale pages")
        return
    T = json.loads(tpath.read_text(encoding="utf-8"))
    count = 0
    for code, _name in LOCALES:
        if code == "en":
            continue
        t = T.get(code)
        if not t:
            print(f"  ! no translation for {code}")
            continue
        # Substitute the placeholder app token with the real brand (verbatim across
        # locales) in every translated field.
        t = {
            **t,
            "title": brandize(t["title"]), "note": brandize(t["note"]),
            "eyebrow": brandize(t["eyebrow"]), "contact_h": brandize(t["contact_h"]),
            "updated_label": t["updated_label"],
            "sections": [{"h": brandize(s["h"]), "p": brandize(s["p"])} for s in t["sections"]],
        }
        rtl = code.split("-")[0] in RTL
        secs = "\n".join(
            f"<h2>{s['h']}</h2>\n<p>{s['p']}</p>" for s in t["sections"]
        )
        body = (
            f'<header>\n<div class="eyebrow">{t["eyebrow"]}</div>\n'
            f'<h1>{t["title"]}</h1>\n'
            f'<p class="meta">{t["updated_label"]}: {UPDATED}</p>\n</header>\n'
            + nav("../")
            + f'\n<p class="note">{t["note"]} <a href="../">English</a></p>\n'
            + '<div class="rule"></div>\n'
            + secs
            + f'\n<h2>{t["contact_h"]}</h2>\n<p><a href="mailto:{EMAIL}">{EMAIL}</a></p>'
        )
        html = page(code, rtl, t["title"], "", body, t["title"])
        d = ROOT / code
        d.mkdir(exist_ok=True)
        (d / "index.html").write_text(html, encoding="utf-8")
        count += 1
    print(f"wrote {count} locale pages")


if __name__ == "__main__":
    build_english()
    build_locales()
