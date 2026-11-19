# tiny-chess-01

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/katsuraxyz/tiny-chess-01/rank.svg)](https://make.fun/bounty/tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/katsuraxyz/tiny-chess-01/reward.svg)](https://make.fun/bounty/tiny-chess-01)

A chess engine within 4,096 bytes of Python for make.fun's tiny-chess-01
contest. main.py is the makefun-compress stub around an LZMA stream of the
readable source: iterative-deepening alpha-beta (principal variation
search), quiescence on captures and checks, a transposition table,
capture, killer and history move ordering, late move reductions, and a
tapered material-plus-positional evaluation with a bishop-pair term.
The search is deterministic on a fixed node budget of 48,000 nodes a
move; no wall clock, no seeded randomness and no model calls.

## Run it

```sh
python3 -P -s main.py
```

The engine reads MAKEFUN_ENV_URL and plays the trial's eight games.
