from datetime import datetime, timedelta
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

def open_file(week=None):
    df = pd.read_csv('timesheet.csv')

    if week:
        df = df[df['week_number'] == int(week)]

    table = df.pivot_table(values='hours', index=['week_number', 'date', 'result_select'], aggfunc='sum')
    print(table)

def read_file():
    df = pd.read_csv('timesheet.csv')
    new_df = df[df['week_number'] == int(week_number) ]
    return new_df['result_select'].to_list()

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

def rounded_fifteen(round_to=15):
    rounded_time = round(now.minute / round_to) * round_to
    rounded_text = ":".join([str(now.hour), str(rounded_time)])

    return rounded_text

now = datetime.now()
full_date, date, weekday, week_number = get_date(now)

@click.command()
def main():
    items = read_file()
    x = 0

    options = [
        'CLI Options (or select existing item)',
        'n: new entry',
        'g: generate random data',
        'r: read CSV'
    ]

    separator = '========================'

    print(separator)
    for opts in options:
        click.secho(opts)
    print(separator)

    for item in items:
        click.secho(f'{x}: {item}')
        x = x + 1

    if not items:
        click.secho(f"No items yet for this week: {week_number} \n")
        select = 'n'
    else:
        click.secho(f"Available items for this week: {week_number} \n")
        select = click.prompt("\nSelect your item")

    if select.isdigit():
        result_select = items[int(select)]
        click.secho(f'\nEnter your start and stop time. 24-hour like 23:55.')
        start = click.prompt("\nStart", default=rounded_fifteen())
        stop = click.prompt("\nstop", default=rounded_fifteen())

        seconds, hours = calculate_duration(start, stop)

        data = ",".join([week_number, date, full_date, start, stop, seconds, hours, result_select])
        write_to_file(data)
        print(data)
    elif select == 'n':
        result_select = click.prompt("\nNew item name")
        start = click.prompt("\nStart", default=rounded_fifteen())
        stop = click.prompt("\nstop", default=rounded_fifteen())

        seconds, hours = calculate_duration(start, stop)

        data = ",".join([week_number, date, full_date, start, stop, seconds, hours, result_select])
        write_to_file(data)
        print(data)
    elif select == 'g':
        print(f'Generating random project data')
        generate_project_data()
    elif select == 'r':
        print(f'Reading csv...')
        select_week = click.prompt("\nSpecific week?", default=0)
        open_file(week=select_week)
    else:
        print(f'Invalid select: {select}')

if __name__ == '__main__':
    main()