# slop.py <file.html> - the writing half of the gate.
#
# grade.py measures pictures. This measures sentences. It checks the
# machine-checkable part of the local `unslop` skill against the prose a person
# will actually read on the page.
#
# IT DOES NOT TOUCH QUOTED USER SPEECH. Everything inside <blockquote> is the
# user's own words, misspellings included, and rewriting those would destroy the
# evidence. Those spans are stripped before anything is counted.
#
# It cannot run the skills. A script cannot invoke `unslop`, `bro`, `ste-writing`
# - those run in the agent. This catches the tells that survive
# a pass, so "I applied unslop" stops being a claim and becomes a check.
import io, re, sys, collections

if len(sys.argv) < 2:
    print("Usage: python3 slop.py <page.html>")
    sys.exit(2)
SRC = sys.argv[1]

# hard tells: an occurrence is a defect
HARD = {
 "AI vocabulary": r"\b(additionally|crucial|delve|enduring|enhance|fostering|garner|"
                  r"interplay|intricate|pivotal|showcase|tapestry|testament|underscore|vibrant|"
                  r"moreover|furthermore|utilize|leverage|facilitate|numerous|robust|seamless)\b",
 "puffery / promotional": r"\b(pivotal moment|testament to|evolving landscape|setting the stage|"
                  r"indelible|deeply rooted|groundbreaking|renowned|stunning|breathtaking|"
                  r"cutting-edge|world-class|next-generation|revolutionary|powerful)\b",
 "fancy ways to say is": r"\b(serves as|stands as|boasts|it features)\b",
 "not just X but Y": r"\bnot (just|only) .{1,60}?\bbut\b",
 "filler": r"\b(in order to|due to the fact that|it is important to note|"
                  r"it is worth noting|needless to say|at the end of the day)\b",
 "hedging stack": r"\b(could potentially|may possibly|might perhaps|it could be argued)\b",
 "chatbot phrasing": r"(I hope this helps|Let me know if|Of course!|Certainly!)",
 "superficial -ing": r",\s+(highlighting|ensuring|reflecting|showcasing|fostering|underscoring)\b",
 "vague attribution": r"\b(experts believe|industry reports suggest|some critics argue|studies show)\b",
}
# soft tells: legitimate in this project, so they are reported and not failed
SOFT = {
 "abstract metaphor noun": r"\b(substrate|nexus|locus|bedrock|flywheel|north star|"
                  r"paradigm|modality|gold-plating)\b",
 "em dash": r"\u2014|&mdash;",
 "generic conclusion": r"\b(the future looks|only time will tell|in conclusion)\b",
}

raw = io.open(SRC, encoding="utf-8").read()
# drop everything that is not prose the author wrote
body = re.sub(r"(?is)<(script|style|head)[^>]*>.*?</\1>", " ", raw)
quoted = len(re.findall(r"(?is)<blockquote", body))
body = re.sub(r"(?is)<blockquote.*?</blockquote>", " [USER QUOTE] ", body)
body = re.sub(r"(?is)<cite.*?</cite>", " ", body)
text = re.sub(r"<[^>]+>", " ", body)
text = re.sub(r"[ \t]+", " ", text)

def scan(rules):
    out = collections.OrderedDict()
    for name, pat in rules.items():
        hits = [m.group(0) for m in re.finditer(pat, text, re.I)]
        if hits:
            out[name] = hits
    return out

hard, soft = scan(HARD), scan(SOFT)
words = len(text.split())

print("=" * 66)
print(SRC)
print("=" * 66)
print("  prose words (user quotes excluded) ... %d" % words)
print("  user quotes protected ................ %d blockquotes" % quoted)
print()
if not hard:
    print("  PASS  no hard AI tells in the author's prose")
for name, hits in hard.items():
    c = collections.Counter(h.lower() for h in hits)
    print("  FAIL  %-24s %s" % (name, ", ".join('"%s" x%d' % (k, v) for k, v in c.most_common(6))))
for name, hits in soft.items():
    c = collections.Counter(h.lower() for h in hits)
    print("  NOTE  %-24s %d found: %s" % (name, len(hits),
          ", ".join('"%s" x%d' % (k, v) for k, v in c.most_common(4))))
print()
print("  This checks prose patterns. The agent must also apply the optional")
print("  writing helpers or the built-in plain-English pass.")
print()
print("  VERDICT: %s" % ("rewrite needed" if hard else "prose gate passed"))
