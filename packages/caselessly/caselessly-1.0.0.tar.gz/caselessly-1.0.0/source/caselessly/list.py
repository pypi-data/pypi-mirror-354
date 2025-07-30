from caselessly.logging import logger

logger = logger.getChild(__name__)


class caselesslist(list):
    """A list subclass that doesn't consider case-sensitivity for string items."""

    def __contains__(self, item: object) -> bool:
        # logger.debug("%s.__contains__(item: %s) %s" % (self.__class__.__name__, item, self))

        if isinstance(item, str):
            _item = item.casefold()

            for item in self:
                if isinstance(item, str):
                    if item.casefold() == _item:
                        return True

            return False
        else:
            return super().__contains__(item)

    def __eq__(self, other: list) -> bool:
        if not isinstance(other, list):
            return False

        if len(self) != len(other):
            return False

        for index, value in enumerate(self):
            if isinstance(value, str):
                if not value.casefold() == other[index].casefold():
                    return False
            else:
                if not value == other[index]:
                    return False

        return True


# Shorthand alias
cilist = caselesslist
