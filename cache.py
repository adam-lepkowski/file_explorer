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

    def store(self, item):
        """
        Store an item.

        Parameters
        ---------------
        item
            object to be stored
        """

        if self.current != len(self.items) - 1:
            self.items = self.items[:self.current + 1]
        self.items.append(item)
        self.current += 1

    def undo(self):
        if self.current > 0:
            self.current -= 1

    def redo(self):
        if self.current < len(self.items) - 1:
            self.current += 1
