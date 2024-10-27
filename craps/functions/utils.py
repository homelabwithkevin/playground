import os
import random
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
    rounded_bank_roll = round(int(bank_roll), 2)
    print(f'\n\nFinal Bankroll: {rounded_bank_roll}')
    print(f'Final Total Roll Count: {total_rolls}')

def calculate_odds(number, amount):
    if number in [6, 8]: # 7:6
        return round(amount * 1.2, 2)

    if number in [5, 9]: # 7:5
        return round(amount * 1.4, 2)

    if number in [4, 10]: # 9:5
        return round(amount * 1.8, 2)

    if number in [2, 12]: # 11:2
        return round(amount * 5.5, 2)

    if number in [3, 11]: # 11:4
        return round(amount * 2.75, 2)

def roulette_number():
    number = random.randint(0, 36)

    if number == 0:
        set_twelve = 'None'
    if 1 <= number <= 12:
        set_twelve = '1st 12'
    elif 13 <= number <= 24:
        set_twelve = '2nd 12'
    elif 25 <= number <= 36:
        set_twelve = '3rd 12'

    return number, set_twelve

def roulette_color(number):
    if number == 0:
        color = 'Green'
    elif number % 2 == 0:
        color = 'Red'
    else:
        color = 'Black'

    return color
