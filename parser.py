from bs4 import BeautifulSoup
import requests
import time
import random
from fake_useragent import UserAgent

def format_price(price):
    # Убираем "от", "₽" и лишние пробелы
    price = price.replace('от', '').replace('₽', '').replace('\xa0', '').strip()
    # Убираем все нечисловые символы, кроме пробелов
    price = ''.join(filter(str.isdigit, price))
    # Форматируем с точками (например, 2249900 -> 2.249.900)
    price = int(price)
    return f"{price:,}".replace(',', '.')


def parse():

    url = 'https://keyauto.ru/omsk/cars/'

    # Инициализация случайного User-Agent
    ua = UserAgent()

    # Заголовки для имитации браузера
    headers = {
        'User-Agent': ua.random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Referer': 'https://keyauto.ru/',
    }

    try:
        # Выполняем запрос
        page = requests.get(url, headers=headers, timeout=10)
        print(f"Статус код: {page.status_code}")

        if page.status_code != 200:
            print("Ошибка: Скорее всего, капча или блокировка.")
            return

        # Парсим страницу
        soup = BeautifulSoup(page.content, 'html.parser')
        blocks = soup.find_all('div', class_='card')

        if not blocks:
            print("Блоки не найдены. Возможно, структура сайта изменилась.")
            return

        description = ''

        # Извлекаем данные
        for data in blocks:
            try:
                # Название
                name_elem = data.find('a', class_='card__title')
                name = name_elem.text.strip() if name_elem else "Название не найдено"

                # Цена
                price_elem = data.find('div', class_='card__price')
                price = price_elem.text.strip() if price_elem else "Цена не указана"
                price = format_price(price)  # Форматируем цену

                # Формируем строку (только название и цена)
                description += f"{name}/{price}\n"
            except AttributeError:
                print("Ошибка в структуре данных. Пропускаем.")
                continue

        # Записываем в файл
        with open('output.txt', 'w', encoding='utf-8') as f:
            f.write(description)
        print("Данные успешно записаны в output.txt")

    except requests.RequestException as e:
        print(f"Ошибка запроса: {e}")

    # Случайная задержка
    time.sleep(random.uniform(1, 3))

if __name__ == "__main__":
    parse()