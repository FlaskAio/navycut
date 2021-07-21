from munch import Munch, munchify

class NCObject(Munch):
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
    def __init__(self, *args, **kwargs):
        super(NCObject, self).__init__(*args, **kwargs)
        self.update(munchify(self))
    
    def to_dict(self):
        """
        Recursively converts a NCObject back into a dictionary.
        >>> b = NCObject(foo=NCObject(lol=True), hello=42, ponies='are pretty!')
        >>> sorted(b.to_dict().items())
        [('foo', {'lol': True}), ('hello', 42), ('ponies', 'are pretty!')]
        """
        return self.toDict()

    def to_json(self):
        return self.toJSON()