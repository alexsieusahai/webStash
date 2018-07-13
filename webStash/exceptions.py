
class CacheMapError(Exception):
    def __init__(self, message):
        print(message)  # should I use an enum instead?

class ImplementationError(Exception):
    def __init__(self, message):
        print(message)
        # eventually include github integration

class SerializerImplementationError(ImplementationError):
    def __init__(self, message):
        super()

class GetterImplementationError(ImplementationError):
    def __init__(self, message):
        super()
