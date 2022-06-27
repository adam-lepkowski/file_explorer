class Cache:

    def __init__(self):
        """
        Cache actions.

        Attributes
        ---------------
        actions : list
            cached actions
        current : dict
            action to be performed
        """
        
        self.actions = []
        self.current = {}
