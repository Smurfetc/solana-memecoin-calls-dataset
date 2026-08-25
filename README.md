# Solana memecoin calls — a public record with the misses left in

**5,198 pump.fun token calls**, each with the market cap we called it at, the peak it reached
afterwards, and the exact second it was posted publicly. The whole file is hashed and the hash is
anchored in a Bitcoin block, so no row can be added, edited or back-dated after the fact.

Every trading channel publishes its winners. This is the same feed with the **losers still in it** —
about six calls in ten never double, and they are all here.

Live version and full methodology: **[smugcalls.com](https://smugcalls.com)** ·
dataset page: **[smugcalls.com/data.html](https://smugcalls.com/data.html)**

Built on the same feed: **[How many pump.fun launches actually graduate?](https://smugcalls.com/pumpfun-graduation-rate.html)**
— 825,123 launches measured over 30 days, with every denominator spelled out. Published estimates
range from 0.2% to 6% because each one silently counts something different.

New here? The short version — what the record is, why the losing calls are in it, and how to
disprove it in three commands: **[smurfetc.github.io/solana-memecoin-calls-dataset](https://smurfetc.github.io/solana-memecoin-calls-dataset/)**

---

## What's in the numbers

| | |
|---|---|
| Calls | 5,198 |
| Period | 2026-06-30 → 2026-08-25 |
| Median market cap at call time | **$11,210** |
| Reached 2x | 38.7% |
| Reached 3x | 23.7% |
| Reached 5x | 12.1% |
| Reached 10x | 5.2% |
| Reached 100x | 0.3% |
| Median peak | 1.64x |
| Largest | CATE — called at $21,077, peaked **4,566x** |

The low entry cap is the point: these are calls made on the bonding curve, before migration, not
after a chart has already moved.

## Schema

One JSON object per line (JSON Lines, UTF-8).

| field | type | meaning |
|---|---|---|
| `mint` | string | Token mint address on Solana (base58). Primary key of the row. |
| `sym` | string | Ticker as it appeared on pump.fun at call time. |
| `t` | integer | Unix timestamp of the call, in seconds. |
| `utc` | string | The same instant in ISO-8601 UTC, for convenience. |
| `mc` | number | Market cap in USD at the moment of the call — the entry reference. |
| `peak` | number | Highest multiple reached **after** the call, relative to `mc`. Ratchet: never revised down. |
| `tg` | integer | Message number in the public channel — `t.me/SmugCalls/<tg>`. |

```json
{"mc": 21077, "mint": "Ai66LHZG9MCzg1WKdawwqduVAXpNDUuV8M3uyq5ppump", "peak": 4167.35, "sym": "CATE", "t": 1785083184, "tg": 4448, "utc": "2026-07-26T16:26:24Z"}
```

## Verify it yourself

The file is only worth something if you can check it, so here is how.

```bash
# 1. hash the dataset — must equal "sha256" in attest.json
sha256sum calls.jsonl

# 2. confirm the hash is anchored in Bitcoin (needs `pip install opentimestamps-client`)
ots verify calls-a.ots
ots verify calls-b.ots
```

Or run the bundled checker, which does both and explains what it found:

```bash
python3 verify.py
```

`calls-a.ots` and `calls-b.ots` are OpenTimestamps receipts from two independent calendars. They
prove the exact byte content of `calls.jsonl` existed at the stamped moment. A call cannot be
inserted afterwards without changing the hash and invalidating both receipts.

Every row is independently checkable too: take `mint`, open it on any Solana chart, and compare
against `mc` and `t`.

## Check a single call without downloading anything

The file is browsable in a table right in the browser — search, sort, filter:

**[open the dataset viewer](https://huggingface.co/datasets/Smurfetc/solana-memecoin-calls/viewer/default/train)**

Type a ticker into the search box, take the `mint` from the row, paste it into any Solana
chart and compare against `mc` and `t`. That is the entire verification loop, and it takes
about ten seconds. Start with `CATE` — the largest call in the file.

## How `peak` is measured

`peak` is the highest market cap reached **after** the call divided by the market cap **at** the
call. Deliberately excluded: anything that happened before the call — a launch bundle that spiked
the price seconds before we posted is not our result and does not count. Post-migration highs do
count, since the token keeps trading.

It is a ratchet: it can rise as a token keeps running, never fall back. That makes it an honest
ceiling, not a running price.

## What this is not

**A peak is not a payout.** `peak` says the token traded there — not that anyone sold there, and
certainly not that you would have. Roughly nine of ten tokens that doubled later fell back below
where they peaked, and plenty went to zero afterwards. Read the file as a record of what happened,
not as a promise of what you would have made.

This is not financial advice, and it is not a claim that these numbers are reachable by anyone.

## Where it comes from

[SmugCalls](https://smugcalls.com) is a fully automated caller: it watches Solana on-chain activity,
posts to a public Telegram channel the moment its filters fire, and publishes this dataset from the
same database that drives the channel. Nothing is curated by hand — including the failures.

Channel: [t.me/SmugCalls](https://t.me/SmugCalls) · X: [@SmugDeg](https://x.com/SmugDeg)

## License

[CC0 1.0](LICENSE) — public domain. Use it, republish it, build on it, no attribution required.
