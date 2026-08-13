import random
import subprocess
import sys

from lessons import LESSONS, get_lesson
from quiz_data import QUESTIONS


def pause() -> None:
    input("\nPress Enter to continue...")


def show_lessons() -> None:
    print("\n=== Lesson list ===")
    for lesson in LESSONS:
        print(f"{lesson['id']:>2}. {lesson['title']}")


def read_lesson() -> None:
    show_lessons()
    raw_id = input("\nChoose lesson id: ").strip()

    if not raw_id.isdigit():
        print("Lesson id must be a number.")
        return

    lesson = get_lesson(int(raw_id))
    if lesson is None:
        print("Lesson not found.")
        return

    print(f"\n=== {lesson['title']} ===")
    print(lesson["content"])


def run_quiz() -> None:
    print("\n=== Python quiz ===")
    raw_count = input(f"How many questions? 1-{len(QUESTIONS)} [default 5]: ").strip()

    if raw_count:
        if not raw_count.isdigit():
            print("Question count must be a number.")
            return
        count = int(raw_count)
    else:
        count = 5

    count = max(1, min(count, len(QUESTIONS)))
    questions = random.sample(QUESTIONS, count)
    score = 0

    for index, item in enumerate(questions, start=1):
        print(f"\nQuestion {index}/{count}: {item['question']}")
        for choice_index, choice in zip("ABCD", item["choices"]):
            print(f"  {choice_index}. {choice}")

        answer = input("Your answer: ").strip().upper()

        if answer == item["answer"]:
            print("Correct.")
            score += 1
        else:
            print(f"Wrong. Correct answer: {item['answer']}")

    percent = score / count * 100
    print(f"\nScore: {score}/{count} ({percent:.0f}%)")


def show_coding_tests() -> None:
    print("\n=== Coding tests ===")
    print("Open `exercises.py` and implement:")
    print("1. check_number(number)")
    print("2. even_squares(numbers)")
    print("3. summarize_numbers(raw_numbers)")
    print("4. BankAccount class")
    print("\nThen run:")
    print("python test_exercises.py")


def run_coding_tests() -> None:
    print("\n=== Running coding tests ===")
    result = subprocess.run(
        [sys.executable, "test_exercises.py"],
        text=True,
        capture_output=True,
        check=False,
    )

    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)

    if result.returncode == 0:
        print("All coding tests passed.")
    else:
        print("Some tests failed. Open exercises.py and fix the failing part.")


def main() -> None:
    while True:
        print("\n=== Python AI Mini Project ===")
        print("1. Show lesson list")
        print("2. Read a lesson")
        print("3. Take quiz")
        print("4. Show coding test tasks")
        print("5. Run coding tests")
        print("0. Exit")

        choice = input("Choose: ").strip()

        if choice == "1":
            show_lessons()
            pause()
        elif choice == "2":
            read_lesson()
            pause()
        elif choice == "3":
            run_quiz()
            pause()
        elif choice == "4":
            show_coding_tests()
            pause()
        elif choice == "5":
            run_coding_tests()
            pause()
        elif choice == "0":
            print("Bye.")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
