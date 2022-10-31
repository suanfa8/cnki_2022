from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import pandas as pd


def driver_init():
    """
    初始化
    :return:
    """
    # 设置浏览器不关闭 begin
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    # 设置浏览器不关闭 end
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    # 全局设置
    driver.implicitly_wait(5)
    return driver


def login(driver, username, password):
    """
    登录
    :param driver:
    :param username:
    :param password:
    :return:
    """
    login_btn = driver.find_element(By.XPATH, '//*[@id="Ecp_top_login"]/a')
    login_btn.click()
    time.sleep(1)

    user_input = driver.find_element(By.XPATH, '//*[@id="Ecp_TextBoxUserName"]')
    user_input.send_keys(username)

    password_input = driver.find_element(By.XPATH, '//*[@id="Ecp_TextBoxPwd"]')
    password_input.send_keys(password)

    login_submit_btn = driver.find_element(By.XPATH, '//*[@id="Ecp_Button1"]')
    login_submit_btn.click()


def set_search_criteria(driver):
    """
    设置搜索条件
    :param driver:
    :return:
    """
    # 第 1 步：点击「报纸」选项卡
    newspaper_a = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div/ul[1]/li[4]/a')
    newspaper_a.click()
    # 这一步很重要，要让页面加载完
    time.sleep(2)
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

    time.sleep(2)


def change_page_size(driver):
    # 设置每一页显示 50 条数据 begin
    js3 = 'document.querySelector("#perPageDiv > ul").style.display="block" '
    driver.execute_script(js3)

    # li[3] 表示第 1 个选项，即每页 10 条数据
    page_size = driver.find_element(By.XPATH, '//*[@id="perPageDiv"]/ul/li[1]/a')

    # li[3] 表示第 2 个选项，即每页 20 条数据
    # page_size = driver.find_element(By.XPATH, '//*[@id="perPageDiv"]/ul/li[2]/a')

    # li[3] 表示第 3 个选项，即每页 50 条数据
    # page_size = driver.find_element(By.XPATH, '//*[@id="perPageDiv"]/ul/li[3]/a')

    time.sleep(2)
    page_size.click()
    # 等待数据加载
    time.sleep(2)
    # 设置每一页显示 50 条数据 end


def crawler_one_page(driver, search_homepage, rows, df):
    """
    爬取具体的网页内容
    :param driver:
    :param search_homepage:
    :param rows:
    :param df:
    :return:
    """
    for row in rows:

        item = dict()

        row_no = row.find_element(By.CSS_SELECTOR, 'td.seq').text
        print("\t正在爬第 " + row_no + " 条数据")
        item['row_no'] = row_no

        time.sleep(2)

        article_url = row.find_element(By.CSS_SELECTOR, "td.name > a")
        article_url.click()

        current_window = driver.window_handles[-1]
        driver.switch_to.window(current_window)

        time.sleep(1)

        # 爬取文章页面的一些信息
        # 1 标题
        title = driver.find_element(By.CSS_SELECTOR,
                                    'body > div.wrapper > div.main > div.container > div.doc > '
                                    'div > div.brief > div.wx-tit > h1')
        item['title'] = title.text

        # 2 正文 todo （放在最后爬）

        # 3 报纸名
        newspaper_name = driver.find_element(By.XPATH, '//*[@id="func610"]/div/a')
        item['newspaper_name'] = newspaper_name.text

        # 4 报纸级别
        newspaper_level = driver.find_element(By.XPATH, '//*[@id="func610"]/div/span')
        item['newspaper_level'] = newspaper_level.text

        # 5 作者名
        author = driver.find_element(By.XPATH, '//*[@id="authorpart"]')
        item['author'] = author.text

        # 有一些文章没有关键词
        keyword = driver.find_elements(By.CSS_SELECTOR, 'p.keywords')
        if len(keyword) != 0:
            # 6 关键词
            item['keyword'] = keyword[0].text

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

        driver.find_element(By.XPATH, '//*[@id="DownLoadParts"]/div[1]/ul/li[2]/a').click()
        # 跳转到「文章详情」页面
        driver.switch_to.window(driver.window_handles[-1])

        # 这个时候到了新的页面
        free_read_btn = driver.find_elements(By.XPATH, '/html/body/div[2]/form/div/div/div[1]/input')
        if len(free_read_btn) == 1:
            free_read_btn[0].click()

        content = driver.find_elements(By.CSS_SELECTOR, "div.content > div.p1,div.content > h3")
        content_text = '\n'.join([c.text for c in content])

        item['content'] = content_text
        driver.close()
        time.sleep(2)

        driver.switch_to.window(current_window)
        driver.close()

        driver.switch_to.window(search_homepage)
        df = pd.concat([df, pd.Series(item).to_frame().T], ignore_index=True)

    time.sleep(2)

    return row_no, df
