# tiny-chess-01

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/katsuraxyz/tiny-chess-01/rank.svg)](https://make.fun/bounty/tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/katsuraxyz/tiny-chess-01/reward.svg)](https://make.fun/bounty/tiny-chess-01)

A chess engine in at most 4,096 bytes of Python for make.fun's tiny-chess-01
contest. main.py is the lzma-packed engine: iterative-deepening alpha-beta
(PVS) with quiescence search, a transposition table, capture/killer/history
move ordering, late move reductions and tapered material/positional
evaluation, on a fixed deterministic 24,000-node budget. Python 3.13
standard library only.

## Run it

```sh
python3 -P -s main.py
```

It talks to the competition env at `MAKEFUN_ENV_URL`.
