from colorama import Fore, Back, Style

# NOTE:
# Function to print the banner

dim_text = Style.DIM

def print_banner():
    print(Fore.BLUE + ' __         ______     ______     __  __        ______     ______     __  __    ')
    print('/\ \       /\  __ \   /\___  \   /\ \_\ \      /\  == \   /\  __ \   /\ \_\ \   ')
    print('\ \ \____  \ \  __ \  \/_/  /__  \ \____ \     \ \  __<   \ \ \/\ \  \ \____ \  ')
    print(' \ \_____\  \ \_\ \_\   /\_____\  \/\_____\     \ \_____\  \ \_____\  \/\_____\ ')
    print('  \/_____/   \/_/\/_/   \/_____/   \/_____/      \/_____/   \/_____/   \/_____/ ')
    print(Fore.YELLOW + '|==============================================================================|')
    print('|====================== ' + Style.RESET_ALL + dim_text + 'Surprisingly Fast JoePeg Minting' + Style.RESET_ALL + Fore.YELLOW + ' ======================|')
    print('|==============================================================================|')
    print(Style.RESET_ALL)
