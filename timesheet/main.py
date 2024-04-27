from datetime import datetime
import argparse
import random

def get_date(now):
    full_date = now.strftime("%Y-%m-%d %H:%M - %A")
    date = now.strftime("%Y-%m-%d")
    weekday = now.strftime('%A')
    week_number = str(now.isocalendar()[1])
    return full_date, date, weekday, week_number

def generate_random_numbers(count=8):
    numbers = []
    for i in range(count):
        numbers.append(random.randint(1, 9))

    random_number = "".join(str(n) for n in numbers)
    return random_number

def generate_random_data(count=10):
    names = []
    for i in range(count):
        number = generate_random_numbers()
        names.append(f'PROJ-{number}')
    print(names)

now = datetime.now()
full_date, date, weekday, week_number = get_date(now)

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("action", help=("What action do you want to take?\n"
                                    "test: testing action\n"
                                    "generate_random_data: generate random data for projects\n"))
args = parser.parse_args()

if args.action == 'test':
    print('test')
elif args.action == 'generate_random_data':
    print('Generating random data...')
    generate_random_data()
else:
    print(f'Invalid action: {args.action}')