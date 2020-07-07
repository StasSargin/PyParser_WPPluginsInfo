import requests
from bs4 import BeautifulSoup
import csv


def get_html(url):
    r = requests.get(url)
    return r.text


# Форматируем строку с рейтингом.
def refined(s):
    r = s.split(' ')[0]
    result = r.replace(',', '')
    return result


def write_csv(data):
    with open('plugins.csv', 'a') as f:  # Записываем данные в конец файла.
        writer = csv.writer(f)

        writer.writerow((data['name'],  # Принимает только один элемент, поэтому создаем внутри кортеж.
                         data['url'],
                         data['rating']))


def get_data(html):
    soup = BeautifulSoup(html, 'lxml')
    sections = soup.find_all('section')  # Возвращает РезалтСет(список), каждый элемент которого это объект soup.
    articles = []
    for section in sections:
        articles += section.find_all('article')
    for article in articles:
        name = article.find('h3').find('a').text
        url = article.find('h3').find('a').get('href')

        r = article.find('span', class_="rating-count").find('a').text
        rating = refined(r)

        data = {
            'name': name,
            'url': url,
            'rating': rating
        }

        write_csv(data)


def main():
    url = "https://wordpress.org/plugins/"
    get_data(get_html(url))


if __name__ == '__main__':
    main()
