# news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/giandraharfan11-crypto/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/giandraharfan11-crypto/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

A complete newspaper front page — "The World Today", Friday, 20 November 2026 — drawn at build time in code with Pillow by `generate.py` and committed in this repository as `entry.png`; `main.py` (Python standard library only) copies those exact bytes to /output/entry.png. The lead story is the International Court of Justice ruling, 9-6, that Myanmar committed genocide against the Rohingya, the first time the World Court has held a state responsible for genocide. Below it: Russia's overnight barrage of 110 missiles and some 400 drones on Kyiv hours after the Shenzhen summit (nine killed, 28 injured, three bridges damaged); Trump, Xi and Putin's first three-way summit in Shenzhen and its four-point declaration; and Anthropic's record $81.3bn Nasdaq debut, closing 17% above its offer price while the S&P 500 fell 2% and the Nikkei dropped 4.8%. A briefs strip adds the Houthi missile strike on Riyadh, COP31's dropped fossil-fuel phase-out, and Kenya's last Ebola patient discharged. No external images, no network, no randomness: the committed PNG is byte-identical on every run (1024x1024, under 1 MiB). `generate.py` is kept as the image's source so the page can be reproduced and audited; it is not the grader entrypoint.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Without `MAKEFUN_OUTPUT_DIR` it writes `/output/entry.png`, as the grader expects. To regenerate the image from source (requires Pillow): `MAKEFUN_OUTPUT_DIR=out python3 generate.py`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=6neab42c&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
