class DatabaseException(Exception):
    def __init__(self, message):
        super().__init__(message)

class DatabaseNotFoundException(DatabaseException):
    def __init__(self, message):
        super().__init__(message)

class CollectionNotFoundException(DatabaseException):
    def __init__(self, message):
        super().__init__(message)