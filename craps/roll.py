from functions import dice

while True:
    print(dice.roll())
    press = input('Press Enter to roll again')
    if not press:
        continue
    else:
        break
