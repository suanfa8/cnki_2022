import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


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


def set_search_criteria():
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


if __name__ == '__main__':
    driver_init()
    root_url = 'https://www.cnki.net/'
    driver.get(url=root_url)
    login()
    # 找到「高级搜索」按钮，并点击
    high_search_button = driver.find_element(By.XPATH, '//*[@id="highSearch"]')
    high_search_button.click()

    # 搜索主页，这一页很重要
    search_homepage = driver.window_handles[-1]
    # 切换到最新打开的窗口
    driver.switch_to.window(search_homepage)

    # 设置搜索条件
    set_search_criteria()

    time.sleep(1)

    # 设置每一页显示 50 条数据 begin
    # js3 = 'document.querySelector("#perPageDiv > ul").style.display="block" '
    # driver.execute_script(js3)
    # # li[3] 表示第 3 个选项，即每页 50 条数据
    # page_size = driver.find_element(By.XPATH, '//*[@id="perPageDiv"]/ul/li[3]/a')
    # time.sleep(2)
    # page_size.click()
    # # 等待数据加载
    # time.sleep(2)
    # 设置每一页显示 50 条数据 end

    total_pages_str = driver.find_element(By.XPATH, '//*[@id="countPageDiv"]/span[2]')
    total_pages = int(total_pages_str.text.split('/')[1])
    print("总页数", total_pages)

    df = pd.DataFrame()
    current_page = 1
    index = 1
    while True:
        print('爬第 ' + str(current_page) + ' 页的内容')
        rows = driver.find_elements(By.XPATH, '//*[@id="gridTable"]/table/tbody/tr')

        # 爬取具体的网页内容 begin
        for row in rows:
            index += 1
            item = dict()

            article_url = row.find_element(By.CSS_SELECTOR, "td.name > a")
            article_url.click()

            driver.switch_to.window(driver.window_handles[-1])

            print("爬取文章页面的一些信息")
            # 1 标题
            title = driver.find_element(By.CSS_SELECTOR, 'body > div.wrapper > div.main > div.container > div.doc > '
                                                         'div > div.brief > div.wx-tit > h1')
            print("1 标题", title.text)
            item['title'] = title.text

            # 2 正文 todo

            # 3 报纸名
            newspaper_name = driver.find_element(By.XPATH, '//*[@id="func610"]/div/a')
            print("3 newspaper_name", newspaper_name.text)
            item['newspaper_name'] = newspaper_name.text

            # 4 报纸级别
            newspaper_level = driver.find_element(By.XPATH, '//*[@id="func610"]/div/span')
            print("4 报纸级别", newspaper_level.text)
            item['newspaper_level'] = newspaper_level.text

            # 5 作者名
            author = driver.find_element(By.XPATH, '//*[@id="authorpart"]')
            print("5 作者名", author.text)
            item['author'] = author.text

            keyword = driver.find_element(By.CSS_SELECTOR, 'p.keywords')
            # 6 关键词
            print("6 关键词", keyword.text)
            item['keyword'] = keyword.text

            # 7、8、9
            other_info = driver.find_elements(By.CSS_SELECTOR, 'div.doc-top > div.row')
            for r in other_info:
                key = r.find_element(By.TAG_NAME, 'span').text
                value = r.find_element(By.TAG_NAME, 'p').text
                if '报纸日期：' == key:
                    item['publish_data'] = value
                if '版名：' == key:
                    item['version_name'] = value
                if '版号：' == key:
                    item['version_no'] = value

            other_info2 = driver.find_elements(By.CSS_SELECTOR, 'div.doc-top li.top-space')
            for r in other_info2:
                key = r.find_element(By.TAG_NAME, 'span').text
                value = r.find_element(By.TAG_NAME, 'p').text
                if '专辑：' == key:
                    item['album'] = value
                if '专题：' == key:
                    item['special'] = value
                if '分类号：' == key:
                    item['category_no'] = value

            time.sleep(2)

            driver.close()
            print("爬取完成以后关闭")
            driver.switch_to.window(search_homepage)
            df = pd.concat([df, pd.Series(item).to_frame().T], ignore_index=True)

            if index == 8:
                break

        # 爬取具体的网页内容 end

        # 每爬取一页休息 2 秒
        time.sleep(2)
        current_page += 1

        # 测试的时候爬 2 页
        if current_page == 2:
            break

        next_page_btn = driver.find_elements(By.XPATH, '//*[@id="Page_next_top"]')
        if len(next_page_btn) == 1:
            driver.execute_script("arguments[0].click();", next_page_btn[0])
        else:
            break

    df.to_excel('cnki.xlsx', sheet_name='cnki')
