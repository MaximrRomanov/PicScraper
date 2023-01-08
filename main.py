from typing import List
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from fake_useragent import UserAgent
import os


def parser() -> List[str]:
    user_agent = UserAgent()
    header = {'user-agent': f'{user_agent.chrome}'}
    base_url = 'https://mosplitka.ru/catalog/plitka/plitka-dlya-vannoy/view_product/'
    response = requests.get(base_url, headers=header)
    soup = BeautifulSoup(response.text, 'lxml')
    urls = []
    get_image_url_from_page(soup, urls)  # для главной страницы получаем список ссылок
    # last_page_index = int(get_index_of_last_page())  # 391
    for index in range(2, 51):
        next_page_link = 'https://mosplitka.ru/catalog/plitka/plitka-dlya-vannoy/view_product/' + '?PAGEN_1=' + str(
            index)
        response = requests.get(next_page_link)
        soup = BeautifulSoup(response.text, 'lxml')
        get_image_url_from_page(soup, urls)
    return urls


def get_image_url_from_page(soup: BeautifulSoup, urls: list):
    images = soup.find('div', class_='products product-list-block plitka_new').find_all('img',
                                                                                        class_='lazy')  # all images

    for image in images:
        img_url = image.attrs.get('src') or image.attrs.get('data-original')
        if not img_url:
            # если img не содержит атрибута src, просто пропустим
            continue
            # сделаем URL абсолютным, присоединив имя домена к только что извлеченному URL
        img_url = urljoin('https://mosplitka.ru/', img_url)
        try:
            requests.get(img_url)
            urls.append(img_url)
        except:
            print('Ошибка доступа')


def get_index_of_last_page() -> int:
    url = 'https://mosplitka.ru/catalog/plitka/plitka-dlya-vannoy/view_product/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    last_page_link = soup.find_all('li', class_='pagination-catalog__item')[6].find('a', class_='pagination'
                                                                                                '-catalog__link').get(
        'href')
    last_page_index = last_page_link.split('=')[-1]  # 391
    return last_page_index


def download(url: str, pathname: str):
    if not os.path.isdir(pathname):
        os.mkdir(pathname)
    # получаем имя файла
    filename = os.path.join(pathname, url.split("/")[-1])
    # проверка на наличие картинки в директории
    if not os.path.exists(filename):
        with open(filename, 'wb') as file:
            # записываем прочитанные данные в файл
            file.write(requests.get(url).content)


def main(pathname: str):
    images = parser()
    print(len(images))
    print(images)
    for img in images:
        download(img, pathname)


main('mosplitka photo')
