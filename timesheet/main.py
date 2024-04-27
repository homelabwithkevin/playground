from datetime import datetime, timedelta
import argparse
import random
import click
import pandas as pd

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
    return names

def arggy():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("action", help=("What action do you want to take?\n"
                                        "test: testing action\n"
                                        "generate_random_data: generate random data for projects\n"))
    args = parser.parse_args()

    if args.action == 'test':
        print('test')
    elif args.action == 'generate_random_data':
        print('Generating random data...')
        generate_random_data(count=10)
    else:
        print(f'Invalid action: {args.action}')

def calculate_duration(start, stop):
    start_hour = int(start.split(":")[0])
    start_minute = int(start.split(":")[1])
    stop_hour = int(stop.split(":")[0])
    stop_minute = int(stop.split(":")[1])

    in_seconds = (timedelta(hours=stop_hour, minutes=stop_minute) - timedelta(hours=start_hour, minutes=start_minute)).total_seconds()
    in_hours = in_seconds / 60.0
    return str(in_seconds), str(in_hours)

def write_to_file(data):
    with open('timesheet.csv', 'a') as file:
        file.write(data + "\n")

def open_file():
    df = pd.read_csv('timesheet.csv')
    table = df.pivot_table(values='hours', index=['week_number', 'date', 'result_select'], aggfunc='sum')
    print(table)

def generate_project_data(count=10):
    for i in range(count):
        start = "00:00"
        stop = "00:00"
        seconds = generate_random_numbers(count=3)
        hours = generate_random_numbers(count=1)
        result_select = generate_random_data(count=1)[0]

        data = ",".join([week_number, date, full_date, start, stop, seconds, hours, result_select])
        write_to_file(data)
        print(data)

now = datetime.now()
full_date, date, weekday, week_number = get_date(now)

@click.command()
def main():
    # Create a list of items to display
    items = generate_random_data(count=5)

    # Display the list using the click.secho() function
    x = 0

    click.secho(f'r: read CSV')
    click.secho(f'g: generate random data')

    for item in items:
        click.secho(f'{x}: {item}')
        x = x + 1

    select = click.prompt("\nSelect your item")

    if type(select) == int:
        result_select = items[int(select)]
        click.secho(f'\nEnter your start and stop time. 24-hour like 23:55.')
        start = click.prompt("\nStart")
        stop = click.prompt("\nstop")

        seconds, hours = calculate_duration(start, stop)

        data = ",".join([week_number, date, full_date, start, stop, seconds, hours, result_select])
        write_to_file(data)
        print(data)
    elif select == 'g':
        print(f'Generating random project data')
        generate_project_data()
    else:
        open_file()

if __name__ == '__main__':
    main()