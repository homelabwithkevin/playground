from functions import dice, utils

output_file = f'rolls_{utils.today()}.csv'

header = 'Timestamp, Dice 1, Dice 2, Roll #, Sum of Dice\n'
utils.save_to_csv(output_file, data=header)

roll_number = 0

while True:
    dice_1, dice_2, sum_of_dice = dice.roll()

    if sum_of_dice == 7:
        roll_number = 0
    else:
        roll_number = roll_number + 1

    result = f'{utils.today()}, {dice_1}, {dice_2}, {roll_number}, {sum_of_dice}\n'
    print_result = f'{dice_1}, {dice_2}, {roll_number}, {sum_of_dice}\n'
    print(print_result)
    utils.save_to_csv(output_file, data=result, print_out=False)

    press = input('Press Enter to roll again')

    if not press:
        continue
    else:
        break
