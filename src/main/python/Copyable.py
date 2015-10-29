class Copyable:
    def __init__(self): pass

    def copy(self, **kwargs):
        """
        create a shallow copy of this class. fields already present in the class can be updated with the kwargs argument
        """
        instanceKeys = dict((key, value) for key, value in self.__dict__.iteritems() if not callable(value) and not key.startswith('__'))
        if all(key in instanceKeys for key in kwargs):
            copy = Empty()
            copy.__class__ = self.__class__
            for key, value in instanceKeys.iteritems():
                if key not in kwargs:
                    copy.__dict__[key] = value
                else:
                    copy.__dict__[key] = kwargs[key]
            return copy
        else:
            raise AttributeError("could not copy object with the given kwargs")


class Empty():
    pass