import os
import zipfile
import hashlib
import requests
import re
import csv

# Задание №1 - Программно разархивировать архив в выбранную директорию.
directory_to_extract_to = 'C:\\Users\\D_20\\Desktop\\ВУЗ\\Лабы Прикладное\\unpacking'  # директория извлечения файлов архива
arch_file = "C:\\Users\\D_20\\Desktop\\ВУЗ\\Лабы Прикладное\\tiff-4.2.0_lab1.zip"  # путь к архиву
zip_file = zipfile.ZipFile(arch_file)  # Открытие zip-архива
zip_file.extractall(directory_to_extract_to)  # Извлечение всех файлов из архива в директорию + создание директории

# Задание №2 - Найти в директории все файлы формата txt, получить значения MD5 хеша для найденных файлов и
# вывести полученные данные на экран (имя файла и хеш).

# Получаем полные пути текстовых файлов и сохраняем их в список.
txt_files = []
for root, dirs, files in os.walk(directory_to_extract_to):
    for file in files:  # бежим по файлам
        if file.endswith('.sh'):  # если окончание .txt
            txt_files.append(str(root + '\\' + file))  # записываем в список абсолютные пути текстовых файлов
            print(file)

# Получаем значения MD5 хеша для файлов из списка и выводим полученные данные на экран
for file in txt_files:
    target_file_data = open(file, 'rb').read()
    hash = hashlib.md5(target_file_data).hexdigest()
    print('name: ', os.path.basename(file), 'hash: ', hash)

# Задание №3 - Найти файл, MD5 хеш которого равен следующему значению: 4636f9ae9fef12ebd56cd39586d33cfb. Прочитать из файла ссылку на веб-страницу.
target_hash = "4636f9ae9fef12ebd56cd39586d33cfb"
for file in txt_files:
    target_file_data = open(file, 'rb').read()
    if hashlib.md5(target_file_data).hexdigest() == target_hash:
        print('File: ', file, 'Link to the web page: ', target_file_data)

# Задание №4 - Получить содержимое веб-страницы (по ссылке из задания 3). При помощи
# регулярных выражений и методов работы со строками распарсить содержимое HTML страницы и сохранить информацию из таблицы в словарь.
target_file_data = 'https://meduza.io/feature/2020/03/05/poslednie-dannye-po-koronavirusu-vo-vsem-mire-tablitsa'
r = requests.get(target_file_data)
result_dct = {}  # словарь для записи содержимого таблицы

counter = 0
# Получение списка строк таблицы
lines = re.findall(r'<div class="Table-module_row__3TH83">.*?</div>.*?</div>.*?</div>.*?</div>.*?</div>', r.text)
for line in lines:
    # извлечение заголовков таблицы
    if counter == 0:
        counter += 1
        continue
    # Удаление тегов
    temp = re.sub('<[^<>]*>', ';', line)
    temp = re.sub(r'\([^()]*\)', '', temp)
    temp = re.sub(r';[;;]*;', ';', temp)
    temp = temp[1:-1]
    temp = re.sub('.*\s\s', '', temp)
    temp = re.sub('_', '-', temp)
    temp = re.sub('\*', '', temp)
    temp = temp.replace(u'\xa0', u' ')# sub

    tmp_split = temp.split(';')  # разделяем строку на подстроки для массива
    country_name = tmp_split[0]  # получаем название страны

    # извлечение данных из оставшихся столбцов (статистика)
    col1_val = tmp_split[1]
    col2_val = tmp_split[2]
    col3_val = tmp_split[3]
    col4_val = tmp_split[4]

    # Запись извлеченных данных в словарь
    result_dct[country_name] = [0, 0, 0, 0]
    result_dct[country_name][0] = col1_val
    result_dct[country_name][1] = col2_val
    result_dct[country_name][2] = col3_val
    result_dct[country_name][3] = col4_val

    counter += 1

# Задание №5 - Сохранить содержимое таблицы в новый файл, где каждая новая строка таблицы
# сохраняется с новой строки, а отдельные столбцы отделены символом ";".

output = open('C:\\Users\\D_20\\Desktop\\ВУЗ\\Лабы Прикладное\\data.csv', 'w')  # открытие файла для записи
writer = csv.writer(output, delimiter=";")  # красивое разделение в excel
writer.writerow(['', 'ЗАБОЛЕЛИ', 'УМЕРЛИ', 'ВЫЛЕЧИЛИСЬ', 'АКТИВНЫЕ СЛУЧАИ'])  # строка для обозначения статистики
for key, v in result_dct.items():  # записываем словарь в таблицу
    writer.writerow([key, v[0], v[1], v[2], v[3]])
output.close()

# Задание №6

target_country = input("Введите название страны: ")
print(result_dct[target_country])
