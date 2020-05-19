class FrankiException(Exception):
    pass


class FrankiInvalidFormatException(Exception):
    pass


class FrankiFileNotFound(Exception):
    pass


class FrankiInvalidFileFormat(Exception):
    pass


__all__ = ("FrankiInvalidFormatException", "FrankiFileNotFound",
           "FrankiInvalidFileFormat", "FrankiException")
