import time

import pandas as pd
from selenium.webdriver.common.by import By

from utils.crawler import driver_init
from utils.crawler import login
from utils.crawler import set_search_criteria
from utils.crawler import change_page_size
from utils.crawler import crawler_one_page

if __name__ == '__main__':
    username = "zying1998@163.com"
    password = 'xwa123456@'
    root_url = 'https://www.cnki.net/'

    global driver
    driver = driver_init()
    driver.get(url=root_url)

    login(driver, username, password)

    high_search_button = driver.find_element(By.XPATH, '//*[@id="highSearch"]')
    high_search_button.click()
    search_homepage = driver.window_handles[-1]
    driver.switch_to.window(search_homepage)

    set_search_criteria(driver)

    change_page_size(driver)

    total_pages_str = driver.find_element(By.XPATH, '//*[@id="countPageDiv"]/span[2]')
    total_pages = int(total_pages_str.text.split('/')[1])
    print("总页数", total_pages)

    # 当前第几页
    current_page = 1
    # 保存结果的表格
    df = pd.DataFrame()
    try:
        while True:
            time.sleep(2)
            print("正在爬第 " + str(current_page) + " 页的数据")
            rows = driver.find_elements(By.XPATH, '//*[@id="gridTable"]/table/tbody/tr')
            time.sleep(2)

            row_no, df = crawler_one_page(driver, search_homepage, rows, df)

            # 测试
            if current_page == 2:
                break

            current_page += 1

            # 如果找不到「下一页」，就停止爬取
            next_page_btn = driver.find_elements(By.XPATH, '//*[@id="Page_next_top"]')
            if len(next_page_btn) == 1:
                driver.execute_script("arguments[0].click();", next_page_btn[0])
            else:
                break
    except Exception as ex:
        # 出现异常的时候，把已经爬好的结果存起来
        print(ex)
        df.to_excel('cnki.xlsx', sheet_name='cnki', index=False)
    df.to_excel('cnki.xlsx', sheet_name='cnki', index=False)
