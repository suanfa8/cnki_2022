from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.keys import Keys

import time


def driver_init():
    global driver
    # 设置浏览器不关闭 begin
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    # 设置浏览器不关闭 end
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    # 全局设置
    driver.implicitly_wait(5)


def login():
    login_btn = driver.find_element(By.XPATH, '//*[@id="Ecp_top_login"]/a')
    login_btn.click()
    time.sleep(1)

    user_input = driver.find_element(By.XPATH, '//*[@id="Ecp_TextBoxUserName"]')
    user_input.send_keys("zying1998@163.com")

    password_input = driver.find_element(By.XPATH, '//*[@id="Ecp_TextBoxPwd"]')
    password_input.send_keys('xwa123456@')

    login_submit_btn = driver.find_element(By.XPATH, '//*[@id="Ecp_Button1"]')
    login_submit_btn.click()


def click_newspaper_tab():
    newspaper_a = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div/ul[1]/li[4]/a')
    newspaper_a.click()


if __name__ == '__main__':
    driver_init()

    root_url = 'https://www.cnki.net/'
    driver.get(url=root_url)

    login()

    # 找到「高级搜索」按钮，并点击
    high_search_button = driver.find_element(By.XPATH, '//*[@id="highSearch"]')
    high_search_button.click()
    # 切换到最新打开的窗口

    # 搜索主页，这一页很重要
    search_page = driver.window_handles[-1]
    driver.switch_to.window(search_page)

    # 第 1 步：点击「报纸」选项卡
    click_newspaper_tab()
    # 这一步很重要，要让页面加载完
    time.sleep(1)

    # 第 2 步：选项卡 1 选择「全文」
    # 因为「选项卡 1」的样式是 display: none; ，需要使用 js 让它全部显示出来
    js = 'document.querySelector("#gradetxt > dd:nth-child(2) > div.input-box > div.sort.reopt > ' \
         'div.sort-list").style.display="block" '
    driver.execute_script(js)
    time.sleep(1)

    quan_wen_a_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="gradetxt"]/dd[1]/div[2]/div[1]/div[2]/ul/li[5]/a')))
    print("下拉框 1 选择了", quan_wen_a_link.text)
    # 需要点击两下
    quan_wen_a_link.click()
    time.sleep(1)
    quan_wen_a_link.click()

    # 第 3 步：选项卡 2 选择「全文」
    js2 = 'document.querySelector("#gradetxt > dd:nth-child(3) > div.input-box > div.sort.reopt > ' \
          'div.sort-list").style.display="block"'
    driver.execute_script(js2)
    time.sleep(1)

    quan_wen_a_link2 = driver.find_element(By.XPATH, '//*[@id="gradetxt"]/dd[2]/div[2]/div[1]/div[2]/ul/li[5]/a')
    print("下拉框 2 选择了", quan_wen_a_link2.text)
    quan_wen_a_link2.click()
    time.sleep(1)
    quan_wen_a_link2.click()

    # 第 4 步：默认就是 「AND」

    # 第 5 步：文本框 1 里写入「小米」
    input1 = driver.find_element(By.XPATH, '//*[@id="gradetxt"]/dd[1]/div[2]/input')
    input1.send_keys("小米")

    # 第 6 步：文本框 2 里写入「小米」
    input2 = driver.find_element(By.XPATH, '//*[@id="gradetxt"]/dd[2]/div[2]/input')
    input2.send_keys("危机")

    # 第 7 步：点击「搜索」按钮
    search_button = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/input')
    search_button.click()

    rows = driver.find_elements(By.XPATH, '//*[@id="gridTable"]/table/tbody/tr')
    print(len(rows))

    js3 = 'document.querySelector("#perPageDiv > ul").style.display="block" '
    driver.execute_script(js3)

    page_size = driver.find_element(By.XPATH, '//*[@id="perPageDiv"]/ul/li[3]/a')

    time.sleep(2)

    page_size.click()

    time.sleep(2)


    total_pages_str = driver.find_element(By.XPATH, '//*[@id="countPageDiv"]/span[2]')
    print("总页数", total_pages_str.text.split('/')[1])
    total_pages = int(total_pages_str.text.split('/')[1])

    # 12
    i = 1
    while True:
        print('爬第 ' + str(i) + ' 页的内容')
        time.sleep(1)
        i += 1

        next_page_btn = driver.find_elements(By.XPATH, '//*[@id="Page_next_top"]')
        if len(next_page_btn) == 1:
            driver.execute_script("arguments[0].click();", next_page_btn[0])
        else:
            break

    # for row in rows:
    #     article_url = row.find_element(By.CSS_SELECTOR, "td.name > a")
    #     article_url.click()
    #
    #     driver.switch_to.window(driver.window_handles[-1])
    #
    #     print("爬取文章页面的一些信息")
    #
    #     title = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[3]/div[1]/div/div[3]/div[1]/h1')
    #     print(title.text)
    #     baozhi_name = driver.find_element(By.XPATH, '//*[@id="func610"]/div/a')
    #     print(baozhi_name.text)
    #
    #     baozhi_level = driver.find_element(By.XPATH, '//*[@id="func610"]/div/span')
    #     print(baozhi_level.text)
    #     author = driver.find_element(By.XPATH, '//*[@id="authorpart"]')
    #     print(author.text)
    #     keyword = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[3]/div[1]/div/div[3]/div[4]/p')
    #
    #     report_date = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[3]/div[1]/div/div[4]/p')
    #
    #     version_name = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[3]/div[1]/div/div[5]/p')
    #
    #     version_no = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[3]/div[1]/div/div[6]/p')
    #
    #     album = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[3]/div[1]/div/div[7]/ul/li[1]/p')
    #
    #     special = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[3]/div[1]/div/div[7]/ul/li[2]/p')
    #
    #     category_no = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[3]/div[1]/div/div[7]/ul/li[4]/p')
    #
    #     time.sleep(2)
    #
    #     driver.close()
    #     print("爬取完成以后关闭")
    #
    #     driver.switch_to.window(search_page)
