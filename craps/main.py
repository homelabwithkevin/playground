import random
import argparse
import os
from datetime import datetime

from functions import initialize, dice, utils

# Default Values
total_rolls = 0
current_roll = 0
winnings = 0
total_out = 0
record_game = True

# Intial Values
bank_roll = 500
board_type = 'craps' # crapless or craps
amount_per_roll = 10
across = 'y'

while True:
    if record_game:
        output_file = f'{utils.today()}.csv'

    if current_roll == 0:
        # bank_roll = input('Bank roll: ')
        utils.save_to_csv(output_file, data=f'Initial bank roll: {bank_roll}')
        utils.save_to_csv(output_file, data=f'Setting amount per roll: {amount_per_roll}')

        utils.save_to_csv(output_file, data=f'Setting game version to {board_type}\n')
        board = initialize.board(board_type=board_type)

        # across = input('Bet across (y/n): ')
        if across == 'y':
            print(f'\nInitial bet across...')
            board, total_bet = initialize.update_board(board, 'across', amount_per_roll)
            bank_roll -= total_bet
            # utils.save_to_csv(output_file, data=f'Bank roll after across bet: {bank_roll}\n')

        current_roll = 1
    else: # Play
        # File Headers
        data = f'\ndice_1,dice_2,sum_of_dice,result,bank_roll,total_bet,total_rolls\n'
        utils.save_to_csv(output_file, data=data, print_out=False)

        while True:
            total_rolls += 1

            if bank_roll < 0:
                bank_roll = input(f'Deposit more money or q to quit: ')
                if bank_roll == 'q':
                    utils.quit(bank_roll, total_rolls)
                    break
                elif type(bank_roll) == str:
                    bank_roll = int(bank_roll)
                else:
                    utils.quit(bank_roll, total_rolls)
                    break

            print(f'------------------------------')
            print(f'Bet: {total_bet}')
            print(f'Bankroll: {bank_roll}')
            dice_1, dice_2, sum_of_dice = dice.roll(False)
            print(f'------------------------------')
            print(f'{sum_of_dice} out!')
            print(f'------------------------------')

            if sum_of_dice == 7:
                result = 'loss'
            elif sum_of_dice in [1, 2, 3, 11, 12]:
                result = 'tie'
            else:
                result = 'win'

            data = f'\n{dice_1},{dice_2},{sum_of_dice},{result},{bank_roll},{total_bet},{total_rolls}'
            utils.save_to_csv(output_file, data=data, print_out=False)

            if sum_of_dice == 7:
                continue_game = input('loss, 7 out, (r)oll, (w)ithdraw, (q)uit: ')
                if continue_game == 'q':
                    board, total_bet = initialize.update_board(board, 'quit', 0, sum_of_dice, total_bet)
                    utils.quit(bank_roll, total_rolls)
                    break
                else:
                    # Reset board
                    board = initialize.board(board_type=board_type)
                    board, total_bet = initialize.update_board(board, 'across', amount_per_roll)
                    try:
                        bank_roll -= total_bet
                    except:
                        print(f'Out of money')
                        utils.quit(bank_roll, total_rolls)
                        break
            elif sum_of_dice in [1, 2, 3, 11, 12]:
                continue_game = input(f'tie, {sum_of_dice}, (r)oll, (w)ithdraw, (q)uit: ')
                if continue_game == 'q':
                    board, total_bet = initialize.update_board(board, 'quit', 0, sum_of_dice, total_bet)
                    utils.quit(bank_roll, total_rolls)
                    break
                continue
            else:
                try:
                    bank_roll += amount_per_roll
                except:
                    print(f'Out of money')
                    utils.quit(bank_roll, total_rolls)
                    break

                press = input(f'win, {sum_of_dice}, (r)oll, (w)ithdraw, (q)uit: ')
                if press == 'q':
                    board, total_bet = initialize.update_board(board, 'quit', 0, sum_of_dice, total_bet)
                    bank_roll += total_bet
                    utils.quit(bank_roll, total_rolls)
                    break
                else:
                    print(press)
                    # If enter key pressed
                    if not press:
                        board, total_bet = initialize.update_board(board, 'press', amount_per_roll, sum_of_dice, total_bet)
                    else:
                        amount_per_roll = int(press)
                        bank_roll -= amount_per_roll
                        print(f'New bet: {amount_per_roll}')
                        board, total_bet = initialize.update_board(board, 'press_custom', amount_per_roll, sum_of_dice, total_bet)

            if not record_game:
                print(f'| {dice_1} | {dice_2} | {sum_of_dice} | {result} |')

        if record_game:
            print(f'\nGame Record: {output_file}')

        break
