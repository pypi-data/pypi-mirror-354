"""A module that provides a class to mimic slice behavior."""


class MakeSlice:
    """A class that returns the item itself when called, mimicking a slice object."""

    def __getitem__(self, item: slice) -> slice:
        """Mimics the behavior of a slice object by returning the item itself."""
        return item


make_slice = MakeSlice()
