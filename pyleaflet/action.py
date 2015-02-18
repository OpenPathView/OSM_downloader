NOACTION         =-1


class Action():
    """
    define an action
    """

    def __init__(self, actionId = NOACTION, **kwargs):
        """
        init the action and its component
        """

        self.actionId = actionId
        for key, value in kwargs.items():   #load wanted attribute
            setattr(self, key, value)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "<Action("+", "+", ".join("%s = %s"%(key,value) for key,value in self.__dict__.items())+")>"