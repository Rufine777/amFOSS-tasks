# Task 05

---

When I started building **TimeTickQuiz**, my goal wasn’t just to make another trivia game.  
I wanted a **fast, real-time quiz** that could challenge both knowledge and reflexes.  
Here’s how I approached each step and why I made the choices I did.  

---

### 1. Choosing the Data Source (API)

I needed **live, diverse trivia questions** without creating my own database.  

- **Options I had**:
  - Hardcode questions myself (boring and limited).  
  - Use a CSV/JSON file with pre-written questions.  
  - Find a **free trivia API**.  

- **My choice**: [Open Trivia Database API](https://opentdb.com/api_config.php)  
  - Free and easy to use.  
  - Provides categories, difficulty levels, and types (multiple/boolean).  
  - Returns simple JSON.  

So I wrote `fetch_categories` and `fetch_questions` to connect with it.  

---

### 2. Making It Interactive (CLI)

I didn’t want a GUI or web app yet — too heavy for a simple idea.  

- **Options I had**:
  - GUI with Tkinter/PyQt.  
  - Web app with Flask/Django.  
  - Keep it simple with CLI menus.  

- **My choice**: CLI input functions (`select_category`, `select_difficulty`, `select_question_type`).  
  - Works everywhere.  
  - Easy to test and debug.  
  - Keeps focus on logic, not UI.  

---

### 3. Handling Question Text (HTML Entities)

The API sometimes returns text like `&quot;` instead of `"`.  

- **Options I had**:
  - Ignore it (messy for users).  
  - Replace manually.  
  - Use a built-in module.  

- **My choice**: `html.unescape` (Python’s standard library).  
  - Automatically cleans up all HTML entities.  

---

### 4. Randomizing Answers

If the correct answer always stayed in the same position, the quiz would be predictable.  

- **Options I had**:
  - Keep fixed positions.  
  - Shuffle manually.  
  - Use `random.shuffle`.  

- **My choice**: `random.shuffle` — clean, simple, built-in.  

---

### 5. Adding the Timer (Real-Time Challenge)

This was the most important feature: **15 seconds per question**.  
But `input()` is blocking in Python.  

- **Options I had**:
  - Skip the timer (too easy).  
  - Use `signal` (Unix-only, not portable).  
  - Use `threading` to separate input from timer.  

- **My choice**: `threading` + `time`.  
  - Cross-platform.  
  - Lets one thread handle input while the main loop checks time.  

That’s why `ask_question` spawns a thread (`get_input`) while the timer runs.  

---

### 6. Score Tracking

I wanted the score to update inside the question loop.  

- **Options I had**:
  - Use a global variable.  
  - Return values from each function.  
  - Use a mutable object like a list.  

- **My choice**: `score = [0]` (list trick).  
  - Lists are mutable, so functions can update them directly.  

---

### 7. Game Flow

The whole game is wrapped in `main()` with this flow:  
1. Greet the user.  
2. Fetch categories and let them choose.  
3. Ask how many questions to play.  
4. Fetch questions from API.  
5. Ask each with a 15-second limit.  
6. Show **instant feedback**   
7. End with a **final score summary**.  

I chose **immediate feedback** instead of waiting until the end — more interactive and fun.  

---

## Why This Approach Worked

- **API-driven** → always fresh questions.  
- **Threading + timer** → adds real challenge.  
- **CLI-first** → lightweight and accessible.  
- **Step-by-step modular design** → easy to extend later (high scores, GUI, web app).  

---

## What I Learned

- How to fetch and handle **external APIs** in Python.  
- How to deal with **real-time input** using threads.  
- How to design an interactive **CLI app**.  
- How to clean and randomize data from an API.  


## Get Started
Follow the steps below to set up and run TimeTickQuiz on your local machine:

### 1. Directory Structure
```bash 
TimeTickQuiz/`
├── src/`
│   ├── requirements.txt`
│   ├── time_tick_quiz.py`
└── README.md
```
### 2. Navigate to the Source Folder
```bash 
cd TimeTickQuiz/src
```
### 3. Create a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
``` 
### 4. Install Required Packages
```bash
 pip install -r requirements.txt
```
