import csv
import requests
import time
from pprint import pp
from bs4 import BeautifulSoup

all_thems = {
    '10': 'Армия, ВПК, спецслужбы',
    '40': 'Африка как ничейные ресурсы',
    '35': 'Ближний Восток',
    '52': 'БРИКС',
    '27': 'В России',
    '44': 'Демократия и удобные режимы',
    '24': 'Европа: тенденции',
    '46': 'Информационные пузыри',
    '2': 'Иран',
    '23': 'История: факты и документы',
    '21': 'Кавказ: зона нестабильности',
    '48': 'Космос',
    '41': 'Мировое правительство',
    '9': 'Наследники СССР сегодня',
    '51': 'НАТО: реликт ушедшей эпохи',
    '31': 'Наука, техника, образование',
    '38': 'Новости сайта',
    '20': 'США: опыт строительства империи',
    '28': 'Терроризм: факты и движущие силы',
    '50': 'Торговые войны',
    '47': 'Цензура',
    '45': 'Чрезвычайные ситуации',
    '34': 'ШОС и ситуация в Азии',
    '49': 'Экология и климат',
    '26': 'Экономика и Финансы',
    '11': 'Южноамериканский бунт'
}

file_name = 'Все по 200.csv'

start_time = time.time()


def get_data():
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                'Категория',
                'Название статьи',
                'Ссылка на статью',
                'Текст статьи'
            )
        )

    for number_of_category, category_name in all_thems.items():
        page = 1
        wap_url = f'https://www.warandpeace.ru/ru/archive/search/_/text_header=&author=&topic={number_of_category}&date_st=01.05.2006&sselect=0&date_en=23.4.2024&archive_sort=5&page={page}/'

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
        }

        #  Заходим на требуемый сайт
        response = requests.get(wap_url, headers)
        # time.sleep(5)

        #  Парсим его в виде текста
        soup = BeautifulSoup(response.text, 'html.parser')

        #  Получаем количество страниц определенной темы
        try:
            articles = soup.find('span', class_="menu_1").text.split()
            colvo_str = (int(articles[3]))

        except:
            print('Количество страниц не найдено')
            colvo_str = 1

        topic_data = []

        for page in range(1, 201):

            #  URL сайта
            wap_url = f'https://www.warandpeace.ru/ru/archive/search/_/page=1/?text_header=&author=&topic={number_of_category}&date_st=01.05.2006&sselect=0&date_en=23.4.2024&archive_sort=5&page={page}/'

            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
            }

            #  Заходим на требуемую страницу
            response = requests.get(wap_url, headers)

            #  Парсим ее
            soup = BeautifulSoup(response.text, 'html.parser')

            try:
                # Получаем ссылки на статьи
                links_articles = soup.find_all('td', class_="topic_caption")
            except:
                print('Ссылки не найдены')
                links_articles = []

            for article in links_articles:
                # Выделяем название статьи
                topic_name = article.text
                # Выделяем ссылку на статью
                link_article = article.a['href']

                URL = link_article
                #  Заходим на статью
                response = requests.get(URL)

                #  Парсим ее
                soup = BeautifulSoup(response.text, 'html.parser')

                try:
                    topic_text = soup.find('td', class_='topic_text').text.replace('\xa0', '')
                except:
                    topic_text = 'Текст статьи не найден'

                topic_data.append(
                    {
                        'category_name': category_name,
                        'topic_name': topic_name,
                        'topic_link': link_article,
                        'topic_text': topic_text
                    }
                )

                with open(file_name, 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(
                        (
                            category_name,
                            topic_name,
                            link_article,
                            topic_text
                        )
                    )

            print(f'Обработал страницу {page}')


def main():
    get_data()
    finish_time = time.time() - start_time
    print(f'Время на работу: {finish_time}')


if __name__ == '__main__':
    main()
