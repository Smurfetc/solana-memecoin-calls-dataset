#!/usr/bin/env python3
"""Check this dataset yourself. No dependencies, no network.

What it does:
  1. recomputes SHA-256 of calls.jsonl and compares it to attest.json
  2. checks every row parses and carries the seven documented fields
  3. recomputes the headline statistics straight from the file

What it does NOT do: verify the Bitcoin anchor. That needs the OpenTimestamps client,
because it talks to the blockchain:

    pip install opentimestamps-client
    ots verify calls-a.ots
    ots verify calls-b.ots

Usage:  python3 verify.py
"""
import hashlib
import json
import os
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "calls.jsonl")
ATTEST = os.path.join(HERE, "attest.json")
FIELDS = {"mint", "sym", "t", "utc", "mc", "peak", "tg"}


def main():
    if not (os.path.exists(DATA) and os.path.exists(ATTEST)):
        sys.exit("calls.jsonl or attest.json missing — run this from the repo root")

    raw = open(DATA, "rb").read()
    digest = hashlib.sha256(raw).hexdigest()
    att = json.load(open(ATTEST))

    print("SHA-256 of calls.jsonl : %s" % digest)
    print("SHA-256 in attest.json : %s" % att["sha256"])
    if digest != att["sha256"]:
        print("\nMISMATCH — the file is not the one that was stamped.")
        print("Either it was modified, or you have a newer dataset than this receipt.")
        sys.exit(1)
    print("match. stamped at %s (%d calls)\n" % (att["stamped_utc"], att["calls"]))

    rows, bad = [], 0
    for i, line in enumerate(raw.decode("utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            r = json.loads(line)
        except ValueError as e:
            bad += 1
            print("  line %d does not parse: %s" % (i, str(e)[:60]))
            continue
        if set(r) != FIELDS:
            bad += 1
            print("  line %d has unexpected fields: %s" % (i, sorted(set(r) ^ FIELDS)))
            continue
        rows.append(r)

    print("rows parsed : %d" % len(rows))
    print("rows broken : %d" % bad)
    if att["calls"] != len(rows):
        print("  note: attest.json says %d calls, file has %d" % (att["calls"], len(rows)))

    peaks = [r["peak"] for r in rows]
    caps = [r["mc"] for r in rows if r.get("mc")]
    n = len(peaks)
    print("\nrecomputed from the file itself:")
    for x in (2, 3, 5, 10, 50, 100):
        hit = sum(1 for p in peaks if p >= x)
        print("  reached %4dx : %5.1f%%  (%d calls)" % (x, 100.0 * hit / n, hit))
    print("  median peak   : %.2fx" % statistics.median(peaks))
    print("  median cap at call time : $%s" % format(int(statistics.median(caps)), ","))

    best = max(rows, key=lambda r: r["peak"])
    print("\nlargest: %s — called at $%s, peaked %.1fx  (t.me/SmugCalls/%d)"
          % (best["sym"], format(best["mc"], ","), best["peak"], best["tg"]))
    print("verify any single row by opening its mint on a Solana chart.")


if __name__ == "__main__":
    main()
