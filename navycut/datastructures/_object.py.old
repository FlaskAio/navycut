from json import loads, dumps, decoder
import typing as t
from ..errors.datastructure import NCObjectDataTypeMisMatchError

class NCObject(object):
    """
    The special object of Navycut fullstack web framework.
    It's basically gives you the feel like javascript while dealing with json or dictionary.

    :param *wargs: provide a dictionary or json data here. It supported only for json and dictionary like data object.
    :param **kwargs: the kwargs based value.

    :example::
        from navycut.datastructure import NCObject
        data = {"name":"Jerry", "planet": "Pluto"}
        nob = NCObject(data)
        print (nob.name, nob.planet)
    """

    def __init__(self, *wargs, **kwargs):
        
        if not len(wargs) and kwargs is not None:
            self.dict = kwargs
        
        elif len(wargs) is not None and isinstance(wargs[0], str):
            try:
                self.dict = loads(wargs[0])
            except decoder.JSONDecodeError:
                raise NCObjectDataTypeMisMatchError(wargs[0])
            except Exception as e:
                raise Exception("something went wrong.\nError: "+e)
        
        elif len(wargs) is not None and isinstance(wargs[0], dict): 
            self.dict = wargs[0]

        else:
            raise NCObjectDataTypeMisMatchError(wargs[0])

        self.__dict__.update({k: self.__elt(v) for k, v in self.dict.items()})

    def get(self, attr) ->t.Any:
        """
        return the attribute value.
        :param attr: attribute name
        """
        return self.__getattribute__(attr)

    def update(self, *wargs, **kwargs):
        """
        update single/multiple attribute values.
        :param *wargs:A simple dictionary object.
        :param **kwargs: the kwargs based values.
        :example::
            a= NCObject({"name":"pluto"})
            print (a.name)
            a.update({"name":"mars"})
            #or simply
            a.update(name="mars")
            print (a.name)
        """
        if len(wargs) and not isinstance(wargs[0], dict): 
            raise NCObjectDataTypeMisMatchError(wargs[0])

        if len(wargs): 
            self.__dict__.update({k: self.__elt(v) for k, v in wargs[0].items()})
            
        else: 
            self.__dict__.update({k: self.__elt(v) for k, v in kwargs.items()})

    def _convert_to_dict(self, obj):
            _dict = obj.__dict__
            _dict.pop('dict')
            for key, value in _dict.items():
                if isinstance(value, NCObject):
                    _dict.update({key:self._convert_to_dict(value)})
            return _dict
    
    def to_dict(self) -> dict: 
        """
        It return the equivalent dictionary value of the NCObject.
        """

        return self._convert_to_dict(self)

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