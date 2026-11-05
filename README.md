# py-snake

A tiny terminal snake game. Python 3, standard library only — no install step.

```bash
python3 snake.py
```

Controls: arrow keys or `h`/`j`/`k`/`l` or WASD. `p` pauses, `q` quits, `r` restarts after a game over.

The snake speeds up as it eats. Hitting a wall or your own body ends the run; filling the whole board is a win. Needs a terminal of at least 30x12.

There is also a headless check of the game logic:

```bash
python3 snake.py --selftest
```
