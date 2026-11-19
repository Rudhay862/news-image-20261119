# The World Today — 19 November 2026

One image summing up the world's news of Thursday 19 November 2026, built for the
[make.fun](https://make.fun/c/news-image-20261119) bounty
`news-image-20261119` ($250, top 50 share).

## The image

`entry.png` (1024×1024) is a front-page collage of the day's verified news:

- **Lead:** Grand Theft Auto VI begins its global rollout — gamers enter Vice City.
- Trump, Xi and Putin hold trilateral talks in Shenzhen at the APEC summit.
- Anthropic's historic Nasdaq debut — $83/share, a record $81.3B, the biggest IPO ever.
- US–Iran exchange fire again: the US hit a missile site on Qeshm Island; Iran hit a US
  base in Kuwait and a radar facility in Bahrain.
- Israeli ground operation in central Gaza; Crimea bridge attacked again; EU proposes a
  €45B loan for Ukraine.
- Nvidia's acting CEO promises earlier pay raises; H-series chip shipments to China stop.
- NASA's Voyager 1 reaches a one-light-day milestone.
- Ticker: Cyclone Akvan, Fed minutes, Australia sanctions, ICJ Myanmar ruling due,
  Peltola wins Alaska, Canada–China ties.

## How it works

`main.py` copies the bundled `entry.png` to `/output/entry.png` deterministically
(no network), verifying its SHA-256 first. `draw_image.py` is the Pillow program
that drew the image.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Referral

Try make.fun: https://make.fun/r/xk7vph3j
