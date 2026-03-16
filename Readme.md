# Snookhead Selenium Automation

This project automates **game creation** and **table creation** in the Snookhead web application using **Python and Selenium WebDriver**.

The automation scripts simulate user actions such as logging in, creating games, adding tables, and filling pricing details automatically.

---

# Project Overview

The automation covers two main workflows.

## 1. Game Creation

The game creation script performs the following actions:

* Logs into the application
* Navigates to the **Setup → Games** section
* Creates multiple games:

  * Game A
  * Game B
  * Game C
* Saves screenshots during execution
* Stores created game names in **games.txt**

---

## 2. Table Creation

Separate scripts are used for each game.

Each script performs the following steps:

* Logs into the application
* Opens a specific game
* Adds tables inside that game
* Creates the following tables:

| Table Name | Type     |
| ---------- | -------- |
| Table A    | Standard |
| Table B    | Standard |
| Table C    | Premium  |

* Enters pricing values
* Saves screenshots during execution

---

# Technologies Used

* Python
* Selenium WebDriver
* Google Chrome
* ChromeDriver

---

# Project Structure

```
snookhead_selenium/
│
├── Games/
│   └── game_creation/
│       ├── Game_creation.py
│       ├── games.txt
│       └── screenshots/
│
├── tables/
│   └── Table_creation/
│       ├── game_a.py
│       ├── game_b.py
│       ├── game-c.py
│       └── screenshots/
│
├── EXECUTION_FLOW.md
└── README.md
```

---

# How to Run the Scripts

Run the scripts in the following order.

### 1. Create Games

```
python Games/game_creation/Game_creation.py
```

This will create:

* Game A
* Game B
* Game C

---

### 2. Create Tables for Game A

```
python tables/Table_creation/game_a.py
```

---

### 3. Create Tables for Game B

```
python tables/Table_creation/game_b.py
```

---

### 4. Create Tables for Game C

```
python tables/Table_creation/game-c.py
```

---

# Screenshots

All automation steps capture screenshots automatically.

Screenshots are stored inside:

```
screenshots/
```

folders located within each script directory.

---

# Notes

* Ensure the **Snookhead web application is running locally** before executing the scripts.
* The scripts use **ChromeDriver**, so make sure it is installed and compatible with your Chrome version.
* Scripts should be executed in the order mentioned in **EXECUTION_FLOW.md**.
