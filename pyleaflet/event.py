NOEVENT         =-1
QUIT            =0
KEYDOWN         =1
KEYUP           =2
MOUSEMOTION     =3
MOUSEBUTTONUP   =4
MOUSEBUTTONDOWN =5

# QUIT             none
# KEYDOWN          unicode, key, mod, center, visible
# KEYUP            key, mod, center, visible
# MOUSEMOTION      pos, rel, buttons, center, visible
# MOUSEBUTTONUP    pos, button, center, visible
# MOUSEBUTTONDOWN  pos, button, center, visible


class Event():
    """
    define an event
    """

    def __init__(self, eventId = NOEVENT, **kwargs):
        """
        init the event and its component
        """

        self.eventId = eventId
        for key, value in kwargs.items():   #load wanted attribute
            setattr(self, key, value)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "<Event("+", ".join("%s = %s"%(key,value) for key,value in self.__dict__.items())+")>"