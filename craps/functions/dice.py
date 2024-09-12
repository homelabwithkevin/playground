import random

def roll(enable_magic=False):
    sum_of_dice = 0
    result_magic = 0

    if enable_magic == 'yes':
        magic_number = random.randint(1, 1000)
        result_magic = magic_number % 1

    if result_magic == 1:
        dice_1, dice_2, sum_of_dice = magic_dice()
    else:
        while True:
            dice_1 = random.randint(1, 6)
            dice_2 = random.randint(1, 6)
            sum_of_dice = dice_1 + dice_2

            if sum_of_dice == 7 and enable_magic == 'infinite':
                print(f'Was 7, trying again')
            else:
                print(f'Roll complete')
                break

    return dice_1, dice_2, sum_of_dice 
            
def magic_dice(infinite=False):
    sum_of_dice = 0

    if infinite:
        while True:
            dice_1 = random.randint(1, 6)
            dice_2 = random.randint(1, 6)
            sum_of_dice = dice_1 + dice_2
            if sum_of_dice != 7:
                break
    else:
        while sum_of_dice != 7:
            dice_1 = random.randint(1, 6)
            dice_2 = random.randint(1, 6)
            sum_of_dice = dice_1 + dice_2

    return dice_1, dice_2, sum_of_dice
