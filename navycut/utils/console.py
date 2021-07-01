import logging
from .colours import colours
from getpass import getpass
import logging

class Console:
    class log:
        def Success(message:str=None) -> str:
            print (colours.white+'[ '+colours.green+colours.bright+'SUCCESS'+colours.reset+colours.white+' ] '+colours.yellow+message+colours.reset)
        
        def Error(message:str=None) -> str:
            print (colours.white+'[ '+colours.red+colours.bright+'ERROR'+colours.reset+colours.white+' ] '+colours.yellow+message+colours.reset)
        
        def Info(message:str=None) -> str:
            def _print(message_) -> None:
                print (colours.white+'[ '+colours.blue+colours.bright+'INFO'+colours.reset+colours.white+' ] '+colours.yellow+message_+colours.reset)
            if "\n" in message:
                message_line_list:list = message.split("\n")
                for _message in message_line_list: _print(_message)
            else: _print(message)
        
        def Warning(message:str=None) -> str:
            print (colours.white+'[ '+colours.magenta+colours.bright+'WARNING'+colours.reset+colours.white+' ] '+colours.yellow+message+colours.reset) 

    class input:
        def String(input_message:str=None) -> str:
            
            message = colours.white+"[ "+colours.cyan+"INPUT"+colours.white+" ] "+colours.yellow+input_message+colours.reset
            input_msg = input(message)
            try: 
                return str(input_msg)
            except: Console.log.Error("Failed to convert into string.")
                
        def Password(input_message:str=None) -> str:
            
            message = colours.white+"[ "+colours.cyan+"INPUT"+colours.white+" ] "+colours.yellow+input_message+colours.reset
            input_msg = getpass(prompt=message)
            return input_msg
                    

        def Integer(input_message:str=None) -> int:
            
            message = colours.white+"[ "+colours.cyan+"INPUT"+colours.white+" ] "+colours.yellow+input_message+colours.reset
            input_msg = input(message)
            try: 
                return int(input_msg)
            except:
                Console.log.Error("Failed to convert the entered data into integer.")

        def Float(input_message:str=None) -> float:

            message = colours.white+"[ "+colours.cyan+"INPUT"+colours.white+" ] "+colours.yellow+input_message+colours.reset
            input_msg = input(message)
            try: 
                return float(input_msg)
            except:
                Console.log.Error("Failed to convert the entered data into float.")

        def Boolean(input_message:str=None) -> bool:
            message = colours.white+"[ "+colours.cyan+"INPUT"+colours.white+" ] "+colours.yellow+input_message+"(Y/n): "+colours.reset
            while True:
                input_msg = input(message)
                if not input_msg: continue
                if str(input_msg).lower() == "y" or str(input_msg).lower() == "yes": return True
                if str(input_msg).lower() == "n" or str(input_msg).lower() == "no": return False
                else: 
                    Console.log.Error("Invalid input type.") 
                    continue       