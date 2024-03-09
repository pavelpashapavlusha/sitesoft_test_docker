from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
import schedule
import sqlite3


options = webdriver.ChromeOptions()

# открытие драйвера в полном окне
options.add_argument("start-maximized")
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# устанавливаем параметр загрузки страницы
options.page_load_strategy = 'eager'

# настройки стелс режима драйвера
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
browser = webdriver.Chrome(options=options)

# настройки стелс режима драйвера
stealth(browser,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

# создаем пустой словарь и список
data = {}
list_db = []


# функция управления парсером
def parser():
    url = "https://habr.com/ru/articles/"
    browser.get(url)
    blocks = browser.find_element(By.CLASS_NAME, "tm-articles-list")
    posts = blocks.find_elements(By.XPATH, '//*[@class="tm-articles-list__item"]/div[@class="tm-article-snippet tm-article-snippet"]')

    for post in posts:
        title = post.find_element(By.TAG_NAME, 'h2').find_element(By.TAG_NAME, "a").text
        title_url = post.find_element(By.TAG_NAME, 'h2').find_element(By.TAG_NAME, "a").get_attribute("href")
        data[title] = [
            title, title_url
        ]

    for post_url in data.values():
        browser.get(post_url[1])
        date = browser.find_element(By.TAG_NAME, "time").text
        name_author = browser.find_element(By.CLASS_NAME, 'tm-user-info__username').text
        url_author = browser.find_element(By.CLASS_NAME, 'tm-user-info__username').get_attribute('href')
        hab_art_list = browser.find_elements(By.CLASS_NAME, "tm-hubs-list__link")
        post_url.append(date)
        post_url.append(name_author)
        post_url.append(url_author)
        for hab_art in hab_art_list:
            post_url.append(hab_art.text)

    for val in data.values():
        list_db.append(val)

    return (list_db)


parser()


# создаем списки для сохранения информации в бд
list_for_db_frs = []
for list_db_one in list_db:
    list_for_db_frs.append(list_db_one[:5])


list_for_db_sec = []
for list_db_one in list_db:
    list_for_db_sec.append(list_db_one[5])
    list_for_db_sec.append(list_db_one[0])
chunk_size = 2
chunks = [list_for_db_sec[i:i + chunk_size] for i in range(0, len(list_for_db_sec), chunk_size)]


# создание записей в таблицах бд

conn = sqlite3.connect("db.sqlite3")

cursor = conn.cursor()

cursor.executemany("INSERT INTO parser_habr_parser (title, url, date, name_author, url_author) values (?,?,?,?,?)", list_for_db_frs)
cursor.executemany("INSERT INTO parser_habs (hab, title_article) values (?,?)", chunks)

conn.commit()
conn.close()


# скрипт для того, чтобы код выполнялся каждые 10 минут

# schedule.every(10).minutes.do(parser)
# while True:
#     schedule.run_pending()
