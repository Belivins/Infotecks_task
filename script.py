import pandas as pd
from googletrans import Translator
from difflib import SequenceMatcher
from transliterate import translit
from datetime import datetime
from pytz import timezone
from flask import Flask, request, jsonify


class GeoName:

    def __init__(self):
        """ Чтение данных из файла.
        Фильтрация населенных пунктов из всех данных.
        Заполнение NaN значений пустой строкой.
        """
        headers = [
            'geonameid',
            'name',
            'asciiname',
            'alternatenames',
            'latitude',
            'longitude',
            'feature class',
            'feature code',
            'country code',
            'cc2',
            'admin1',
            'admin2',
            'admin3',
            'admin4',
            'population',
            'elevation',
            'dem',
            'timezone',
            'date'
        ]
        data = pd.read_csv("RU.txt", sep="\t", names=headers, low_memory=False)
        self.data_frame = data[data['feature class'] == 'P'].reset_index(drop=True)
        self.data_frame = self.data_frame.fillna('')

    def get_by_id(self, name_id: int):
        """ Получение информации о населенном пункте по geonameid. """
        return self.data_frame[self.data_frame['geonameid'] == name_id]

    def get_page(self, page_num: int, display_num: int):
        """ Получение страницы с информацией о городах.
        :param page_num: номер страницы.
        :param display_num: количество городов на странице.
        :return: Возвращает нужную страницу с заданным количеством городов.
        """
        start_index = (page_num - 1) * display_num
        end_index = start_index + display_num
        num_row = self.data_frame.shape[0]
        num_pages = (num_row + display_num - 1) // display_num
        if (start_index >= 0) and (start_index < num_row) and (page_num < num_pages):
            return self.data_frame[start_index:end_index]
        else:
            return pd.DataFrame()

    def search_in_string(self, city_name):
        """ Поиск названия в строке.
        :param city_name: Название города.
        :return: Возвращает список городов, которые имеют схожие альтернативные названия.
        """
        return self.data_frame[pd.Series(
            max([True if elm.lower() == city_name.lower() else False for elm in row]) for row in
            self.data_frame['alternatenames'].str.split(','))]

    def find_city(self, city_name):
        """ Поиск городов с заданным названием.
        :param city_name: Название города
        :return: Список городов, отсортированных в порядке убывания по населению
        """
        found_cities = pd.concat([self.data_frame[self.data_frame['name'].str.fullmatch(city_name, case=False)],
                                  self.search_in_string(city_name)]).drop_duplicates()
        return found_cities.sort_values('population', ascending=False).reset_index(drop=True)

    def translate_name(self, name):
        """ Перевод с русского на английский.
        :param name: Название города на русском.
        :return: Название на английском.

        Сравниваем два перевод и транслит названия.
        Если они схожи, то выбираем перевод, иначе транслит.
        Например проблемы перевода названий Zyabrikovo и Ladnoye
        """
        translator = Translator()
        name_1 = translator.translate(name).text.title()
        name_2 = translit(name, reversed=True)
        if SequenceMatcher(None, name_1, name_2).ratio() >= 0.8:
            return name_1
        else:
            return name_2

    def find_matches(self, part_name):
        """ Поиск похожих названий.
        :param part_name: Название или часть названия города.
        :return: Список городов, имеющих похожее название.
        """
        found_cities = pd.concat([self.data_frame[self.data_frame['name'].str.find(part_name) != -1], self.data_frame[
            self.data_frame['alternatenames'].str.find(part_name) != -1]]).drop_duplicates()
        return found_cities.sort_values('population', ascending=False).reset_index(drop=True)


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['JSON_AS_ASCII'] = False
geo_date = GeoName()


@app.route('/get_info/<int:name_id>', methods=['GET'])
def get_info(name_id):
    """ Получение информации о населенном пункте по geonameid. """
    city_info = geo_date.get_by_id(name_id)
    if city_info.empty:
        return "No matches found", 400
    return jsonify(city_info.to_dict(orient="records"))


@app.route('/get_page', methods=['GET'])
def get_page():
    """ Получение страницы с информацией о городах.
    :param page_num: номер страницы.
    :param display_num: количество городов на странице.
    :return: Возвращает нужную страницу с заданным количеством городов.
    """
    page_num = request.args.get('page', type=int)
    display_num = request.args.get('num', type=int)
    page = geo_date.get_page(page_num, display_num)
    if page.empty:
        return "Invalid page", 400
    return jsonify(page.to_dict(orient="records"))


@app.route('/get_compare', methods=['GET'])
def get_compare():
    """ Сравнение двух городов.
    :param first_city: Название первого города.
    :param second_city: Название второго города.
    :return: Возвращает информацию о городах, какой из них расположен севернее,
     одинаковые ли временные зоны и на сколько часов отличаются.
    """
    first_city = request.args.get('first')
    second_city = request.args.get('second')
    if (first_city is None or first_city == "") or (second_city is None or second_city == ""):
        return "Empty request", 400
    first_city = geo_date.find_city(geo_date.translate_name(first_city))
    second_city = geo_date.find_city(geo_date.translate_name(second_city))
    if first_city.empty or second_city.empty:
        return "No matches found", 400
    first_city = first_city.loc[first_city.index[0]]
    second_city = second_city.loc[second_city.index[0]]
    northeren = first_city['name'] if (first_city['latitude'] > second_city['latitude']) else second_city['name']
    timezone_equal = first_city['timezone'] == second_city['timezone']
    time_difference = abs(datetime.now(timezone(first_city['timezone'])).time().hour - datetime.now(
        timezone(second_city['timezone'])).time().hour)
    return jsonify(first_city.to_dict(), second_city.to_dict(), northeren, timezone_equal, time_difference)


@app.route('/get_matches', methods=['GET'])
def get_matches():
    """ Поиск похожих названий.
    :param name: Название или часть названия города.
    :return: Список городов, имеющих похожее название.
    """
    city_name = request.args.get('name')
    if city_name is None or city_name == "":
        return "Empty request", 400
    name_list = geo_date.find_matches(city_name)['name'].to_list()
    if not name_list:
        return "No matches found", 204
    return jsonify(name_list)  # .to_json(orient='records')


# driver function
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
