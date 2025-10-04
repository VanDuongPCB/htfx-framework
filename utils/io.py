import unicodedata

# Global variables
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
GRAY   = "\033[90m"
RESET  = "\033[0m"



def get_text(msg: str = "Enter a string: ") -> str:
    txt = input(msg)
    txt = str(txt).strip()
    if len(txt) == 0:
        print("Input cannot be empty. Please enter a valid string.")
        return None
    
    # Normalize to NFC form to handle special characters
    txt = unicodedata.normalize('NFC', txt)

    # Remove non-UTF-8 characters
    txt = txt.encode('utf-8', 'ignore').decode('utf-8', 'ignore')
    return txt


def get_double(msg: str = "Enter a decimal: ") -> float:
    txt = input(msg)
    try:
        return float(txt)
    except ValueError:
        print("Invalid input. Please enter a valid decimal number.")
    return None


def get_integer(msg: str ="Enter a number: ") -> int:
    txt = input(msg)
    try:
        return int(txt)
    except ValueError:
        print("Invalid input. Please enter a valid integer.")
    return None

def get_boolean(msg: str = "Enter Yes or No: ") -> bool:
    txt = input(msg).strip().lower()
    if txt in ['yes', 'y', 'true', 't', '1']:
        return True
    elif txt in ['no', 'n', 'false', 'f', '0']:
        return False
    else:
        print("Invalid input. Please enter Yes or No.")
        return None
    
def get_select(msg: str, options: list) -> str:
    _texts = []
    _options = []
    for option in options:
        text = option + ","
        patterns = text.split(",")
        _texts.append(patterns[0])
        _options.append(patterns[1])
        pass


    while True:
        print(f"\n{msg}")
        for i, option in enumerate(_texts):
            print(f"{i+1}. {option}")
        print("0 or x. Exit")

        choice = input(f"Enter your choice (1 - {len(_texts)}): ").strip()
        if choice == '0' or choice.lower() == 'x':
            return None
        
        try:
            index = int(choice)
            if 0 < index <= len(options):
                return _options[index - 1]
            else:
                print("Invalid choice. Please select a valid option number.")
                pass
        except ValueError:
            print("Invalid input. Please enter a number corresponding to your choice.")
            pass
    


# def show_doing(message):
#     print(f"\r{GRAY}           {RESET} {message}\033[K", end="")
#     pass

# def show_succeed(message, new_line = ""):
#     print(f"\r{GREEN}[   OK   ]{RESET} {message}\033[K")
#     pass

# def show_failed(message, new_line = ""):
#     print(f"\r{RED}[ FAILED ]{RESET} {message}\033[K")
#     pass

# def show_handle(message, color, tagname):
#     pass