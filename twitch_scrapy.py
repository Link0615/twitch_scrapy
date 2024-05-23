import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from lxml import etree
from datetime import datetime, timedelta
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# 设置Chrome浏览器选项
options = Options()
driver = webdriver.Chrome(options=options)

# 打开Twitch的Elden Ring分类页面
url = 'https://www.twitch.tv/directory/category/elden-ring'
driver.get(url)

# 数据存储列表
data = []

# 要搜索的关键字列表
keywords = ["Grand Theft Auto V", "Call of Duty: Warzone"]

# 遍历每个关键字进行搜索
for keyword in keywords:
    search_input = driver.find_element(By.XPATH, "//input[@placeholder='搜索']")
    search_input.click()
    search_input.send_keys(keyword)
    time.sleep(2)
    search_button = driver.find_element(By.XPATH, "//button[@aria-label='搜索按钮']")
    search_button.click()
    time.sleep(1)

    # 等待并点击搜索结果中的分类链接
    wait = WebDriverWait(driver, 20)
    a_button = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                      '//div[@class="Layout-sc-1xcs6mc-0 ivrFkx"]/div/div[@data-a-target="search-result-category"]//a[@class="ScCoreLink-sc-16kq0mq-0 fPPzLm tw-link"]')))
    a_button.click()
    time.sleep(1)

    # 点击语言过滤按钮并选择葡萄牙语
    b_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[text()="语言"]/ancestor::button')))
    b_button.click()
    time.sleep(1)
    clear_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[text()="清除全部"]')))
    clear_button.click()
    time.sleep(1)
    label = wait.until(EC.element_to_be_clickable((By.XPATH, '//label[contains(., "Português")]')))
    label.click()
    time.sleep(1)
    b_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[text()="语言"]/ancestor::button')))
    b_button.click()
    time.sleep(1)

    # 按观众人数从高到低排序
    c_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="Layout-sc-1xcs6mc-0 xxjeD"]')))
    c_button.click()
    time.sleep(1)
    d_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[contains(text(), "观众人数（高到低）")]')))
    d_button.click()
    time.sleep(2)

    # 获取前几名的主播信息
    elements_count = len(driver.find_elements(By.XPATH, "(//p[contains(@class, 'CoreText-sc-1txzju1-0 gBknDX')])"))
    for index in range(1, min(elements_count, 3)):
        element = driver.find_element(By.XPATH, f"(//p[contains(@class, 'CoreText-sc-1txzju1-0 gBknDX')])[{index}]")
        element.click()
        time.sleep(2)

        # 确保当前URL已更改
        if driver.current_url != url:
            time.sleep(5)

            # 获取主播昵称
            streamer_name_xpath = "//h1[contains(@class, 'CoreText') and contains(@class, 'ScTitleText') and contains(@class, 'tw-title')]"
            streamer_name_element = wait.until(EC.presence_of_element_located((By.XPATH, streamer_name_xpath)))
            streamer_name = streamer_name_element.text

            # 获取关注者人数
            followers_count_xpath = "//span[@class='CoreText-sc-1txzju1-0 iFvAnD InjectLayout-sc-1i43xsx-0 fxviYd']"
            followers_count_element = wait.until(EC.visibility_of_element_located((By.XPATH, followers_count_xpath)))
            followers_count = followers_count_element.text

            print(streamer_name)
            print(followers_count)

            # 点击头像查看近期直播类别
            image_element = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                                   "//div[contains(@class, 'ScAvatar-sc-144b42z-0') and contains(@class, 'dFBjte') and contains(@class, 'tw-avatar')]/img[contains(@class, 'InjectLayout-sc-1i43xsx-0') and contains(@class, 'cXFDOs') and contains(@class, 'tw-image') and contains(@class, 'tw-image-avatar')]")))
            image_element.click()
            time.sleep(1)

            # 获取近期直播类别文本
            elements = driver.find_elements(By.XPATH, "//h2[contains(@class, 'CoreText-sc-1txzju1-0 gLOyjL')]")
            texts = [element.text for element in elements[:5]]
            combined_text = ', '.join(texts)
            print(combined_text)

            # 点击直播时间表
            schedule_element = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                                      "//p[contains(@class, 'CoreText-sc-1txzju1-0') and contains(@class, 'ScTitleText-sc-d9mj2s-0') and contains(@class, 'tw-title') and text()='直播时间表']")))
            schedule_element.click()
            time.sleep(5)

            # 获取过去几周的直播信息
            for _ in range(9):
                try:
                    current_date = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//div[contains(@class, 'eGlHLt')]//p[contains(@class, 'ezNtJL')]"))
                    )
                    current_date_text = current_date.text
                    z_button = driver.find_element(By.XPATH, "//button[@aria-label='上周']")
                    z_button.click()
                    WebDriverWait(driver, 10).until(
                        lambda d: d.find_element(By.XPATH,
                                                 "//div[contains(@class, 'eGlHLt')]//p[contains(@class, 'ezNtJL')]").text != current_date_text
                    )
                except TimeoutException:
                    print("等待超时，页面可能没有按预期更新")
                    break

            time.sleep(5)

            # 获取未来几周的直播信息
            for _ in range(9):
                try:
                    current_date = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//div[contains(@class, 'eGlHLt')]//p[contains(@class, 'ezNtJL')]"))
                    )
                    current_date_text = current_date.text
                    y_button = driver.find_element(By.XPATH, "//button[@aria-label='下周']")
                    y_button.click()
                    WebDriverWait(driver, 10).until(
                        lambda d: d.find_element(By.XPATH,
                                                 "//div[contains(@class, 'eGlHLt')]//p[contains(@class, 'ezNtJL')]").text != current_date_text
                    )
                except TimeoutException:
                    print("等待超时，页面可能没有按预期更新")
                    break

                time.sleep(3)

                # 获取每场直播的详细信息
                date_element = driver.find_element(By.XPATH,
                                                   "//div[contains(@class, 'eGlHLt')]//p[contains(@class, 'ezNtJL')]")
                date_text = date_element.text
                first_date_str = date_text.replace('—', '–').split(' – ')[0]
                specific_date = datetime.strptime(first_date_str, "%Y年%m月%d日")
                days_divs = driver.find_elements(By.XPATH,
                                                 "//*[contains(@class, 'stream-schedule-day') and @data-a-target='stream-schedule-day']")

                for i, day_div in enumerate(days_divs):
                    broadcast_date = (specific_date + timedelta(days=i)).strftime('%Y-%m-%d')
                    broadcasts = day_div.find_elements(By.XPATH, ".//*[contains(@class, 'Layout-sc-1xcs6mc-0 fGIEuO')]")

                    for broadcast in broadcasts:
                        title = driver.execute_script("return arguments[0].textContent;",
                                                      broadcast.find_element(By.XPATH,
                                                                             ".//*[contains(@class, 'bzySrJ stream-schedule-segment--text')]"))
                        try:
                            game_name_element = broadcast.find_element(By.XPATH,
                                                                       ".//*[contains(@class, 'ScCoreLink-sc-16kq0mq-0')]")
                            game_name = driver.execute_script("return arguments[0].textContent;", game_name_element)
                        except NoSuchElementException:
                            game_name = ""
                        viewers_elements = broadcast.find_elements(By.XPATH, ".//span[contains(@class, 'EhlCw')]")
                        if viewers_elements:
                            viewers_text = driver.execute_script("return arguments[0].textContent;",
                                                                 viewers_elements[0])
                            viewers_count = viewers_text.replace('次观看', '').strip()

                        print(title)
                        print(game_name)
                        print(viewers_count)
                        print(broadcast_date)
                        data.append({
                            "主播昵称": streamer_name,
                            "关注者人数": followers_count,
                            "近期直播类别": combined_text,
                            "直播日期": broadcast_date,
                            "每场直播的标题": title,
                            "直播的游戏名称": game_name,
                            "观看次数": viewers_count
                        })

            # 返回搜索结果页继续下一个主播的信息获取
            driver.get(url)
            time.sleep(5)

# 关闭浏览器
driver.quit()

# 将数据保存到Excel文件
df = pd.DataFrame(data)
df.to_excel("C:\\Users\\30473\\Desktop\\爬虫\\twitch.xlsx", index=False)
