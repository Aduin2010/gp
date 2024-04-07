import threading
from spider import my_spider
from Redis import redis_client

def sprider_thread(type, page):
    """
    :param type:工作类型
    :param page: 为该线程分配的页数,也即线程数量
    :return: none
    """
    ### 创建线程 ###
    for i in range(1, int(page)+1):
        # print(i)
        infor_thread = threading.Thread(target=my_spider, args=(type, i))
        infor_thread.name = "爬虫线程-->%d" % i
        infor_thread.start()
        ### 等待线程运行完成 ###
        infor_thread.join()


### 并发运行所有线程 ###
def sprider_thread_2(type, page):
    """
    参数同sprider_thread
    并发运行线程
    """
    threads_list = []
    ### 创建线程 ###
    for i in range(1, int(page) + 1):
        # print(i)
        infor_thread = threading.Thread(target=my_spider, args=(type, i))
        infor_thread.name = "爬虫线程-->%d" % i
        infor_thread.start()
        threads_list.append(infor_thread)

    ### 等待所有线程运行完成 ###
    for infor_thread in threads_list:
        infor_thread.join()


if __name__ == '__main__':
    type = 'java'
    page = 1

    sprider_thread(type=type, page=page)
