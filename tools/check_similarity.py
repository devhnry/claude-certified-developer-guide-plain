"""Fail if a rewrite reuses too much of the original, or is not shorter.
Usage: python3 -I tools/check_similarity.py <chapter-file-name>"""
import re, sys, difflib
name = sys.argv[1]
o = open(f"book/chapters/{name}").read()
r = open(f"plain/chapters/{name}").read()
def body(t):  # drop endnotes, which are copied verbatim on purpose
    return re.split(r"\n#+\s*(?:Notes|Endnotes|References|Sources)\b", t, maxsplit=1)[0]
def sents(t):
    t = re.sub(r"<sup>.*?</sup>", "", t.replace("**", "").replace("*", ""))
    t = re.sub(r"```.*?```", "", t, flags=re.S)
    return [s.strip().lower() for s in re.split(r"(?<=[.!?])\s+|\n+", t) if len(s.split()) >= 6]
so, sr = sents(body(o)), sents(body(r))
near = sum(1 for s in sr if difflib.get_close_matches(s, so, 1, 0.8))
pct = near * 100 // max(len(sr), 1)
wo, wr = len(body(o).split()), len(body(r).split())
bold_o, bold_r = o.count("**") // 2, r.count("**") // 2
print(f"reused sentences: {pct}% (limit 25)  words: {wo} -> {wr} (must be < {wo})  bold: {bold_o} -> {bold_r} (must be < {bold_o // 2})")
h2 = len(re.findall(r"^## ", body(o), re.M))
eli = len(re.findall(r"ELI5", body(r)))
print(f"ELI5 boxes: {eli} (need at least {max(h2 - 1, 1)}, one per major section)  length target: under {wo * 9 // 10} words, hard limit {wo * 95 // 100}")
ok = pct <= 25 and wr < wo * 95 // 100 and bold_r < bold_o // 2 and eli >= max(h2 - 1, 1)
print("PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
