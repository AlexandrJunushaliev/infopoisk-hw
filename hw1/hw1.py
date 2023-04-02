import json
import requests
f = open('hw1\\links.json')
urls =  list(set(json.load(f)))
f.close()
commonFile = 'hw1\\res\\выкачка'
for i, url in enumerate(urls):
    try:
        response = requests.get(url)
        filename = f'hw1\\res\\page_{i+1}.html'

        # открываем файл для записи
        with open(filename, 'w', encoding='utf-8') as f:
            # записываем содержимое страницы в файл
            f.write(response.text)  

        with open(commonFile, 'a', encoding='utf-8') as f:
            f.write(response.text)

        # записываем индекс и URL-адрес страницы в файл index.txt
        with open('hw1\\res\\index.txt', 'a', encoding='utf-8') as f:
            f.write(f'{i+1}\t{url}\n')
    except Exception as e:
        # обработка ошибки при запросе к странице
        print(f'Ошибка при загрузке страницы {url}: {e}')
