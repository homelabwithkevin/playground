from functions import dice, utils

output_file = f'rolls_{utils.today()}.csv'

header = 'Dice 1, Dice 2, Sum of Dice\n'
utils.save_to_csv(output_file, data=header)

while True:
    result = dice.roll()
    utils.save_to_csv(output_file, data=f'{result}\n')

    press = input('Press Enter to roll again')
    if not press:
        continue
    else:
        break
