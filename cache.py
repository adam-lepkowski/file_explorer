class Cache:
    """
    Cache actions.

    Attributes
    ---------------
    items : list
        cached actions
    current : int
        index pointing at current action
    """

    def __init__(self):
        """
        Cache constructor.
        """

        self.items = []
        self.current = -1
