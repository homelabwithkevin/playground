import os
from datetime import datetime

def today():
    return datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

def save_to_csv(output_file, headers=None, data=None):
    # Write actual data
    with open(f'{output_file}', 'a') as f:
            f.write(f'{data}')

    print(data)
    print('\n')

def calculate_roll_sum(existing_rolls):
    return sum([v for k, v in existing_rolls.items()])

def calculate_sum_of_dice(dice_1, dice_2):
    return dice_1 + dice_2

def calculate_point(sum_of_dice):
    if sum_of_dice in [7]:
        return 'loss'

    return 'point'

def quit(bank_roll, total_rolls):
    print(f'\n\nFinal Bankroll: {bank_roll}')
    print(f'Final Total Roll Count: {total_rolls}')

def calculate_odds(number, amount):
    if number in [6, 8]:
        return amount * 1.5

    if number in [5, 9]:
        return amount * 1.75

    if number in [4, 10]:
        return amount * 2.5

