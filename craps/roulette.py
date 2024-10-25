from functions import utils

output_file = f'roulette_{utils.today()}.csv'

header = 'Roll #, Set Twelve, Number\n'
utils.save_to_csv(output_file, data=header)

roll_number = 0

while True:
    number, set_twelve = utils.roulette_number()

    if number == 0:
        roll_number = 0
    else:
        roll_number = roll_number + 1

    result = f'{roll_number}, {set_twelve}, {number}\n'
    utils.save_to_csv(output_file, data=result)

    press = input('Press Enter to spin again')

    if not press:
        continue
    else:
        break
