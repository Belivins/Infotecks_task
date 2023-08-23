## Тестовое задание «Разработчик Python»
Реализовать HTTP-сервер для предоставления информации по географическим объектам.

## Порядок запуска скрипта
1. Установить необходимые зависимости <code>pip install -r requirments.txt</code>
2. Запустить скрипт <code>python script.py</code>

## Описание методов

### 1. Метод принимает идентификатор geonameid и возвращает информацию о городе.
Название функции - get_info(name_id)
Пример запроса - <code>http://127.0.0.1:8000/get_info/451749<code>
Ответ - 
```json
[
  {
    "geonameid":451749,
    "name":"Zhukovo",
    "asciiname":"Zhukovo",
    "alternatenames":"",
    "latitude":57.26429,
    "longitude":34.20956,
    "feature class":"P",
    "feature code":"PPL",
    "country code":"RU",
    "cc2":"",
    "admin1":"77",
    "admin2":"",
    "admin3":"",
    "admin4":"",
    "population":0,
    "elevation":"",
    "dem":237,
    "timezone":"Europe/Moscow",
    "date":"2011-07-09"
  }
]
```
