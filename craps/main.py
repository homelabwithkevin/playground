import random
import argparse
import os
from datetime import datetime

parser = argparse.ArgumentParser(description='Roll two dice')
parser.add_argument('--count', '-c', type=int, default=1, help='Number of times to roll the dice')
args = parser.parse_args()

roll_count = args.count

def roll_dice():
    return random.randint(1, 6), random.randint(1, 6)

def calculate_sum_of_dice(dice_1, dice_2):
    return dice_1 + dice_2

def today():
    return datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

def calculate_point(sum_of_dice):
    if sum_of_dice in [7]:
        return 'loss'

    return 'point'

total_rolls = 0

output_file = f'{today()}.csv'
with open(f'{output_file}', 'a') as f:
    f.write(f'dice_1,dice_2,sum_of_dice,point\n')

while total_rolls < roll_count:
    dice_1, dice_2 = roll_dice()
    sum_of_dice = calculate_sum_of_dice(dice_1, dice_2)

    point = calculate_point(sum_of_dice)

    with open(f'{output_file}', 'a') as f:
        f.write(f'{dice_1},{dice_2},{sum_of_dice},{point}\n')

    print(sum_of_dice)
    total_rolls += 1

print(f'Saved to: {output_file}')
