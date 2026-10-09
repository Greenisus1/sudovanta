# sudovanta 1.0.0

Original offline fullscreen Sudoku. Generated9x9 puzzles retain exactly one solution while removing up to38 cells. Arrows/WASD move,1-9 enter a number,0/Backspace erases, P toggles pencil marks, N generates a new puzzle, Q quits. Fixed clues cannot change. Duplicate row/column/box numbers show red; pencil marks appear for the selected cell. No hints, difficulty grading or saved sessions.

Python3+curses standard library, color highlighting and monochrome fallback. Minimum60x26; inputs pause below that size. No network, accounts, pip packages or commercial assets. Install checks dependencies/source, no automatic package installation.

    bash app-store.sh install
    bash app-store.sh run
    python3 -m unittest -v

Six tests, including10 seeded unique-solution checks; fullscreen pencil-entry/resize/exit/restoration and actual pixels checked on Linux. Physical Raspberry Pi and non-Linux untested. MIT license.
