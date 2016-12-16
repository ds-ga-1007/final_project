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


class InvalidFeatureRequest(InteractionError):
    """Raised when user requests feature does not exist in source dataset."""

    def __init__(self, request):
        self.request = request

    def __str__(self):
        return "\n* Warning: feature `{}` not found in source dataset. " \
               "Not added to request list. *".format(self.request)


class RedundantFeatureRequest(InteractionError):
    """Raised when user requests feature that has already been requested."""

    def __init__(self, request):
        self.request = request

    def __str__(self):
        return "\n* Warning: You've already requested feature `{}`. " \
               "Not added to request list. *".format(self.request)


class UserExitError(InteractionError):
    """Raised when the user asks to exit the process."""

    def __init__(self):
        pass

    def __str__(self):
        return "Exiting..."


class InvalidContinuityResponse(InteractionError):
    """Referenced when user enters a continuation not considered valid."""

    def __init__(self):
        pass

    def __str__(self):
        return "\nPlease enter one of: 'y', 'n', 'yes', 'no'."
