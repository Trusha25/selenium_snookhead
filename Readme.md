# Snookhead Selenium Automation

This project automates **end-to-end workflows** of the Snookhead web application using **Python and Selenium WebDriver**.

The automation simulates real user actions such as:
- Logging in
- Creating games
- Creating tables
- Booking tables (timed, stopwatch, frames)
- Generating and paying bills
- Deleting games
- Verifying revenue updates

---

# Project Overview

The automation covers multiple workflows.

---

## 1. Game Creation

The game creation script performs the following actions:

- Logs into the application  
- Navigates to **Setup → Games**  
- Creates multiple games:
  - Game A
  - Game B
  - Game C  
- Saves screenshots during execution  
- Stores created game names in `games.txt`  

---

## 2. Table Creation

Separate scripts are used for each game.

Each script performs the following steps:

- Logs into the application  
- Opens a specific game  
- Adds tables inside that game  
- Creates the following tables:

| Table Name | Type     |
| ---------- | -------- |
| Table A    | Standard |
| Table B    | Standard |
| Table C    | Premium  |

- Enters pricing values  
- Saves screenshots during execution  

---

## 3. Booking Automation

The project includes three types of booking automation:

### (a) Timed Booking
- Books table for fixed time (e.g., 10 minutes)  
- Selects member (battata_wada)  
- Confirms booking  
- Handles popups  
- Verifies timer functionality  

### (b) Stopwatch Booking
- Books table using stopwatch mode  
- Verifies running timer  
- Handles popups  

### (c) Frame Booking
- Books table using frame-based mode  
- Sets frame count  
- Confirms booking  

---

## 4. Billing & Payment

- Navigates to billing section  
- Selects booked table/member  
- Clicks **Pay Now**  
- Confirms payment  
- Captures payment screenshots  

---

## 5. Game Deletion

- Logs into the application  
- Navigates to **Set up menu**  
- Clicks **Edit** option  
- Deletes selected game  
- Confirms deletion  
- Captures screenshots  

---

## 6. End-to-End Automation (Main Script)

The `main.py` script performs full system validation:

- Login  
- Owner’s Panel revenue check  
- Table creation (Game C)  
- Booking (timed)  
- Timer validation  
- Billing and payment  
- Revenue verification  

---

# Technologies Used

- Python  
- Selenium WebDriver  
- Google Chrome  
- ChromeDriver  

---

# Project Structure

```
snookhead_selenium/
│
├── Games/
│   ├── game_creation/
│   │   ├── Game_creation.py
│   │   ├── games.txt
│   │   └── screenshots/
│   │
│   └── game_deletion/
│       ├── Game_Deletion.py
│       └── screenshots/
│
├── tables/
│   └── Table_creation/
│       ├── game_a.py
│       ├── game_b.py
│       ├── game_c.py
│       └── screenshots/
│
├── Booking/
│   ├── timed_booking.py
│   ├── stopwatch_booking.py
│   ├── frame_booking.py
│   └── screenshots/
│
├── EXECUTION_FLOW.md
├── main.py
└── README.md
```

---

# How to Run the Scripts

Run the scripts in the following order:

### 1. Create Games
```
python Games/game_creation/Game_creation.py
```

### 2. Create Tables
```
python tables/Table_creation/game_a.py
python tables/Table_creation/game_b.py
python tables/Table_creation/game_c.py
```

### 3. Run Booking Scripts
```
python Booking/timed_booking.py
python Booking/stopwatch_booking.py
python Booking/frame_booking.py
```

### 4. Delete Game (Optional)
```
python Games/game_deletion/Game_Deletion.py
```

### 5. Run End-to-End Flow
```
python main.py
```

---

# Screenshots

All scripts capture screenshots automatically.

Screenshots are stored inside:

```
screenshots/
```

folders within each module.

---

# Notes

- Ensure the **Snookhead web application is running locally** before executing scripts  
- Make sure **ChromeDriver is installed and compatible** with your Chrome version  
- Follow the execution order mentioned in `EXECUTION_FLOW.md`  
- Booking scripts depend on tables being already created  
- Main script validates the **complete system workflow**  

---

# Summary

This project provides a complete Selenium automation suite for:

- Game management  
- Table management  
- Booking workflows  
- Billing and payments  
- System validation  

It ensures reliable and repeatable testing of the Snookhead application.