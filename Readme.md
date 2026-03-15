# Snookhead Selenium Automation

This project automates **game creation** and **table creation** in the Snookhead web application using **Python + Selenium WebDriver**.

## Project Overview

The automation covers two main workflows:

1. **Game Creation**
   - Login to the application
   - Open the **Setup** section
   - Create multiple games such as:
     - Game A
     - Game B
     - Game C
   - Save screenshots during execution
   - Store created game names in `games.txt`

2. **Table Creation**
   - Login to the application
   - Open a selected game
   - Add tables inside that game
   - Create:
     - Table A → Standard
     - Table B → Standard
     - Table C → Premium
   - Enter pricing details
   - Save screenshots during execution

---

## Technologies Used

- Python
- Selenium WebDriver
- Chrome Browser
- ChromeDriver

---

## Project Structure

```text
snookhead_selenium/
│
├── game_creation.py
├── table_creation.py
├── game_b_table_creation.py
├── game_c_table_creation.py
├── games.txt
├── screenshots/
└── README.md