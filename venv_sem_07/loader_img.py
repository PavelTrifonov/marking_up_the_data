import os
import requests


def loader_images(dir_name, card_name, url_img):
    # URL фотографии для загрузки
    url = url_img
    # Имя файла, которое вы хотите использовать
    filename = card_name + ".jpg"
    # Имя директории, которую вы хотите создать
    directory_name = dir_name
    # Путь к текущей директории
    current_directory = os.getcwd()
    # Создаем папку, если она не существует
    directory_path = os.path.join(current_directory, directory_name)
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    # Путь к загружаемому файлу
    file_path = os.path.join(directory_path, filename)
    # Отправляем GET-запрос для загрузки фотографии
    response = requests.get(url)
    # Проверяем, успешно ли загружена фотография
    if response.status_code == 200:
        # Открываем файл для записи в бинарном режиме
        with open(file_path, 'wb') as f:
            # Записываем содержимое ответа в файл
            f.write(response.content)
    return file_path
