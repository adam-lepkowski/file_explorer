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
        """
        Undo an action if there is more than one stored.
        """

        if self.current > 0:
            self.current -= 1

    def redo(self):
        """
        Redo an action if current is not pointing at the last action.
        """

        if self.current < len(self.items) - 1:
            self.current += 1

    def get_current(self):
        """
        Return action pointed by current.

        Returns
        ---------------
        Object stored in items
        OR
        None
        """

        if self.items:
            return self.items[self.current]
        return None
