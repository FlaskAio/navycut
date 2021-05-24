from .colours import _Colours
from getpass import getpass

class Console:
    class log:
        def Success(message:str=None) -> str:
            print (_Colours.white+'[ '+_Colours.green+_Colours.bright+'SUCCESS'+_Colours.reset+_Colours.white+' ] '+_Colours.yellow+message+_Colours.reset)
        def Error(message:str=None) -> str:
            print (_Colours.white+'[ '+_Colours.red+_Colours.bright+'ERROR'+_Colours.reset+_Colours.white+' ] '+_Colours.yellow+message+_Colours.reset)
        def Info(message:str=None) -> str:
            def _print(message_) -> None:
                print (_Colours.white+'[ '+_Colours.blue+_Colours.bright+'INFO'+_Colours.reset+_Colours.white+' ] '+_Colours.yellow+message_+_Colours.reset)
            if "\n" in message:
                message_line_list:list = message.split("\n")
                for _message in message_line_list: _print(_message)
            else: _print(message)
        def Warning(message:str=None) -> str:
            print (_Colours.white+'[ '+_Colours.magenta+_Colours.bright+'WARNING'+_Colours.reset+_Colours.white+' ] '+_Colours.yellow+message+_Colours.reset) 

    class input:
        def String(input_message:str=None) -> str:
            
            message = _Colours.white+"[ "+_Colours.cyan+"INPUT"+_Colours.white+" ] "+_Colours.yellow+input_message+_Colours.reset
            input_msg = input(message)
            try: 
                return str(input_msg)
            except: Console.log.Error("Failed to convert into string.")
                
        def Password(input_message:str=None) -> str:
            
            message = _Colours.white+"[ "+_Colours.cyan+"INPUT"+_Colours.white+" ] "+_Colours.yellow+input_message+_Colours.reset
            input_msg = getpass(prompt=message)
            return input_msg
                    

        def Integer(input_message:str=None) -> int:
            
            message = _Colours.white+"[ "+_Colours.cyan+"INPUT"+_Colours.white+" ] "+_Colours.yellow+input_message+_Colours.reset
            input_msg = input(message)
            try: 
                return int(input_msg)
            except:
                Console.log.Error("Failed to convert the entered data into integer.")

        def Float(input_message:str=None) -> float:

            message = _Colours.white+"[ "+_Colours.cyan+"INPUT"+_Colours.white+" ] "+_Colours.yellow+input_message+_Colours.reset
            input_msg = input(message)
            try: 
                return float(input_msg)
            except:
                Console.log.Error("Failed to convert the entered data into float.")

        def Boolean(input_message:str=None) -> bool:
            message = _Colours.white+"[ "+_Colours.cyan+"INPUT"+_Colours.white+" ] "+_Colours.yellow+input_message+"(Y/n): "+_Colours.reset
            while True:
                input_msg = input(message)
                if not input_msg: continue
                if str(input_msg).lower() == "y" or str(input_msg).lower() == "yes": return True
                if str(input_msg).lower() == "n" or str(input_msg).lower() == "no": return False
                else: 
                    Console.log.Error("Invalid input type.") 
                    continue       