from functions import utils

def board(board_type):
    board = {}

    crapless_range = [2, 3, 4, 5, 6, 8, 9, 10, 11, 12]
    craps_range = [4, 5, 6, 8, 9, 10]

    if board_type == 'crapless':
        board_range = crapless_range
    elif board_type == 'craps':
        board_range = craps_range
    else:
        print(f'Incorrect board_type')

    for i in range(1, 13):
        if i in board_range:
            board[i] = 0

    print(board)
    return board 

def update_board(board, bet_type, amount_per_roll, sum_of_dice=0, total_bet=0):
    if bet_type == 'across':
        for number, bet in board.items():
            board[number] = amount_per_roll + board[number] 
            total_bet += amount_per_roll

    if bet_type == 'press':
        print(f'\nSum of dice for press: {sum_of_dice}')
        for number, bet in board.items():
            if number == sum_of_dice:
                amount_on_number = board[number] 

                result_amount = utils.calculate_odds(number, amount_on_number)
                print(f'Result amonut: {result_amount}')
                board[number] = amount_on_number + result_amount
                total_bet += amount_per_roll

    if bet_type == 'quit':
        total_bet = 0
        for number, bet in board.items():
            total_bet += board[number]
            board[number] = 0
        print(f'Resetting board')

    print(board)
    return board, total_bet
