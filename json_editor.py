import json
from colorama import Fore, Back, Style, init

# def jsonedit():
#     with open('testfile.json') as file:

init(autoreset=True)

file = 'testfile.json'


def list():
    print('Here are the current settings:')

    print('')

    print(Back.WHITE + '1', f'{paramnames["1"]}: {data[params[str(1)]]}%')
    print(Back.WHITE + '2', f'{paramnames["2"]}: {data[params[str(2)]]}%')

    print('')

    print(Back.WHITE + '3', f'{paramnames["3"]}: {data[params[str(3)]]} degrees Celcius')
    print(Back.WHITE + '4', f'{paramnames["4"]}: {data[params[str(4)]]} degrees Celcius')

    print('')

    print(Back.WHITE + '5', f'{paramnames["5"]}: {data[params[str(5)]]}%')
    print(Back.WHITE + '6', f'{paramnames["6"]}: {data[params[str(6)]]}%')

    print('')

    print(Back.WHITE + '7', f'{paramnames["7"]}: {data[params[str(7)]]} pH')
    print(Back.WHITE + '8', f'{paramnames["8"]}: {data[params[str(8)]]} pH')
    print(Back.WHITE + '9', f'{paramnames["9"]}: {data[params[str(9)]]} pH')

    print('')

    print(Back.WHITE + '10', f'{paramnames["10"]}: {data[params[str(10)]]}')

    print('')
    if doBeep:
        print(Back.WHITE + '11', 'Buzzer: on')
    elif not doBeep:
        print(Back.WHITE + '11', 'Buzzer: off')


def process(index, value):
    if index in (1, 2, 5, 6):
        if index in (1, 2):
            return f'{value}%'
        else:
            return f'{value}%'
    elif index in (3, 4):
        return f'{value} degrees Celcius'
    elif index in (7, 8, 9):
        return f'{value} pH'
    elif index == 11:
        if value:
            return 'on'
        elif not value:
            return 'off'
        else:
            raise ValueError


def deprocess(index, value):
    return value


with open(file) as settings:
    data = json.load(settings)

params = {'1': 'soilhum_low_threshold', '2': 'soilhum_high_threshold', '3': 'airtemp_low_threshold',
          '4': 'airtemp_high_threshold', '5': 'airhum_low_threshold',
          '6': 'airhum_high_threshold', '7': 'ph_low_threshold', '8': 'ph_high_threshold', '9': 'pH_sensor_zero_shift',
          '10': 'luminance_low_threshold', '11': 'buzzer_on'}

paramnames = {'1': 'Lower soil humidity threshold', '2': 'Higher soil humidity threshold',
              '3': 'Lower air temperature threshold', '4': 'Higher air temperature threshold',
              '5': 'Lower air humidity threshold', '6': 'Higher air humidity threshold', '7': 'Lower pH threshold',
              '8': 'Higher pH threshold', '9': 'pH sensor zero shift (only for calibration)',
              '10': 'Luminance lower threshold', '11': 'Buzzer'}

minimum = {'1': '0.0', '2': '10.0', '3': '0.0',
           '4': '20.0', '5': '0.0',
           '6': '20.0', '7': '0.0', '8': '0.1', '9': '-7.0',
           '10': '0.0'}

maximum = {'1': '90.0', '2': '100.0', '3': '30.0',
           '4': '35.0', '5': '20.0',
           '6': '95.0', '7': '10.0', '8': '13.0', '9': '7.0'}

# soilhum_low = data['soilhum_low_threshold']
# airtemp_low = data['airtemp_low_threshold']
# airhum_low = data['airhum_low_threshold']
# ph_low = data['ph_low_threshold']
# lum_low = data['luminance_low_threshold']
#
# soilhum_high = data['soilhum_high_threshold']
# airtemp_high = data['airtemp_high_threshold']
# airhum_high = data['airhum_high_threshold']
# ph_high = data['ph_high_threshold']

doBeep = data['buzzer_on']
# zeroshift = data['pH_sensor_zero_shift']

data2 = data

print('Welcome to the GreenDom settings editor!')
print('')
while True:
    list()
    while True:
        command = input('Enter "change" and parameter number to change the parameter,'
                        ' "list" to view all current settings or "exit" to close the program. ')

        if 'change' in command:
            try:
                num = int(command.split(' ')[1])
                if 0 < num < 10:
                    # print(data)
                    # print(data[params[str(num)]])
                    print(f'{paramnames[str(num)]}: {process(num, data[params[str(num)]])}')
                    while True:
                        try:
                            n = input(f'Enter a new value between {float(minimum[str(num)])}'
                                      f' and {float(maximum[str(num)])} or type "back" to cancel: ')
                            try:
                                # if n.isdigit(NumericType="Decimal"):
                                new = float(n)
                            # else:
                            #     raise ValueError

                            except ValueError:
                                if n == 'back':
                                    print('Canceled!')
                                    break
                                else:
                                    print('Incorrect input. Please try again.')
                                    continue

                            if float(minimum[str(num)]) <= new <= float(maximum[str(num)]):
                                data[params[str(num)]] = deprocess(num, new)

                                print(f'The {paramnames[str(num)].lower()} is now set to '
                                      f'{process(num, data[params[str(num)]])}')
                                with open(file, 'w') as settings:
                                    json.dump(data, settings)
                                break

                            else:
                                print(f'Please enter a number between'
                                      f' {float(minimum[str(num)])} and {float(maximum[str(num)])}')

                        except ValueError:
                            print('Please input a number with decimal points.')

                elif num == 10:
                    # print(data)
                    # print(data[params[str(num)]])
                    print(f'{paramnames[str(num)]}: {data[params[str(num)]]}')
                    while True:
                        try:
                            n = input(f'Enter a new value from {float(minimum[str(num)])}'
                                      f' or type "back" to cancel: ')
                            try:
                                # if n.isdigit(NumericType="Decimal"):
                                new = float(n)
                            # else:
                            #     raise ValueError

                            except ValueError:
                                if n == 'back':
                                    print('Canceled!')
                                    break
                                else:
                                    print('Incorrect input. Please try again.')
                                    continue

                            if float(minimum[str(num)]) <= new:
                                data[params[str(num)]] = deprocess(num, new)

                                print(f'The {paramnames[str(num)].lower()} is now set to {data[params[str(num)]]}')
                                with open(file, 'w') as settings:
                                    json.dump(data, settings)
                                break

                            else:
                                print(f'Please enter a number from'
                                      f' {float(minimum[str(num)])}')

                        except ValueError:
                            print('Please input a number with decimal points.')

                elif num == 11:
                    print(f'{paramnames[str(num)]}: {process(11, data[params[str(num)]])}')
                    while True:
                        action = input('Would you like to toggle the buzzer (yes/no) ? ')
                        if action.lower() == 'yes':
                            data[params[str(num)]] = not data[params[str(num)]]
                            print(f'The buzzer is now {process(11, data[params[str(num)]])}.')
                            with open(file, 'w') as settings:
                                json.dump(data, settings)
                            break
                        elif action.lower() == 'no':
                            print('Canceled!')
                            break
                        else:
                            continue
                else:
                    print('There is no parameter under this number.')

            except ValueError:
                print("I don't think I can change this. Please try again.")
                continue
            except IndexError:
                print('Please enter the parameter number after the "change" command.')

        elif command == 'exit':
            quit()

        elif command == 'list':
            list()

        else:
            print(f'{command}: command not found. Please try again.')
