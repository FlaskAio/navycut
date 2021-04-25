from .colours import _Colours
from .logger import Console

def String(input_message:str=None) -> str:
    # if not input_message: input_message:str = Tool.default_path
    message = _Colours.white+"[ "+_Colours.cyan+"INPUT"+_Colours.white+" ] "+_Colours.yellow+input_message+_Colours.reset
    while True:
        input_msg = input(message)
        if not input_msg: continue
        else: 
            try: return str(input_msg)
            except:
                Console.log.Error("Failed to convert the entered data into string.")
                continue 
def Integer(input_message:str=None) -> int:
    # if not input_message: input_message:str = Tool.default_path
    message = _Colours.white+"[ "+_Colours.cyan+"INPUT"+_Colours.white+" ] "+_Colours.yellow+input_message+_Colours.reset
    while True:
        input_msg = input(message)
        if not input_msg: continue
        else: 
            try: return int(input_msg)
            except:
                Console.log.Error("Failed to convert the entered data into integer.")
                continue 
def Float(input_message:str=None) -> float:
    # if not input_message: input_message:str = Tool.default_path
    message = _Colours.white+"[ "+_Colours.cyan+"INPUT"+_Colours.white+" ] "+_Colours.yellow+input_message+_Colours.reset
    while True:
        input_msg = input(message)
        if not input_msg: continue
        else: 
            try: return float(input_msg)
            except:
                Console.log.Error("Failed to convert the entered data into float.")
                continue 
def Boolean(input_message:str=None) -> bool:
    # if not input_message: input_message:str = Tool.default_path
    message = _Colours.white+"[ "+_Colours.cyan+"INPUT"+_Colours.white+" ] "+_Colours.yellow+input_message+"(Y/n)"+_Colours.reset
    while True:
        input_msg = input(message)
        if not input_msg: continue
        if str(input_msg).lower() == "y" or str(input_msg).lower() == "yes": return True
        if str(input_msg).lower() == "n" or str(input_msg).lower() == "no": return False
        else: 
            Console.log.Error("Invalid input type.") 
            continue