# Script Execution Order

This document explains the correct order to run the automation scripts in the Snookhead Selenium project.

---

## Folder Structure Used

The project contains the following relevant scripts:

- Games/game_creation/Game_creation.py  
- Games/game_deletion/Game_Deletion.py  
- tables/Table_creation/game_a.py  
- tables/Table_creation/game_b.py  
- tables/Table_creation/game_c.py  
- Booking/timed_booking.py  
- Booking/stopwatch_booking.py  
- Booking/frame_booking.py  
- main.py  

---

## Execution Hierarchy

The scripts must be executed in the following order.

---

## 1. Game Creation Script

```bash
python Games/game_creation/Game_creation.py
```

### Purpose:
- Logs into the application  
- Navigates to the setup section  
- Creates games: Game A, Game B, Game C  
- Stores game names in `games.txt`  
- Captures screenshots  

---

## 2. Table Creation for Game A

```bash
python tables/Table_creation/game_a.py
```

### Purpose:
- Opens Game A  
- Creates tables inside Game A  
- Adds:
  - Table A → Standard  
  - Table B → Standard  
  - Table C → Premium  
- Captures screenshots  

---

## 3. Table Creation for Game B

```bash
python tables/Table_creation/game_b.py
```

### Purpose:
- Opens Game B  
- Creates tables inside Game B  
- Applies pricing configuration  
- Captures screenshots  

---

## 4. Table Creation for Game C

```bash
python tables/Table_creation/game_c.py
```

### Purpose:
- Opens Game C  
- Creates tables inside Game C  
- Applies pricing configuration  
- Captures screenshots  

---

## 5. Booking Scripts

### (a) Timed Booking

```bash
python Booking/timed_booking.py
```

### Purpose:
- Logs into the application  
- Selects a table  
- Books table for fixed time  
- Selects member (battata_wada)  
- Confirms booking  
- Handles popups  
- Verifies timer functionality  
- Captures screenshots  

---

### (b) Stopwatch Booking

```bash
python Booking/stopwatch_booking.py
```

### Purpose:
- Logs into the application  
- Selects a table  
- Books table using stopwatch mode  
- Verifies live timer execution  
- Handles popups  
- Captures screenshots  

---

### (c) Frame Booking

```bash
python Booking/frame_booking.py
```

### Purpose:
- Logs into the application  
- Selects a table  
- Books table using frame-based mode  
- Sets frame count  
- Confirms booking  
- Handles popups  
- Captures screenshots  

---

## 6. Game Deletion Script

```bash
python Games/game_deletion/Game_Deletion.py
```

### Purpose:
- Logs into the application  
- Navigates to Set up menu  
- Clicks Edit option  
- Deletes a selected game  
- Confirms deletion  
- Captures screenshots  

---

## 7. Main End-to-End Script

```bash
python main.py
```

### Purpose:
- Executes complete end-to-end flow:
  - Login  
  - Owner’s Panel revenue check  
  - Table creation in Game C  
  - Table booking  
  - Timer validation  
  - Billing and payment  
  - Revenue verification  
- Ensures full system validation  
- Captures screenshots  

---

## Full Workflow

Run the scripts in this exact order:

```bash
python Games/game_creation/Game_creation.py
python tables/Table_creation/game_a.py  
python tables/Table_creation/game_b.py  
python tables/Table_creation/game_c.py  
python Booking/timed_booking.py  
python Booking/stopwatch_booking.py  
python Booking/frame_booking.py  
python Games/game_deletion/Game_Deletion.py  
python main.py  
```

---

## Important Notes

- Always run the game creation script first  
- Ensure the web application is running locally  
- Booking scripts depend on tables being created  
- Main script performs full end-to-end validation  
- Screenshots are saved in respective folders  
- Update this file if structure changes  