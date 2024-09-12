import os
from datetime import datetime

def today():
    return datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

def save_to_csv(output_file, print_out=True, data=None):
    # Write actual data
    with open(f'{output_file}', 'a') as f:
            f.write(f'{data}')

    if print_out:
        print(data)

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
    if number in [6, 8]: # 7:6
        return round(amount * 2.2, 2)

    if number in [5, 9]: # 7:5
        return round(amount * 2.4, 2)

    if number in [4, 10]: # 9:5
        return round(amount * 2.8, 2)

    if number in [2, 12]: # 11:2
        return round(amount * 6.5, 2)

    if number in [3, 11]: # 11:4
        return round(amount * 3.75, 2)
