from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import csv


def safe_find_text(element, selector, attribute=None):
    try:
        if attribute:
            return element.find(selector)[attribute]
        result = element.find(selector).text.strip()
        return result if result else "Нет данных"
    except:
        return "Нет данных"


def parse_auto_ru():
    url = 'https://auto.ru/omsk/cars/all/?sort=cr_date-desc'

    # Настройка Selenium
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)

        # Ожидание загрузки
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".ListingItem"))
        )

        # Проверка на капчу
        if "showcaptcha" in driver.current_url:
            print("Обнаружена капча! Пожалуйста, решите её вручную в открывшемся браузере.")
            input("Нажмите Enter после решения капчи...")
            driver.get(url)  # Перезагружаем страницу

        # Парсинг данных
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        cars = soup.find_all('div', class_='ListingItem')

        if not cars:
            print("Не найдено ни одного автомобиля. Проверьте структуру страницы.")
            return

        with open('auto_ru_cars.csv', 'w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow([
                'Марка', 'Цена', 'Год', 'Пробег',
                'Двигатель', 'Коробка', 'Привод', 'Ссылка'
            ])

            for car in cars:

                title = safe_find_text(car, 'a', 'title') or safe_find_text(car, 'a', 'text')
                price = safe_find_text(car, 'div', {'class': 'ListingItemPrice__content'})
                year = safe_find_text(car, 'div', {'class': 'ListingItem__year'})
                mileage = safe_find_text(car, 'div', {'class': 'ListingItem__kmAge'})

                specs = car.find_all('div', class_='ListingItemTechSummaryDesktop__cell')
                engine = specs[0].text.strip() if len(specs) > 0 else "Нет данных"
                transmission = specs[1].text.strip() if len(specs) > 1 else "Нет данных"
                drive = specs[2].text.strip() if len(specs) > 2 else "Нет данных"

                link = car.find('a', class_='Link ListingItemTitle__link')['href'] if car.find('a',class_='Link ListingItemTitle__link') else "Нет ссылки"
                writer.writerow([
                    title, price, year, mileage,
                    engine, transmission, drive, link
                ])
        print(f"Успешно сохранено {len(cars)} автомобилей в auto_ru_cars.csv")
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    parse_auto_ru()