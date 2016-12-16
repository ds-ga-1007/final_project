class InteractionError(Exception):
    pass


class MissingHeadersError(InteractionError):
    """Raised when unable to read header file."""

    def __init__(self):
        pass

    def __str__(self):
        return "Unable to read header file `headers.txt`! " \
               "Make sure you're working from the `dov205` directory and try again."


class MissingDatasetError(InteractionError):
    """Raised when unable to read data file."""

    def __init__(self, filename):
        self.filename = filename

    def __str__(self):
        return "Unable to read data file `{}`! " \
               "Make sure you're working from the `dov205 directory and try again.".format(self.filename)