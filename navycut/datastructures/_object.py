from json import loads, dumps, decoder
from ..errors.datastructure import NCObjectDataTypeMisMatchError

class NCObject(object):
    """
    The special object of Navycut fullstack web framework.
    It's basically gives you the feel like javascript while dealing with json or dictionary.
    :param data: provide a dictionary or json data here. It supported only for json and dictionary like data object.
    example:
        from navycut.datastructure import NCObject
        data = {"name":"Jerry", "planet": "Pluto"}
        nob = NCObject(data)
        print (nob.name, nob.planet)
    """
    def __init__(self, ___=None, **kwargs): 
        if ___ is None and kwargs is not None: self.dict = kwargs
        elif ___ is not None and isinstance(___, str): 
            try:self.dict = loads(___)
            except decoder.JSONDecodeError: raise NCObjectDataTypeMisMatchError(___)
        elif ___ is not None and isinstance(___, dict) : self.dict = ___
        else: raise NCObjectDataTypeMisMatchError(___)
        self.__dict__.update({k: self.__elt(v) for k, v in self.dict.items()})

    def get(self, attr):
        """
        return the attribute value.
        :param attr: attribute name
        """
        return self.__getattribute__(attr)

    # def update(self,attr,value):
    #     setattr(self,attr,value)

    def update(self, __:dict=None, **kwargs):
        """
        update single/multiple attribute values.
        :param __:A simple dictionary object.
        :param **kwargs: the kwargs based values.
        example:
        a= NCObject({"name":"pluto"})
        print (a.name)
        a.update({"name":"mars"})
        #or simply
        a.update(name="mars")
        print (a.name)
        """
        if __ and not isinstance(__, dict): raise NCObjectDataTypeMisMatchError(__)
        if __: self.__dict__.update({k: self.__elt(v) for k, v in __.items()})
        else: self.__dict__.update({k: self.__elt(v) for k, v in kwargs.items()})

    def to_dict(self) -> dict: 
        """
        It return the equivalent dictionary value of the NCObject.
        """
        return self.__dict__.get('dict', {})

    def __elt(self, elt):
        """Recurse into elt to create leaf namespace objects"""
        if type(elt) is dict:
            return type(self)(elt)
        if type(elt) in (list, tuple):
            return [self.__elt(i) for i in elt]
        return elt

    def __repr__(self):
        """Return repr(self)."""
        return "%s(%s)" % (type(self).__name__, repr(self.__dict__))

    def __eq__(self, other):
        return self.__dict__ == other.__dict__