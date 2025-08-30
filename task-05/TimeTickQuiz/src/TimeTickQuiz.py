import requests
import html
import random
import threading
import time

CATEGORY_URL = "https://opentdb.com/api_category.php"
QUESTION_URL = "https://opentdb.com/api.php"
TIME_LIMIT = 15  # seconds per question

# ------------------ API functions ------------------
def fetch_categories():
    """Fetches trivia categories from the API."""
    response = requests.get(CATEGORY_URL)
    data = response.json()
    return data["trivia_categories"]

def fetch_questions(amount=10, category=None, difficulty=None, q_type=None):
    """Fetches questions based on selected filters from the API."""
    params = {"amount": amount}
    if category:
        params["category"] = category
    if difficulty:
        params["difficulty"] = difficulty
    if q_type:
        params["type"] = q_type
    response = requests.get(QUESTION_URL, params=params)
    data = response.json()
    return data["results"]

# ------------------ User input selection ------------------
def select_category(categories):
    """Prompts user to select a category from the list."""
    print("Select a category:")
    for idx, cat in enumerate(categories, 1):
        print(f"{idx}. {cat['name']}")
    while True:
        try:
            choice = int(input("Enter the number for your category: "))
            if 1 <= choice <= len(categories):
                return categories[choice - 1]["id"]
            else:
                print("Invalid choice. Please enter a number from the list.")
        except ValueError:
            print("Please enter a valid number.")

def select_difficulty():
    """Prompt user to select question difficulty."""
    options = ['easy', 'medium', 'hard']
    print("Select difficulty:")
    for idx, level in enumerate(options, 1):
        print(f"{idx}. {level}")
    while True:
        try:
            choice = int(input("Enter the number for difficulty: "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Please enter a number.")

def select_question_type():
    """Prompt the user to select type of questions (multiple/boolean)."""
    options = [('multiple', 'Multiple Choice'), ('boolean', 'True/False')]
    print("Select question type:")
    for idx, (_, label) in enumerate(options, 1):
        print(f"{idx}. {label}")
    while True:
        try:
            choice = int(input("Enter the number for question type: "))
            if 1 <= choice <= len(options):
                return options[choice - 1][0]
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Please enter a number.")

# ------------------ Quiz logic ------------------
def ask_question(question, index, total, score):
    """Presents a question to the user with a countdown timer and validates input."""
    print(f"\nQuestion {index + 1} of {total}")
    print(html.unescape(question["question"]))

    answers = question.get("incorrect_answers", []) + [question["correct_answer"]]
    answers = [html.unescape(ans) for ans in answers]
    random.shuffle(answers)

    for idx, ans in enumerate(answers, 1):
        print(f"{idx}. {ans}")

    user_answer = [None]
    input_received = [False]

    def get_input():
        while not input_received[0]:
            try:
                ans = input(f"Your answer (1-{len(answers)}): ").strip()
                if ans == "":
                    continue
                ans_int = int(ans)
                if 1 <= ans_int <= len(answers):
                    user_answer[0] = answers[ans_int - 1]
                    input_received[0] = True
                else:
                    print(f"Invalid choice. Please select a number between 1 and {len(answers)}.")
            except ValueError:
                print("Please enter a valid number.")

    timer_thread = threading.Thread(target=get_input)
    timer_thread.daemon = True
    timer_thread.start()

    start_time = time.time()
    while time.time() - start_time < TIME_LIMIT:
        if input_received[0]:
            break
        time.sleep(0.1)  # Small delay to reduce CPU usage

    if not input_received[0]:
        print("⏰ Time's up! No valid answer submitted.")
        correct = False
    else:
        correct = (user_answer[0] == html.unescape(question["correct_answer"]))
        if correct:
            print("✅ Correct!")
        else:
            print(f"❌ Oops! That's incorrect. The correct answer is: {html.unescape(question['correct_answer'])}. Better luck on the next one!")

    if correct:
        score[0] += 1

def select_quiz_options(categories):
    """Gathers all the quiz options and fetch questions accordingly."""
    cat_id = select_category(categories)
    difficulty = select_difficulty()
    q_type = select_question_type()
    while True:
        try:
            num = int(input("How many questions do you want (1-50)? "))
            if 1 <= num <= 50:
                break
            else:
                print("Enter a number between 1 and 50.")
        except ValueError:
            print("Please enter a valid number.")
    return cat_id, difficulty, q_type, num

# ------------------ Main function ------------------
def main():
    print("Welcome to TimeTickQuiz!\nTest your knowledge and your speed.\n")
    categories = fetch_categories()
    cat_id, difficulty, q_type, num = select_quiz_options(categories)
    questions = fetch_questions(amount=num, category=cat_id, difficulty=difficulty, q_type=q_type)
    if not questions:
        print("No questions found for the selected options. Try again!")
        return
    score = [0]  # List to allow mutable score in function
    for idx, question in enumerate(questions):
        ask_question(question, idx, len(questions), score)
    print(f"\nGame over! Your final score: {score[0]}/{len(questions)}")
    print("Thanks for playing TimeTickQuiz!")

if __name__ == "__main__":
    main()
