# Импорт необходимых модулей
from selenium import webdriver  # модуль для автоматизации работы с браузером
from selenium.webdriver.chrome.options import Options  # модуль для настройки опций браузера Chrome
from selenium.webdriver.common.by import By  # модуль для выбора элементов на веб-странице по различным критериям
from selenium.webdriver.common.keys import Keys  # модуль для эмуляции нажатия клавиш
from selenium.webdriver.support.ui import WebDriverWait  # модуль для ожидания появления элементов на странице
from selenium.webdriver.support import expected_conditions as EC  # модуль для определения ожидаемых условий
from loader_img import loader_images
import pandas as pd
import time

# Запросить у пользователя поисковый запрос и максимальный рейтинг
my_search = input("Что будем искать на сайте:  ")
my_rating = input("До какого рейтинга искать:  ")

# Настройка Chrome webdriver с параметрами для максимизации окна
options = Options()
options.add_argument("start-maximized")
driver = webdriver.Chrome(options=options)

# Открыть веб-сайт Wildberries
driver.get("https://www.wildberries.ru/")

# Найти поле ввода поиска, ввести запрос и нажать Enter
input = driver.find_element(By.ID, "searchInput")
time.sleep(2)  # Подождать загрузки страницы
input.send_keys(my_search)
input.send_keys(Keys.ENTER)
time.sleep(3)  # Подождать загрузки результатов поиска

# Создать пустой словарь для хранения собранных данных
dict_pars = {
    "name": [],
    "rating": [],
    "count_mark": [],
    "price": [],
    "link": [],
    "path": []
}

# Нажать на кнопку выпадающего списка сортировки и выбрать второй вариант сортировки
button = driver.find_element(By.XPATH, './/button[@class="dropdown-filter__btn dropdown-filter__btn--sorter"]')
button.click()
time.sleep(1)  # Подождать отображения выпадающего меню
button = driver.find_element(By.XPATH, './/ul/li[2]/div/span[2]')
button.click()
time.sleep(3)  # Подождать применения сортировки

# Основной цикл для сбора данных до достижения или превышения желаемого рейтинга
rating = 5
while float(my_rating) < float(rating):
    while True:
        # Ожидать появления всех карточек товаров на странице
        wait = WebDriverWait(driver, timeout=30)
        cards = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//article[@id]")))
        print(len(cards))
        count = len(cards)
        # Прокрутить вниз, чтобы загрузить больше карточек товаров
        driver.execute_script("window.scrollBy(0,2000)")
        time.sleep(2)  # Подождать загрузки новых карточек товаров
        cards = driver.find_elements(By.XPATH, "//article[@id]")
        if len(cards) == count:
            break

    # Перебрать каждую карточку товара для сбора данных
    for card in cards:
        # Извлечь название продукта, цену, количество отзывов и рейтинг
        name = card.find_element(By.XPATH, './/div[@class="product-card__wrapper"]/a').get_attribute("aria-label")
        price = card.find_element(By.XPATH, ".//span[@class='price__wrap']/ins").text
        count_mark = card.find_element(By.XPATH, ".//span[@class='product-card__count']").text
        rating = card.find_element(By.XPATH, './/span[@class="address-rate-mini address-rate-mini--sm"]').text
        url_img = card.find_element(By.XPATH, './/div[@class="product-card__img-wrap img-plug j-thumbnail-wrap"]/img').get_attribute("src")
        # Проверить, соответствует ли рейтинг и количество отзывов критериям
        if float(rating) < 4.5 or int(count_mark.split()[0]) < 10:
            continue
        elif float(rating) < 4.3:
            break
        # Извлечь ссылку на продукт
        link = card.find_element(By.XPATH, './/div[@class="product-card__wrapper"]/a').get_attribute("href")
        path = loader_images(my_search, name, url_img)
        # Добавить собранные данные в словарь
        dict_pars["name"].append(name)
        dict_pars["rating"].append(rating)
        dict_pars["count_mark"].append(count_mark)
        dict_pars["price"].append(price)
        dict_pars["link"].append(link)
        dict_pars["path"].append(path)

    # Найти и нажать на кнопку "Следующая страница"
    button = driver.find_element(By.XPATH, '//a[@class="pagination-next pagination__next j-next-page"]')
    try:
        button.click()
    except:
        break

# Создать DataFrame из собранных данных и сохранить его в CSV-файл
df = pd.DataFrame(dict_pars)
df.to_csv(f"{my_search}.csv", index=False)
print(df)

time.sleep(300)

print()
