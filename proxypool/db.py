import redis
from proxypool.error import PoolEmptyError
from proxypool.setting import HOST, PORT, PASSWORD


class RedisClient(object):
    def __init__(self, host=HOST, port=PORT):
        # 连接redis数据库
        if PASSWORD:
            self._db = redis.Redis(host=host, port=port, password=PASSWORD)
        else:
            self._db = redis.Redis(host=host, port=port)

    def get(self, count=1):
        """
        get proxies from redis
        从左侧批量获取redis数据库中的代理ip信息
        """
        proxies = self._db.lrange("proxies", 0, count - 1)
        self._db.ltrim("proxies", count, -1)
        return proxies

    def put(self, proxy):
        """
        add proxy to right top
        将数据插入右侧
        """
        self._db.rpush("proxies", proxy)

    def pop(self):
        """
        get proxy from right.
        从右侧拿出代理 供使用
        """
        try:
            return self._db.rpop("proxies").decode('utf-8')
        except:
            raise PoolEmptyError

    def srand(self, num):
    try:
        # num = random.randint(int(int(num)/1.5), num)
        num = random.randint(1, num)
        print(num)
        return self._db.lindex('proxies', num)
    except:
        raise PoolEmptyError

    @property
    def queue_len(self):
        """
        get length from queue.
        获取队列长度
        """
        return self._db.llen("proxies")

    def flush(self):
        """
        flush db
        刷新整个队列
        """
        self._db.flushall()


if __name__ == '__main__':
    conn = RedisClient()
    print(conn.pop())
