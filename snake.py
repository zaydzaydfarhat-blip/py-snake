#!/usr/bin/env python3
"""snake.py - a terminal snake game.

Standard library only: no pip install, no assets, no config.
Controls: arrow keys or h/j/k/l or WASD. p pauses, q quits.
"""

import argparse
import curses
import os
import random
import sys
from collections import deque

UP, DOWN, LEFT, RIGHT = "UP", "DOWN", "LEFT", "RIGHT"
VECTORS = {UP: (-1, 0), DOWN: (1, 0), LEFT: (0, -1), RIGHT: (0, 1)}
OPPOSITE = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}

KEYS = {
    curses.KEY_UP: UP,
    curses.KEY_DOWN: DOWN,
    curses.KEY_LEFT: LEFT,
    curses.KEY_RIGHT: RIGHT,
    ord("w"): UP,
    ord("s"): DOWN,
    ord("a"): LEFT,
    ord("d"): RIGHT,
    ord("k"): UP,
    ord("j"): DOWN,
    ord("h"): LEFT,
    ord("l"): RIGHT,
}

SNAKE_CH, FOOD_CH, WALL_CH = "o", "*", "#"


class Game:
    """Pure game state. No terminal code, so it can be tested headless."""

    def __init__(self, height, width, rng=None):
        if height < 3 or width < 6:
            raise ValueError("board too small")
        self.height = height
        self.width = width
        self.rng = rng or random.Random()
        mid_y, mid_x = height // 2, width // 2
        self.body = deque([(mid_y, mid_x), (mid_y, mid_x - 1), (mid_y, mid_x - 2)])
        self.direction = RIGHT
        self.score = 0
        self.game_over = False
        self.food = None
        self._place_food()

    def _occupied(self):
        return set(self.body)

    def _place_food(self):
        occupied = self._occupied()
        free = [
            (y, x)
            for y in range(self.height)
            for x in range(self.width)
            if (y, x) not in occupied
        ]
        if not free:
            self.game_over = True  # board filled: you win
            self.food = None
            return
        self.food = self.rng.choice(free)

    def turn(self, direction):
        if direction in VECTORS and direction != OPPOSITE.get(self.direction):
            self.direction = direction

    def step(self):
        if self.game_over:
            return
        dy, dx = VECTORS[self.direction]
        head_y, head_x = self.body[0]
        new_head = (head_y + dy, head_x + dx)
        y, x = new_head

        if not (0 <= y < self.height and 0 <= x < self.width):
            self.game_over = True
            return

        grows = new_head == self.food
        tail = self.body[-1]
        if new_head in self._occupied() and not (new_head == tail and not grows):
            self.game_over = True
            return

        self.body.appendleft(new_head)
        if grows:
            self.score += 1
            self._place_food()
        else:
            self.body.pop()

    def resize(self, height, width):
        """Fit the run into a new board size without ending it."""
        height, width = max(3, height), max(6, width)
        self.height, self.width = height, width

        kept, seen = deque(), set()
        for y, x in self.body:
            cell = (min(max(y, 0), height - 1), min(max(x, 0), width - 1))
            if cell not in seen:
                seen.add(cell)
                kept.append(cell)
        self.body = kept or deque([(height // 2, width // 2)])

        food_ok = (
            self.food is not None
            and 0 <= self.food[0] < height
            and 0 <= self.food[1] < width
            and self.food not in set(self.body)
        )
        if not food_ok:
            if self.game_over:
                self.food = None
            else:
                self._place_food()

    @property
    def tick_ms(self):
        return max(60, 150 - self.score * 5)


def init_colors():
    """Colour pairs when the terminal has them, plain attributes otherwise."""
    if not curses.has_colors():
        return {}
    try:
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_GREEN, -1)
        curses.init_pair(2, curses.COLOR_RED, -1)
        curses.init_pair(3, curses.COLOR_BLUE, -1)
        curses.init_pair(4, curses.COLOR_YELLOW, -1)
    except curses.error:
        return {}
    return {
        "snake": curses.color_pair(1),
        "head": curses.color_pair(1) | curses.A_BOLD,
        "food": curses.color_pair(2) | curses.A_BOLD,
        "wall": curses.color_pair(3),
        "hud": curses.color_pair(4) | curses.A_BOLD,
        "hint": curses.A_DIM,
    }


def draw(stdscr, game, paused, high_score, attrs=None):
    attrs = attrs or {}
    try:
        _draw(stdscr, game, paused, high_score, attrs)
    except curses.error:
        pass


def _draw(stdscr, game, paused, high_score, attrs):
    stdscr.erase()
    stdscr.addstr(0, 0, f" score {game.score}   best {high_score} ", attrs.get("hud", 0))
    if paused:
        stdscr.addstr(0, 26, "[paused]", attrs.get("food", 0))

    top = 2
    for y in range(game.height):
        stdscr.addstr(top + y, 0, WALL_CH, attrs.get("wall", 0))
        stdscr.addstr(top + y, game.width + 1, WALL_CH, attrs.get("wall", 0))
    stdscr.addstr(top - 1, 0, WALL_CH * (game.width + 2), attrs.get("wall", 0))
    stdscr.addstr(top + game.height, 0, WALL_CH * (game.width + 2), attrs.get("wall", 0))

    if game.food and 0 <= game.food[0] < game.height and 0 <= game.food[1] < game.width:
        fy, fx = game.food
        stdscr.addstr(top + fy, 1 + fx, FOOD_CH, attrs.get("food", 0))
    for index, (by, bx) in enumerate(game.body):
        if index == 0:
            stdscr.addstr(top + by, 1 + bx, "@", attrs.get("head", 0))
        else:
            stdscr.addstr(top + by, 1 + bx, SNAKE_CH, attrs.get("snake", 0))

    stdscr.addstr(
        top + game.height + 2,
        0,
        "arrows/hjkl/wasd  p pause  q quit",
        attrs.get("hint", 0),
    )
    stdscr.refresh()


def board_size(rows, cols):
    """Playable area for a terminal that is rows x cols."""
    return max(3, rows - 6), max(20, cols - 2)


def too_small(rows, cols):
    return rows < 12 or cols < 30


def safe_addstr(stdscr, y, x, text, attr=0):
    """addstr that tolerates the last cell of the screen."""
    rows, cols = stdscr.getmaxyx()
    if not (0 <= y < rows) or x >= cols:
        return
    try:
        stdscr.addstr(y, x, text[: max(0, cols - x - 1)], attr)
    except curses.error:
        pass


def terminal_size():
    """Real terminal size, independent of whatever ncurses last noticed."""
    try:
        size = os.get_terminal_size(sys.__stdout__.fileno())
        return size.lines, size.columns
    except (OSError, ValueError, AttributeError):
        return curses.LINES, curses.COLS


def fit_to_terminal(game):
    """Re-sync ncurses and the board with the real window size."""
    rows, cols = terminal_size()
    if (rows, cols) != (curses.LINES, curses.COLS):
        try:
            curses.resizeterm(rows, cols)
        except curses.error:
            pass
    if not too_small(rows, cols):
        target = board_size(rows, cols)
        if (game.height, game.width) != target:
            game.resize(*target)
    return rows, cols


def wait_for_room(stdscr):
    """Wait until the terminal is big enough. Returns False if the user quits."""
    while True:
        rows, cols = terminal_size()
        if not too_small(rows, cols):
            return True
        stdscr.erase()
        safe_addstr(stdscr, 0, 0, "terminal too small")
        safe_addstr(stdscr, 1, 0, f"need 30x12, have {cols}x{rows}")
        safe_addstr(stdscr, 2, 0, "resize the window, or q to quit")
        stdscr.refresh()
        stdscr.timeout(250)
        if stdscr.getch() in (ord("q"), ord("Q")):
            return False


def draw_ending(stdscr, game, win, high_score, attrs):
    draw(stdscr, game, False, high_score, attrs)
    msg = f" you win! score {game.score} " if win else f" game over - score {game.score} "
    hint = " r restart   q quit "
    y = 2 + game.height // 2
    safe_addstr(stdscr, y, max(0, (game.width - len(msg)) // 2 + 1), msg, attrs.get("hud", 0))
    safe_addstr(stdscr, y + 1, max(0, (game.width - len(hint)) // 2 + 1), hint, attrs.get("hint", 0))
    stdscr.refresh()


def play(stdscr):
    curses.curs_set(0)
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    stdscr.nodelay(True)
    attrs = init_colors()
    high_score = 0

    while True:
        if not wait_for_room(stdscr):
            return
        game = Game(*board_size(*terminal_size()))
        paused = False
        stdscr.timeout(game.tick_ms)

        while not game.game_over:
            rows, cols = fit_to_terminal(game)
            small = too_small(rows, cols)
            stdscr.timeout(200 if small else (-1 if paused else game.tick_ms))

            key = stdscr.getch()
            if key in (ord("q"), ord("Q")):
                return
            if not small:
                if key in (ord("p"), ord("P")):
                    paused = not paused
                elif key in KEYS:
                    game.turn(KEYS[key])

            if small:
                stdscr.erase()
                safe_addstr(stdscr, 0, 0, "terminal too small")
                safe_addstr(stdscr, 1, 0, f"need 30x12, have {cols}x{rows}")
                safe_addstr(stdscr, 2, 0, "resize the window, or q to quit")
                stdscr.refresh()
                continue

            if not paused:
                game.step()
                stdscr.timeout(game.tick_ms)
            draw(stdscr, game, paused, high_score, attrs)

        high_score = max(high_score, game.score)
        win = game.food is None
        stdscr.timeout(-1)
        while True:
            fit_to_terminal(game)
            draw_ending(stdscr, game, win, high_score, attrs)
            key = stdscr.getch()
            if key in (ord("q"), ord("Q")):
                return
            if key in (ord("r"), ord("R"), ord(" ")):
                break


def selftest():
    """Headless checks so the logic can be verified without a terminal."""
    g = Game(8, 12, random.Random(0))
    assert len(g.body) == 3 and not g.game_over

    start_len = len(g.body)
    g.turn(LEFT)  # reversing is ignored while moving right
    assert g.direction == RIGHT
    g.turn(DOWN)
    assert g.direction == DOWN

    g.step()
    assert len(g.body) == start_len

    # walls kill
    g = Game(5, 8, random.Random(1))
    for _ in range(10):
        g.step()
    assert g.game_over, "should hit a wall"

    # food grows the snake and raises the score
    g = Game(10, 10, random.Random(2))
    g.food = (g.body[0][0], g.body[0][1] + 1)
    before = len(g.body)
    g.step()
    assert len(g.body) == before + 1 and g.score == 1

    # long random run stays consistent
    g = Game(12, 20, random.Random(3))
    for _ in range(4000):
        if g.game_over:
            break
        g.turn(g.rng.choice([UP, DOWN, LEFT, RIGHT]))
        g.step()
        assert len(set(g.body)) == len(g.body), "snake overlaps itself"
        assert all(0 <= y < g.height and 0 <= x < g.width for y, x in g.body)

    # terminal sizing helpers
    assert board_size(24, 80) == (18, 78)
    assert board_size(13, 31) == (7, 29)
    assert too_small(11, 80) and too_small(24, 29) and not too_small(12, 30)

    # shrinking mid-run keeps the snake inside and on-screen
    g = Game(20, 40, random.Random(4))
    for _ in range(10):
        g.step()
    assert not g.game_over
    g.resize(6, 10)
    assert all(0 <= y < 6 and 0 <= x < 10 for y, x in g.body), "resize left cells outside"
    assert g.body and len(set(g.body)) == len(g.body), "resize overlapped the snake"
    assert g.food is None or (0 <= g.food[0] < 6 and 0 <= g.food[1] < 10)
    assert g.food is None or g.food not in set(g.body)
    # and growing again still works
    g.resize(30, 90)
    assert (g.height, g.width) == (30, 90)
    if not g.game_over:
        g.step()

    print("selftest: all checks passed")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description="terminal snake")
    parser.add_argument("--selftest", action="store_true", help="run headless checks and exit")
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    try:
        curses.wrapper(play)
    except KeyboardInterrupt:
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
