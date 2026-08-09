#!/usr/bin/env python3
"""Пересчитывает числа в README из самого файла — чтобы карточка не расходилась с данными.

Иначе README быстро начинает врать: датасет растёт ежедневно, а таблица в описании стоит.
Все значения берутся из calls.jsonl, ни одно не вписано руками.
"""
import io
import json
import os
import re
import statistics

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows = [json.loads(l) for l in io.open(os.path.join(HERE, "calls.jsonl"), encoding="utf-8") if l.strip()]
n = len(rows)
peaks = [r["peak"] for r in rows]
caps = [r["mc"] for r in rows if r.get("mc")]


def pct(x):
    return 100.0 * sum(1 for p in peaks if p >= x) / n


best = max(rows, key=lambda r: r["peak"])
table = "\n".join([
    "| | |",
    "|---|---|",
    "| Calls | {:,} |".format(n),
    "| Period | {} → {} |".format(min(r["utc"] for r in rows)[:10], max(r["utc"] for r in rows)[:10]),
    "| Median market cap at call time | **${:,}** |".format(int(statistics.median(caps))),
    "| Reached 2x | {:.1f}% |".format(pct(2)),
    "| Reached 3x | {:.1f}% |".format(pct(3)),
    "| Reached 5x | {:.1f}% |".format(pct(5)),
    "| Reached 10x | {:.1f}% |".format(pct(10)),
    "| Reached 100x | {:.1f}% |".format(pct(100)),
    "| Median peak | {:.2f}x |".format(statistics.median(peaks)),
    "| Largest | {} — called at ${:,}, peaked **{:,.0f}x** |".format(
        best["sym"], best["mc"], best["peak"]),
])

for name in ("README.md",):
    p = os.path.join(HERE, name)
    s = io.open(p, encoding="utf-8").read()
    new, cnt = re.subn(r"\| \| \|\n\|---\|---\|\n(?:\|.*\|\n)+", table + "\n", s, count=1)
    if not cnt:
        raise SystemExit("%s: таблица чисел не найдена — README изменил структуру" % name)
    # первая строка описания тоже содержит счётчик
    new = re.sub(r"\*\*[\d,]+ pump\.fun token calls\*\*",
                 "**{:,} pump.fun token calls**".format(n), new, count=1)
    if new != s:
        io.open(p, "w", encoding="utf-8").write(new)
        print("%s: числа обновлены (%d коллов)" % (name, n))
    else:
        print("%s: без изменений" % name)
