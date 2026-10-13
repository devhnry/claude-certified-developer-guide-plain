"""Flag numbers, `code` terms and [n] citations in the original that are missing from the rewrite.
Usage: python3 -I tools/check_facts.py <chapter-file-name>"""
import re, sys
name = sys.argv[1]
o = open(f"book/chapters/{name}").read()
r = open(f"plain/chapters/{name}").read()
def facts(t):
    t = t.replace("**", "")
    fences = set(re.findall(r"```.*?```", t, re.S))
    t = re.sub(r"```.*?```", "", t, flags=re.S)
    return (set(re.findall(r"`[^`]+`", t)),
            set(re.findall(r"\d[\d,.]*[kKmM%]?", t)),
            set(re.findall(r"<sup>\[[\d,\s]+\]</sup>", t)),
            fences)
for label, a, b in zip(("code terms", "numbers", "citations", "code blocks"), facts(o), facts(r)):
    miss = sorted(a - b)
    print(f"{label}: {len(miss)} missing", miss[:40])
