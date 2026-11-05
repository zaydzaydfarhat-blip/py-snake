🐍 Py-Snake

A classic Snake game that runs right inside your terminal.

Collect food, grow longer, avoid the walls and your own tail, and see how high you can score!

Py-Snake is written in Python 3 and uses the standard library. It needs no game assets or Pygame. Windows requires a small terminal compatibility package.

Simple • Lightweight • Keyboard-friendly

---

✨ Features

- 🐍 Classic Snake gameplay in your terminal
- 🍎 Collect food and grow your snake
- ⚡ Snake gets faster as you eat
- 🏆 Best score tracking during your session
- ⌨️ Arrow keys, WASD, and Vim controls
- 🖱️ Mouse/tap steering where supported
- ⏸️ Pause and resume
- 🔄 Restart after game over
- 📐 Automatic terminal resizing
- 🧪 Built-in self-test
- 🐧 Linux, macOS, and Windows support

🎮 Controls

Choose your favorite control scheme!

Direction| Arrow keys| WASD| Vim keys
Up| ↑| W| K
Down| ↓| S| J
Left| ←| A| H
Right| →| D| L

Other controls

Key| Action
P| Pause / Resume
Q| Quit
R| Restart after game over
Space| Restart after game over

📋 Requirements

- Python 3
- A compatible terminal
- Minimum terminal size: 20 × 6

No Pygame, external game engine, or graphics assets required.

---

🚀 Installation

🪟 Windows

1. Install Python 3 from https://www.python.org/downloads/
2. Open PowerShell or Windows Terminal.
3. Clone the repository:

git clone https://github.com/zaydzaydfarhat-blip/py-snake.git
cd py-snake

4. Install Windows terminal compatibility:

py -m pip install windows-curses

5. Start the game:

py snake.py

🍎 macOS

1. Install Python 3 from https://www.python.org/downloads/
2. Open Terminal.
3. Clone the repository:

git clone https://github.com/zaydzaydfarhat-blip/py-snake.git
cd py-snake

4. Start the game:

python3 snake.py

🐧 Linux

Ubuntu / Debian

Install Python and Git:

sudo apt update
sudo apt install python3 git

If curses is missing:

sudo apt install python3-curses

Arch Linux / Omarchy

sudo pacman -S python git

Fedora

sudo dnf install python3 git

Clone and run

git clone https://github.com/zaydzaydfarhat-blip/py-snake.git
cd py-snake
python3 snake.py

---

🧪 Self-test

Py-Snake includes a built-in headless test for its game logic.

Linux / macOS:

python3 snake.py --selftest

Windows:

py snake.py --selftest

Expected output:

selftest: all checks passed

🕹️ How to play

1. Launch Py-Snake.
2. Choose your preferred controls.
3. Collect food ("*") to grow.
4. Avoid the walls and your own body.
5. Keep playing and try to fill the entire board!

The snake gets faster as your score increases.

📁 Project structure

py-snake/
├── snake.py
├── README.md
└── .gitignore

🛠️ Built with

Technology| Purpose
Python 3| Programming language
curses| Terminal interface
OpenCode| AI coding assistant
ChatGPT| README documentation

🤖 AI Credits

Project created with OpenCode.

OpenCode helped with the development of Py-Snake.

- OpenCode: https://github.com/anomalyco/opencode
- ChatGPT: https://chatgpt.com/

README written by ChatGPT (OpenAI).

📜 License

No license file is currently included. Licensing information will be added when a license is chosen.

---

<div align="center">🐍 Py-Snake

Simple. Classic. Open Source-minded.

Made with ❤️, Python, and OpenCode.

📖 README written by ChatGPT.

⭐ Enjoying Py-Snake? Give the repository a star!

</div>
