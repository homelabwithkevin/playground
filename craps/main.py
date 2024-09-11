import random

def roll_dice():
    return random.randint(1, 12), random.randint(1, 12)

dice_1, dice_2 = roll_dice()

print(dice_1, dice_2)
