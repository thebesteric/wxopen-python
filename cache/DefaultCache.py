def singleton(cls):
    _instance = {}

    def _singleton(*args, **kwargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwargs)
        return _instance[cls]

    return _singleton


@singleton
class MemoryCache:

    def __init__(self):
        self.__dict = {}
        self.ACCESS_TOKEN = 'access_token'

    def set(self, key, value):
        self.__dict[key] = value

    def delete(self, key):
        del self.__dict[key]

    def get(self, key):
        try:
            return self.__dict[key]
        except KeyError:
            return None

    def is_empty(self):
        return self.__dict is {}

    def size(self):
        return len(self.__dict)


if __name__ == '__main__':
    m1 = MemoryCache()
    m2 = MemoryCache()

    m1.set('x', 1)
    m1.set('y', 2)
    m2.set('z', 3)

    print(m2.get('x'))
    print(m2.get('y'))
    print(m2.get('z'))
    m2.delete('x')
    print(m1.get('x'))
