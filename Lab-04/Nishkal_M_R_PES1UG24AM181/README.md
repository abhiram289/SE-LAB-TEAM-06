# Lab 4 – VibeCoding: Skyscraper Stack

Name: Nishkal M R | SRN: PES1UG24AM181 | Source repo: SETAPESU26/54_skyscrapper_stack

| Task | Change | Files |
|---|---|---|
| 1 | Fixed inverted overlap check (`overlap <= 0` -> `overlap > 0`); Space now restarts after game over, as the README states | `game/game_engine.py` |
| 2 | Perfect placement: snap flush, `PERFECT!` popup, streak bonus points, width restored after 2+ perfects in a row | `game/game_engine.py` |
| 3 | Falling, rotating debris for sliced off-cuts (and the whole block on a miss) | `game/debris.py`, `game/game_engine.py` |
| 4 | Sky gradient shifts day -> sunset -> dusk -> night -> space with height, stars at night | `game/game_engine.py` |

Run: `pip install pygame` then `python main.py`.

Contents: `Code/` updated game, `Videos/` before/after recordings, `Chat_History.pdf` AI conversation.
