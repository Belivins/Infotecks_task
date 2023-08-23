## Тестовое задание «Разработчик Python»
Реализовать HTTP-сервер для предоставления информации по географическим объектам.

## Порядок запуска скрипта
1. Установить необходимые зависимости <code>pip install -r requirments.txt</code>
2. Запустить скрипт <code>python script.py</code>

## Описание методов

### 1. Метод принимает идентификатор geonameid и возвращает информацию о городе.
* Название функции - get_info(name_id)
* Пример запроса - <code>http://127.0.0.1:8000/get_info/451749</code>
#### Ответ 
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
### 2. Метод принимает страницу и количество отображаемых на странице городов и возвращает список городов с их информацией. 
* Название функции - get_page()
* Пример запроса - <code>http://127.0.0.1:8000/get_page?page=1&num=5</code>
#### Ответ 
```json
[
  {"geonameid":451747,"name":"Zyabrikovo","asciiname":"Zyabrikovo","alternatenames":"","latitude":56.84665,"longitude":34.7048,"feature class":"P","feature code":"PPL","country code":"RU","cc2":"","admin1":"77","admin2":"","admin3":"","admin4":"","population":0,"elevation":"","dem":204,"timezone":"Europe/Moscow","date":"2011-07-09"},
  {"geonameid":451748,"name":"Znamenka","asciiname":"Znamenka","alternatenames":"","latitude":56.74087,"longitude":34.02323,"feature class":"P","feature code":"PPL","country code":"RU","cc2":"","admin1":"77","admin2":"","admin3":"","admin4":"","population":0,"elevation":"","dem":215,"timezone":"Europe/Moscow","date":"2011-07-09"},
  {"geonameid":451749,"name":"Zhukovo","asciiname":"Zhukovo","alternatenames":"","latitude":57.26429,"longitude":34.20956,"feature class":"P","feature code":"PPL","country code":"RU","cc2":"","admin1":"77","admin2":"","admin3":"","admin4":"","population":0,"elevation":"","dem":237,"timezone":"Europe/Moscow","date":"2011-07-09"},
  {"geonameid":451750,"name":"Zhitovo","asciiname":"Zhitovo","alternatenames":"","latitude":57.29693,"longitude":34.41848,"feature class":"P","feature code":"PPL","country code":"RU","cc2":"","admin1":"77","admin2":"","admin3":"","admin4":"","population":0,"elevation":"","dem":247,"timezone":"Europe/Moscow","date":"2011-07-09"},
  {"geonameid":451751,"name":"Zhitnikovo","asciiname":"Zhitnikovo","alternatenames":"","latitude":57.20064,"longitude":34.57831,"feature class":"P","feature code":"PPL","country code":"RU","cc2":"","admin1":"77","admin2":"","admin3":"","admin4":"","population":0,"elevation":"","dem":198,"timezone":"Europe/Moscow","date":"2011-07-09"}
]
```
