# Script Execution Order

This document explains the correct order to run the automation scripts in the Snookhead Selenium project.

## Execution Hierarchy

The scripts must be executed in the following order:

1. **Game Creation Script**

Run this script first:

python game_creation.py
Purpose:
- Logs into the application
- Navigates to the Setup section
- Creates the following games:
  - Game A
  - Game B
  - Game C
- Stores created game names in `games.txt`
- Captures screenshots during execution

---

2. **Table Creation for Game A**

After games are created, run:
python game_a_table_creation.py


Purpose:
- Opens Game A
- Creates tables inside Game A
- Tables created:
  - Table A → Standard
  - Table B → Standard
  - Table C → Premium

---

3. **Table Creation for Game B**

Run:
python game_b_table_creation.py

Purpose:
- Opens Game B
- Creates tables inside Game B
- Applies pricing configuration

---

4. **Table Creation for Game C**

Run:

Purpose:
- Opens Game B
- Creates tables inside Game B
- Applies pricing configuration

---

4. **Table Creation for Game C**

Run:

Purpose:
- Opens Game B
- Creates tables inside Game B
- Applies pricing configuration

---

4. **Table Creation for Game C**

Run:
python game_c_table_creation.py

Purpose:
- Opens Game C
- Creates tables inside Game C
- Applies pricing configuration

---

## Full Workflow


