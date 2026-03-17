# Script Execution Order

This document explains the correct order to run the automation scripts in the Snookhead Selenium project.

## Folder Structure Used

The project contains the following relevant scripts:

- Games/game_creation/Game_creation.py
- Games/game_deletion/Game_Deletion.py
- tables/Table_creation/game_a.py
- tables/Table_creation/game_b.py
- tables/Table_creation/game-c.py

---

## Execution Hierarchy

The scripts must be executed in the following order.

---

## 1. Game Creation Script

Run this script first:

python Games/game_creation/Game_creation.py

Purpose:
- Logs into the application
- Navigates to the setup/game creation section
- Creates the following games:
  - Game A
  - Game B
  - Game C
- Stores created game names in `games.txt`
- Captures screenshots during execution

---

## 2. Table Creation for Game A

After games are created, run:

python tables/Table_creation/game_a.py

Purpose:
- Opens Game A
- Creates tables inside Game A
- Tables created:
  - Table A → Standard
  - Table B → Standard
  - Table C → Premium

---

## 3. Table Creation for Game B

Run:

python tables/Table_creation/game_b.py

Purpose:
- Opens Game B
- Creates tables inside Game B
- Applies pricing configuration for Game B tables

---

## 4. Table Creation for Game C

Run:

python tables/Table_creation/game-c.py

Purpose:
- Opens Game C
- Creates tables inside Game C
- Applies pricing configuration for Game C tables

---

## Game_deletion

Purpose:
- login
- navigates through sidebar selects "set up menu"
- Clicks the Edit option in the Games section
- Selects the Delete option for a game
- confirm  the deletion 

## Full Workflow

Run the scripts in this exact order:

python Games/game_creation/Game_creation.py 
python tables/Table_creation/game_a.py  
python tables/Table_creation/game_b.py  
python tables/Table_creation/game-c.py
python Games/game_deletion/Game_deletion.py   

---

## Important Notes

- Always run the **game creation script first** before running any table creation script.
- Ensure the **web application is running locally** before executing the scripts.
- Do not change file names unless this execution document is updated.
- Screenshots captured during automation will be stored in the respective **screenshots** folders.