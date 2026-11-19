# Tiny chess candidate

Original Python chess engine, ISC licensed. Run `python3 -P -s main.py`
with `MAKEFUN_ENV_URL` pointing to the competition environment.

The entry uses only the standard library. It searches deterministically
with a fixed 24,000-node budget, iterative deepening, alpha-beta/PVS,
quiescence, a transposition table, capture/killer/history move ordering,
late move reductions, and tapered material/positional evaluation.
All code and chess data are in main.py. No model calls, random choices,
or clock reads are used by the engine.

main.py is produced by the kit's official `makefun compress` command.
Keep .gitattributes to preserve its exact bytes when committing on Windows.
The readable source, tests, and local practice reports are development
artifacts outside this submission directory. Only commit this directory's
entry files; never add the kit, source, test outputs, or transcript bundle
to the size-limited snapshot. Submit genuine session logs separately.

Local tests do not certify the official Python 3.13 sandbox, transcript
gate, final qualification, or prize eligibility.
