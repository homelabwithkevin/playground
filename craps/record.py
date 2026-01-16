"""
    Created with Claude Code.
"""

from datetime import datetime


def get_dice_input():
    """Get dice values from user input."""
    while True:
        try:
            die1_input = input("Enter die 1 (1-6): ")
            if die1_input.lower() == 'q':
                return None, None

            die1 = int(die1_input)
            if die1 < 1 or die1 > 6:
                print("Please enter a number between 1 and 6")
                continue

            die2_input = input("Enter die 2 (1-6): ")
            if die2_input.lower() == 'q':
                return None, None

            die2 = int(die2_input)
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


def display_statistics(roll_counts):
    """Display statistics for all rolls."""
    print("\nRoll Statistics:")
    for total in range(2, 13):
        count = roll_counts.get(total, 0)
        if count > 0:
            print(f"  {total:2d}: {count:3d}")


def save_statistics(roll_counts, filename):
    """Save statistics to a file."""
    total_rolls = sum(roll_counts.values())

    with open(filename, "w") as f:
        f.write(f"Dice Roll Statistics\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total Rolls: {total_rolls}\n")
        f.write("=" * 50 + "\n\n")

        for total in range(2, 13):
            count = roll_counts.get(total, 0)
            percentage = (count / total_rolls * 100) if total_rolls > 0 else 0
            f.write(f"{total:2d}: {count:3d} ({percentage:5.1f}%)\n")


def main():
    # Generate filename with current date and time
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"dice_rolls_{timestamp}.txt"
    stats_filename = f"dice_statistics_{timestamp}.txt"

    # Initialize roll tracking dictionary
    roll_counts = {i: 0 for i in range(2, 13)}

    print("Dice Rolling Recorder")
    print(f"Recording to: {filename}")
    print("-" * 40)

    while True:
        die1, die2 = get_dice_input()

        if die1 is None:
            print("\n\nThanks for playing!")
            display_statistics(roll_counts)
            save_statistics(roll_counts, stats_filename)
            print(f"\nStatistics saved to: {stats_filename}")
            break

        total = record_roll(die1, die2, filename)
        roll_counts[total] += 1

        print(f"\nRecorded - Die 1: {die1}, Die 2: {die2}, Total: {total}")
        print(f"Times {total} has rolled: {roll_counts[total]}")
        print("-" * 40)
        print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nThanks for playing!")
