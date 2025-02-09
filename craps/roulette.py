import time
from functions import utils

output_file = f'roulette_{utils.today()}.csv'

header = 'Roll #, Set Twelve, Number, Color, Since Set\n'
utils.save_to_csv(output_file, data=header)

roll_number = 0
since_set = 0
sleep_time = 6

while True:
    number, set_twelve = utils.roulette_number()
    color = utils.roulette_color(number)

    if number == 0:
        roll_number = 0
    else:
        roll_number = roll_number + 1

    if set_twelve == "2nd 12":
        since_set = 0
    else:
        since_set = since_set + 1

    result = f'{roll_number}, {set_twelve}, {number}, {color}, {since_set}'
    utils.save_to_csv(output_file, data=result)

    x = 0 
    while x < sleep_time:
        print(f'Waiting {sleep_time - x} seconds for next roll...', end='\r')
        time.sleep(1)
        x = x + 1
        if x == sleep_time:
            print('\n')
