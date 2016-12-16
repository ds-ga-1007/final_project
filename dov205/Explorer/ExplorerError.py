class ExplorerError(Exception):
    pass


class InvalidActionError(ExplorerError):
    """Raised when user provides an invalid action."""

    def __init__(self, action):
        self.action = action

    def __str__(self):
        return "\n* Error: Cannot perform provided action `{}`. " \
               "Please try again with a valid action. *".format(self.action)


class InvalidFeatureError(ExplorerError):
    """Raised when user provides an invalid feature to perform action."""

    def __init__(self, feature):
        self.feature = feature

    def __str__(self):
        return "\n* Error: Cannot perform action on provided feature `{}`. \n" \
               "Please specify a valid feature or leave blank (when possible) to \n" \
               "apply onto entire data set. *".format(self.feature)


class InvalidGroupbyFeature(ExplorerError):
    """Raised when user provides an invalid feature to GropuBy."""

    def __init__(self, feature):
        self.feature = feature

    def __str__(self):
        return "\n* Error: Invalid groupby feature `{}`. You must " \
               "pair :groupby with a different feature and function to return safely. *".format(self.feature)


class InvalidGroupbyCombinator(ExplorerError):
    """Raised when user provides an invalid aggregator to GroupBy."""

    def __init__(self, combinator):
        self.combinator = combinator

    def __str__(self):
        return "\n* Error: Invalid groupby combinator `{}`. You must " \
               "pair :groupby with another feature and function to return safely. *".format(self.combinator)