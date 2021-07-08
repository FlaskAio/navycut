from .colours import colours
from getpass import getpass
import click as c


class _logger:

    @classmethod
    def _open_box(cls, **options) ->str:
        return c.style("[ ", fg="white", bold=True)

    @classmethod
    def _close_box(cls, **options) -> str:
        options.setdefault("fg", "white")
        options.setdefault("bold", True)
        return c.style(" ] ", **options)

    @classmethod
    def _create_log_base_msg(cls, type:str, **options):

        colour:str = "blue" 

        if options.get("colour", None) is None:

            if type.lower() == "info":
                colour = "blue"
            
            elif type.lower() == "warning":
                colour = "magenta"
            
            elif type.lower() == "success":
                colour = "green"

            elif type.lower() == "error":
                colour = "red"

        else:
            colour = options.get("colour")

        options.setdefault("fg", colour)
        options.setdefault("bold", True)
        return c.style(type.upper(), **options)

    @classmethod
    def _message(cls, msg:str, **options):
        options.setdefault("fg", "yellow")
        return c.style(msg, **options)

class Console:


    class log:

        _logger_class = _logger

        @classmethod
        def _clogger(cls, type:str, message_:str) -> None:
                c.echo(cls._logger_class._open_box()+\
                        cls._logger_class._create_log_base_msg(type)+\
                            cls._logger_class._close_box()+\
                                cls._logger_class._message(message_))

        @classmethod
        def Success(cls, message:str=None) -> str:
            if "\n" in message:
                message_line_list:list = message.split("\n")
                for _message in message_line_list: cls._clogger("success", _message)
            else: cls._clogger("success", message)
        
        @classmethod
        def Error(cls, message:str=None) -> str:
            if "\n" in message:
                message_line_list:list = message.split("\n")
                for _message in message_line_list: cls._clogger("error", _message)
            else: cls._clogger("error", message)
        
        @classmethod
        def Info(cls, message:str=None) -> str:
            if "\n" in message:
                message_line_list:list = message.split("\n")
                for _message in message_line_list: cls._clogger("info", _message)
            else: cls._clogger("info", message)
        
        @classmethod
        def Warning(cls, message:str=None) -> str:
            if "\n" in message:
                message_line_list:list = message.split("\n")
                for _message in message_line_list: cls._clogger("warning", _message)
            else: cls._clogger("warning", message)

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