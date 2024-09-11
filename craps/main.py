import random

def roll_dice():
    return random.randint(1, 6), random.randint(1, 6)

def calculate_sum_of_dice(dice_1, dice_2):
    return dice_1 + dice_2

dice_1, dice_2 = roll_dice()

sum_of_dice = calculate_sum_of_dice(dice_1, dice_2)

print(sum_of_dice)

