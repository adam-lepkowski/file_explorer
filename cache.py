class Cache:

    def __init__(self):
        """
        Cache actions.

        Attributes
        ---------------
        actions : list
            cached actions
        current : int
            index pointing at current action
        """

        self._actions = []
        self._current = -1
