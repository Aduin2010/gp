from redis import *

def redis_client():
    """
    连接数据库
    :return: 数据库对象
    """
    try:
        redis_config = {
            'host': '127.0.0.1',
            'port': '6379',
            'db': 0,
        }

        sr = Redis(
            host=redis_config['host'],
            port=redis_config['port'],
            db=redis_config['db'],
        )
        return sr

    except Exception as e:
        print(e)

def clean_all(sr):
    for key in sr.keys():
        sr.delete(key)

if __name__ == '__main__':

    sr = redis_client()
    clean_all(sr)

