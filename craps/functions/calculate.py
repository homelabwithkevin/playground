from datetime import datetime

def calculate_roll_sum(existing_rolls):
    return sum([v for k, v in existing_rolls.items()])

def calculate_sum_of_dice(dice_1, dice_2):
    return dice_1 + dice_2

def calculate_point(sum_of_dice):
    if sum_of_dice in [7]:
        return 'loss'

    return 'point'
