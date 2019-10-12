import time
import datetime
from apscheduler.schedulers.background import BackgroundScheduler


def get_cache_instance(cache_name):
    """
    获取缓存实例
    :param cache_name: 缓存名称
    :return:
    """
    _cache = MemoryCache()
    if cache_name.lower() == 'redis':
        pass
    elif cache_name.lower() == 'default':
        _cache = MemoryCache()
    return _cache


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
        self.SEPARATOR = '@@'
        self.__dict = {}
        self.__run_job()

    def set(self, key, value, ttl=-1):
        try:
            ttl = int(ttl)
        except Exception as e:
            ttl = -1
        now_timestamp = int(time.time())
        expired = 0
        if ttl > -1:
            expired = now_timestamp + ttl
        value = '{value}{separator}{expired}'.format(value=value, expired=expired, separator=self.SEPARATOR)
        self.__dict[key] = value

    def delete(self, key):
        try:
            del self.__dict[key]
        except Exception as e:
            pass

    def get(self, key):
        try:
            value = self.__dict[key]
            value_arr = value.split(self.SEPARATOR)
            return ''.join(value_arr[:len(value_arr) - 1])
        except KeyError:
            return None

    def is_empty(self):
        return self.__dict is {}

    def size(self):
        return len(self.__dict)

    def __run_job(self):
        scheduler = BackgroundScheduler()
        scheduler.add_job(self.__work, 'interval', seconds=1, next_run_time=datetime.datetime.now())
        scheduler.start()

    def __work(self):
        for key in list(self.__dict.keys()):
            value_arr = self.__dict[key].split(self.SEPARATOR)
            expired = int(value_arr[len(value_arr) - 1])
            if expired != 0 and int(time.time()) > expired:
                self.delete(key)


if __name__ == '__main__':
    m1 = MemoryCache()
    m2 = MemoryCache()

    m1.set('x', 1, 5)
    m1.set('y', 2)
    m2.set('z', 3)

    print(m2.get('x'))
    print(m2.get('y'))
    print(m2.get('z'))
    m2.delete('x')
    print(m1.get('x'))
