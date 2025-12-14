"""
    Created with Claude Code.
"""

from datetime import datetime


def get_dice_input():
    """Get dice values from user input."""
    while True:
        try:
            die1 = int(input("Enter die 1 (1-6): "))
            if die1 < 1 or die1 > 6:
                print("Please enter a number between 1 and 6")
                continue

            die2 = int(input("Enter die 2 (1-6): "))
            if die2 < 1 or die2 > 6:
                print("Please enter a number between 1 and 6")
                continue

            return die1, die2
        except ValueError:
            print("Please enter valid numbers")


def record_roll(die1, die2, filename="dice_rolls.txt"):
    """Record the dice roll to a file."""
    total = die1 + die2
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(filename, "a") as f:
        f.write(f"{timestamp} - Die 1: {die1}, Die 2: {die2}, Total: {total}\n")

    return total


def main():
    # Generate filename with current date and time
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"dice_rolls_{timestamp}.txt"

    print("Dice Rolling Recorder")
    print(f"Recording to: {filename}")
    print("-" * 40)

    while True:
        die1, die2 = get_dice_input()
        total = record_roll(die1, die2, filename)

        print(f"\nRecorded - Die 1: {die1}, Die 2: {die2}, Total: {total}")
        print("-" * 40)
        print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nThanks for playing!")
