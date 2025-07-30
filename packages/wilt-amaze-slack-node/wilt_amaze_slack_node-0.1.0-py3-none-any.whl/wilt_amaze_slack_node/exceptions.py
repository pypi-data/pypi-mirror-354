class TreeException(Exception):
    # Would be nice to be able to draw an ascii diagram or something?
    def __init__(self, message, *args:object) -> None:
        self.message = message
        super().__init__(*args)

class InsertError(TreeException):
    pass

class CircularError(TreeException):
    # TODO: Show which node connection is raising the circular error
    def __init__(self, message="", *args: object) -> None:
        super().__init__(message, *args)