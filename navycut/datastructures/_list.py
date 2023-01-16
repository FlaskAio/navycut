class List(list):
    """
    list enhancements
    """
    def __init__(self,*args) -> None:
        elems = list(args)
        # for index, item in enumerate(elems):
        #     if isinstance(item, list):
        #         elems.insert(index, List(*tuple(item)))
        super().__init__(elems)

    def push(self, item) -> None:
        """
        to append a item to the end of the list.
        """
        self.append(item)

    def to_string(self) -> str:
        """
        convert a list to a string.
        """
        new_list = []
        for item in self:
            if isinstance(item, self.__class__):
                new_list.append(item.to_string())
            else:
                try:
                    new_list.append(str(item))
                except Exception:
                    new_list.append(repr(item))
                
        return ','.join(new_list)