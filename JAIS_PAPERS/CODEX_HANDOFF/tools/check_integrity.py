"""Compare an old and a new main.tex and report what changed in the protected parts.

Usage: python check_integrity.py OLD.tex NEW.tex

Protected parts: tables, figures, algorithms, equations, citations, numbers.
Any difference listed here must be one that was asked for.
"""
import re
import sys
from collections import Counter

ENVS = ["table", "table*", "figure", "figure*", "algorithm", "equation",
        "equation*", "align", "align*", "tikzpicture", "thebibliography"]


def body(s):
    # Ignore the embedded bibliography when counting numbers in the text.
    return re.split(r"\\begin\{thebibliography\}", s)[0]


def envs(s, e):
    return re.findall(r"\\begin\{" + re.escape(e) + r"\}.*?\\end\{" + re.escape(e) + r"\}", s, re.S)


def cites(s):
    keys = []
    for group in re.findall(r"\\cite[a-z]*\{([^}]*)\}", s):
        keys += [k.strip() for k in group.split(",")]
    return keys


def numbers(s):
    return Counter(re.findall(r"(?<![A-Za-z])-?\d+(?:[.,]\d+)?", body(s)))


def main(old_path, new_path):
    a = open(old_path, encoding="utf-8").read()
    b = open(new_path, encoding="utf-8").read()
    ok = True
    for e in ENVS:
        ea, eb = envs(a, e), envs(b, e)
        same = ea == eb
        print(f"{e:16s} old={len(ea):3d} new={len(eb):3d} identical={same}")
        if not same:
            ok = False
            for i, (x, y) in enumerate(zip(ea, eb)):
                if x != y:
                    print(f"   first differing {e} block: #{i + 1}")
                    break
    ca, cb = set(cites(a)), set(cites(b))
    print("citations removed:", sorted(ca - cb) or "none")
    print("citations added:  ", sorted(cb - ca) or "none")
    na, nb = numbers(a), numbers(b)
    lost, added = na - nb, nb - na
    print("numbers lost: ", dict(lost) or "none")
    print("numbers added:", dict(added) or "none")
    if lost:
        ok = False
    print("RESULT:", "OK" if ok else "CHECK THE DIFFERENCES ABOVE")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
