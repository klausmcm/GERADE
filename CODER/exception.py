class CapacityError(Exception):
    def __init__(self, msg=None):
        if msg is None:
            msg = "Capacity Error"
        super().__init__(msg)
