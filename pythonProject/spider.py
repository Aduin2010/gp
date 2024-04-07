import threading
import time
from chaojiying import *
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.edge.options import Options
from Redis import *
from ip_pool import get_ip_list


def my_spider(job_type, page):

    """
    :param job_type:工作类型
    :param page: 爬取的页数
    :return: job_infor包含-工作名称，工作地点，公司名字，薪资待遇 的类
    """
    ### 代理ip池 ###
    a = get_ip_list(int(page))

    ### 无头浏览器 ###
    opt = Options()
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0'
    opt.add_argument('--headless')
    opt.add_argument('--disable-gpu')
    opt.add_argument(f'user-agent={user_agent}')
    # opt.add_argument('--proxy-server=http://%s' % a)
    driver = webdriver.Edge(options=opt)

    # driver = webdriver.Edge()
    try:
        driver.get(f"https://www.zhipin.com/web/geek/job?query={job_type}&page={page}")
        # driver.get(f"https://www.zhipin.com/web/user/safe/verify-slider")
        time.sleep(9)

        ### 判断是否需要输入验证码 ###
        if driver.current_url == "https://www.zhipin.com/web/user/safe/verify-slider":
            driver.find_element(By.CLASS_NAME, "btn").click()
            time.sleep(9)
            # wait = WebDriverWait(driver, 10)
            # img = wait.until()
            ### 对接打码平台 ###
            img = driver.find_element(By.CLASS_NAME, "geetest_item_wrap")
            img.screenshot('yzm.png')
            im = open('yzm.png', 'rb').read()

            chaojiying = Chaojiying_Client('125349224', '125349224s9ns9p', '958791')
            pic_str = chaojiying.PostPic(im, 9004)['pic_str']
            for index in pic_str.split('|'):
                x = index.split(',')[0]
                y = index.split(',')[1]
                action = ActionChains(driver)
                action.move_to_element_with_offset(img, int(x), int(y)).click().perform()
            driver.find_element(By.CLASS_NAME, "geetest_commit").click()
            time.sleep(5)

            ### 验证成功后跳转后再次对job_type进行搜索 ###
            driver.find_element(By.CSS_SELECTOR, "ipt-search").send_keys(f"{job_type}")
            driver.find_element(By.CSS_SELECTOR, "btn btn-search").click()

        ### 获取信息 ###
        content = driver.page_source
        soup = BeautifulSoup(content, 'html.parser')

        ### 查找工作名字和地点 ###
        job_area = soup.findAll('span', attrs={'class': 'job-area-wrapper'})
        job_name = soup.findAll('span', attrs={'class': 'job-name'})
        job_salary = soup.findAll('span', attrs={'class': "salary"})
        job_infor = soup.findAll('h3', attrs={'class': 'company-name'})

        ### company_name数据格式与其他数据不同，对其进行处理 ###
        job_company = []
        for company in job_infor:
            company_name = company.findAll('a', attrs={'target': '_blank'})
            job_company.extend(company_name)

        ### 连接数据库,存放数据 ###
        redis_conf = redis_client()

        No = (page-1)*30
        i = 0
        while i < len(job_infor):
            area = job_area[i].string
            name = job_name[i].string
            salary = job_salary[i].string
            company = job_company[i].string

            redis_conf.hset(f'{i + No}.{company}', '公司名字', company)
            redis_conf.hset(f'{i + No}.{company}', '工作地点', area)
            redis_conf.hset(f'{i + No}.{company}', '工作名字', name)
            redis_conf.hset(f'{i + No}.{company}', '工作薪资', salary)

            i += 1

        print(f'当前线程:', threading.current_thread())
        print(f'当前IP{a}', '\n')


    except Exception as error:
        print(f'爬虫出现错误: {error}')


if __name__ == '__main__':

    i = '1'

    # for i in range(1, 3):
    masseage_thread = threading.Thread(target=my_spider, args=('java', int(i)))
    masseage_thread.name = "爬虫线程-->%d" % 1
    masseage_thread.start()
    # i += 1