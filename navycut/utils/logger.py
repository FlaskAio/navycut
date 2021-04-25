from .colours import _Colours

class Console:
    class log:
        def Success(message:str=None) -> str:
            print (_Colours.white+'[ '+_Colours.green+_Colours.bright+'SUCCESS'+_Colours.reset+_Colours.white+' ] '+_Colours.yellow+message+_Colours.reset)
        def Error(message:str=None) -> str:
            print (_Colours.white+'[ '+_Colours.red+_Colours.bright+'ERROR'+_Colours.reset+_Colours.white+' ] '+_Colours.yellow+message+_Colours.reset)
        def Info(message:str=None) -> str:
            def _print(message_) -> None:
                print (_Colours.white+'[ '+_Colours.blue+_Colours.bright+'INFO'+_Colours.reset+_Colours.white+' ] '+_Colours.yellow+message_+_Colours.reset)
            # _print(_message) if for _message in message.split("\n")
            if "\n" in message:
                message_line_list:list = message.split("\n")
                for _message in message_line_list: _print(_message)
            else: _print(message)
        def Warning(message:str=None) -> str:
            print (_Colours.white+'[ '+_Colours.magenta+_Colours.bright+'WARNING'+_Colours.reset+_Colours.white+' ] '+_Colours.yellow+message+_Colours.reset)        