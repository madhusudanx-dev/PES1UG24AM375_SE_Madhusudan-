# Lab 4 - 2048

This folder contains the completed terminal 2048 lab. The original four-equal-tile merge defect is fixed, and the game now includes complete win/loss handling, one-step undo, best-score tracking, and concise move feedback.

## Run the game

From this folder, run:

```bash
python main.py
```

The game uses only the Python standard library. Use `W`, `A`, `S`, and `D` to move, `U` to undo the last successful move, and `Q` to quit.

## Run the tests

```bash
python -m unittest discover -s tests -v
```

The regression suite covers ordinary slides in all directions, four equal tiles, independent merges, score updates, unchanged and invalid moves, win and no-move states, tile creation, undo, best score, feedback, and quitting.

## Completed tasks

1. A tile can merge at most once per move. Merge points are added to the score.
2. Reaching 2048 or having no legal moves ends the game. A tile is created only after a successful, non-winning move.
3. Undo restores the board and score for the last successful move. The best score records the highest score reached during the run.
4. Each action reports its result once. Board-scanning methods do not print action feedback.

All game state stays in memory. No third-party runtime dependencies or persistent storage were added.

## Submission files

- `board.py`, `game.py`, `main.py`, and `requirements.txt` contain the updated game.
- `tests/` contains the standard-library regression tests.
- `videos/before_demo.mp4` and `videos/after_demo.mp4` are 10-second rendered walkthroughs of the baseline defect and corrected game behavior. They are generated demos, not desktop screen recordings.
- `LLM_CHAT_HISTORY.docx` records the request and implementation summary. The complete visible conversation is available at the [full chat history](https://chatgpt.com/s/cx_6ac868d2f7408191b56aa90440b8e0d6).

## Folder structure

```text
LAB4/
├── README.md
├── board.py
├── game.py
├── main.py
├── requirements.txt
├── LLM_CHAT_HISTORY.docx
├── tests/
└── videos/
    ├── before_demo.mp4
    └── after_demo.mp4
```
