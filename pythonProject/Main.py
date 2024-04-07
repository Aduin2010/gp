from Spider_thread import sprider_thread
from ip_pool import get_ip_list


job_type = input('工作类型: ')
infor_page = input('爬取的数量: ')

# i = 1

thread = sprider_thread(job_type, infor_page)


