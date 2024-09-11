import random
import argparse

parser = argparse.ArgumentParser(description='Roll two dice')
parser.add_argument('--count', '-c', type=int, default=1, help='Number of times to roll the dice')
args = parser.parse_args()

roll_count = args.count

def roll_dice():
    return random.randint(1, 6), random.randint(1, 6)

def calculate_sum_of_dice(dice_1, dice_2):
    return dice_1 + dice_2

total_rolls = 0

while total_rolls < roll_count:
    dice_1, dice_2 = roll_dice()
    sum_of_dice = calculate_sum_of_dice(dice_1, dice_2)
    print(sum_of_dice)
    total_rolls += 1
