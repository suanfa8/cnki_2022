## 旧版项目

- 地址：[https://gitee.com/minge8/cnki](https://gitee.com/minge8/cnki)

## 报错 `element not interactable` 是因为 `display: none;`

```
selenium.common.exceptions.ElementNotInteractableException: Message: element not interactable
```

解决办法：https://blog.csdn.net/teachskyLY/article/details/85029157

```python
# 休息 5 秒
import time
time.sleep(5) 


    # dropdown2 = driver.find_element(By.XPATH, '//*[@id="gradetxt"]/dd[2]/div[2]/div[1]')
    # dropdown2.click()
    #
    # quanwen_a_link2 = driver.find_element(By.XPATH, '//*[@id="gradetxt"]/dd[2]/div[2]/div[1]/div[2]/ul/li[5]/a')
    # print(quanwen_a_link2.text)
    # quanwen_a_link2.click()
    # quanwen_a_link2.click()

    # sort_list2 = driver.find_element(By.XPATH, '//*[@id="gradetxt"]/dd[2]/div[2]/div[1]/div[2]')
    # options2 = sort_list2.find_elements(By.TAG_NAME, "li")
    # for option in options2:
    #     if option.text == '全文':
    #         a = option.find_element(By.TAG_NAME, "a")
    #         a.click()
    #         a.click()
    #         break
```
