
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

if __name__ == "__main__":
    try:
        raise SerializerImplementationError('test')
    except Exception as e:
        print(e)
        try:
            raise CacheMapError('cache map test')
        except Exception as e:
            a = 1
