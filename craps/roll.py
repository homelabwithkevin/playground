from functions import dice, utils

output_file = f'rolls_{utils.today()}.csv'

header = 'Dice 1, Dice 2, Sum of Dice, Roll #\n'
utils.save_to_csv(output_file, data=header)

roll_number = 0

while True:
    dice_1, dice_2, sum_of_dice = dice.roll()
    if sum_of_dice == 7:
        roll_number = 1
    else:
        roll_number = roll_number + 1

    result = f'{dice_1}, {dice_2}, {sum_of_dice}, {roll_number}\n'
    utils.save_to_csv(output_file, data=result)

    press = input('Press Enter to roll again')
    if not press:
        continue
    else:
        break
