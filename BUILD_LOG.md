# BUILD_LOG — news-image-20261125

- Built: Wed 2026-11-25 01:18–01:41 UTC (08:18–08:41 WIB) by build agent (fresh session, started after the competition opened 2026-11-25T00:00Z).
- Entry: one 1024×1024 front page summing up Wednesday 25 November 2026 in 50 sourced stories: 15 illustrated feature cards, a UTC timeline ruler (7 events), a DATE CHECK box (10 excluded older stories + 1 "Not yet"), a world map with 15 numbered pins, and a region-grouped ALSO ON list (items 16–50). Every card carries a verification label (CONFIRMED / CLAIM / REPORTED + source).
- `draw.py` — authored fresh in this session (write + 3 genuine edit passes). Never copied from any previous edition.
- `main.ts` — copy-only entrypoint (Node 22, stdlib only): copies the committed `entry.png` to the output dir, validates PNG signature + 1024×1024, verifies sha256 after copy. It never runs draw.py or any subprocess at grade time.
- `entry.png` — 1024×1024, 212,248 bytes, sha256 `317748c7bffcfad1c89f1b8fdd2a68c4792f1a84f4e0834481264ad836a0b6b4`.
- Determinism: draw.py run 3 times by the build agent + 1 independent re-run by the watch run — identical sha256 every time. `main.ts` copy verified with matching sha256.
- Visual pass: rendered image viewed twice; fixed clipped masthead date, truncated decks/headlines, timeline collisions, DATE CHECK overlap, truncated also-on lines. Final render: all text complete, no overlaps.
- Consistency pass: DATE CHECK exclusions do not appear among the 50; all numbers re-added (11 wounded = 2+2+3+4; Huawei 10 of 12 counts; England 188/2 chasing 185, 41 balls left; confidence 103.3; Ifo 90.6).
- Kit: fresh download first try (no 503). RULES.txt + competition.yaml confirm: deadline 2026-11-27T00:00Z, $100 pot, 50 places (1st $20), escrowed, ≤1 MiB, ≤1024×1024, no network, runs twice with identical bytes. Judge z-ai/glm-5.3-flash.
- Research: RESEARCH_25NOV.md — 50 stories with source + date, 7 regions, 15 fields.
