from datetime import datetime
import argparse

def get_date(now):
    full_date = now.strftime("%Y-%m-%d %H:%M - %A")
    date = now.strftime("%Y-%m-%d")
    weekday = now.strftime('%A')
    week_number = str(now.isocalendar()[1])
    return full_date, date, weekday, week_number

now = datetime.now()
full_date, date, weekday, week_number = get_date(now)

parser = argparse.ArgumentParser()
parser.add_argument("action", help="What do you want to do?")
args = parser.parse_args()

if args.action == 'test':
    print('test')
else:
    print(f'Invalid action: {args.action}')