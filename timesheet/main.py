from datetime import datetime, timedelta
import argparse
import random
import click

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
    return in_seconds, in_hours

now = datetime.now()
full_date, date, weekday, week_number = get_date(now)

@click.command()
def main():
    # Create a list of items to display
    items = generate_random_data(count=5)

    # Display the list using the click.secho() function
    x = 0

    for item in items:
        click.secho(f'{x}: {item}')
        x = x + 1

    select = int(click.prompt("\nSelect your item"))
    result_select = items[select]

    click.secho(f'\nEnter your start and stop time. 24-hour like 23:55.')
    start = click.prompt("\nStart")
    stop = click.prompt("\nstop")

    seconds, hours = calculate_duration(start, stop)

    print("\n", week_number, date, full_date, start, stop, seconds, hours, result_select)

if __name__ == '__main__':
    main()