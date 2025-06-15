import json
import random
import os

FLASHCARD_FILE = "flashcards.json"

# Ensure the file exists and is initialized with empty JSON if missing
if not os.path.exists(FLASHCARD_FILE):
    with open(FLASHCARD_FILE, "w") as f:
        json.dump({}, f)

# Load existing flashcards if any
with open(FLASHCARD_FILE, "r") as file:
    content = file.read()
    flashcards = json.loads(content) if content else {}

while True:
    choice = input("\n1. Add Flashcard\n2. Quiz Yourself\n3. Exit\nChoose an option: ")

    if choice == "1":
        question = input("Enter the question: ")
        answer = input("Enter the answer: ")
        flashcards[question] = answer

        with open(FLASHCARD_FILE, "w") as file:
            json.dump(flashcards, file, indent=4)

        print("Flashcard added!\n")

    elif choice == "2":
        if not flashcards:
            print("No flashcards found!\n")
            continue

        score = 0
        for question in random.sample(list(flashcards.keys()), len(flashcards)):
            user_answer = input(f"{question}: ").strip().lower()
            correct_answer = flashcards[question].strip().lower()

            if user_answer == correct_answer:
                print("Correct!\n")
                score += 1
            else:
                print(f"Wrong! Answer: {flashcards[question]}\n")

        print(f"Quiz finished! Score: {score}/{len(flashcards)}\n")

    elif choice == "3":
        print("Goodbye!")
        break

    else:
        print("Invalid choice. Try again.\n")
