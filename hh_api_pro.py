import requests

import pprint
import collections
import pymorphy2
import string



def avarage_salary():

    URL = 'https://api.hh.ru/vacancies'
    salary_list_from = [] # список с зарплатами от...
    salary_list_to = [] # список с зарплатами до...

    for n in range(20):

        params = {'text': 'Python && Москва',
        'only_with_salary': True,
        'per_page': 100, 'page': n
        }

        result = requests.get(URL, params = params).json()

        for j in result['items']:
            if j['salary']['from'] != None: # убираем зарплаты с пустным значением
                salary_list_from.append(j['salary']['from']) # создаем лист с зарплатой от...
            if j['salary']['to'] != None: # убираем зарплаты с пустным значением
                salary_list_to.append(j['salary']['to']) # создаем лист с зарплатой до...

    # Средняя зарплата (от:)
    # делим сумму списка зарплат от... на количество элементов списка
    # округляем (round), приводим к строке для вывода в формате 000 000
    salary_from_average = str(round(sum(salary_list_from)/len(salary_list_from)))
    salary_from_average = f'{salary_from_average [:-3]} {salary_from_average [-3:]}'

    # Средняя зарплата (до:)
    # делим сумму списка зарплат до... на количество элементов списка
    # округляем (round), приводим к строке для вывода в формате 000 000
    salary_to_average = str(round(sum(salary_list_to)/len(salary_list_to)))
    salary_to_average = f'{salary_to_average [:-3]} {salary_to_average [-3:]}'



    #print(f'Средняя зарплата: от {salary_from_average} до {salary_to_average}')

    # Всего было найдено вакансий:
    results_all = result['found']

    data = {

            'salary_from_average': salary_from_average,
            'salary_to_average':salary_to_average,
            'results_all': results_all
                }

    return data

def hh_requirements():

    URL = 'https://api.hh.ru/vacancies'

    requirement_list = [] # список с требованиями

    for n in range(20):
        params = {
            'text': 'Python && Москва',
            'page': n,
            'per_page': 100
                        }


        result = requests.get(URL, params=params).json()
        result_items = result['items']
        results_all = result['found']

        for i in result_items:
            if i['snippet'] != None:  # убираем snippet с пустным значением
                result_snippet = i['snippet']
                if result_snippet['requirement'] != None:  # убираем requirement с пустным значением
                    requirement = result_snippet['requirement']

                    # очистить текст c требованиями по вакансиям от знаков препинания и вставки "highlighttext". Убираем лишние пробелы
                    for i in string.punctuation:
                        requirement = requirement.replace(i, " ")
                        requirement = requirement.replace('highlighttext', "")
                        requirement = requirement.replace('   ', " ")
                        requirement = requirement.replace('  ', " ")
                requirement_list += requirement.split() # создаем список из отдельных слов


    other_words = {"основа","приветствоваться","задача","java","инструмент","r","go","perl","php","скрипт","технология","желательно","анализ","плюс","скриптовый",
                   "автоматизация","работа","опыт", "работы","на", "не", "под", "у", "в", "с", "перед","до", "о", "по", "из-за", "от", "для",
                    "из-под", "над", "без", "близ", "ввиду", "между", "возле", "рядом", "около",
                    "отношении", "вокруг", "впереди", "в продожение", "вследствие", "течение",
                    "из", "кроме", "от", "подле", "по мере", "после", "прежде", "против",
                    "благодаря", "вопреки", "к", "согласно", "соответсвенно", "несмотря",
                    "про", "сквозь", "через", "во", "за", "об", "обо", "в", "соответствии",
                    "надо", "перед", "согласно", "связи", "при", "без", "до", "для", "из",
                    "под", "пред", "при", "ввиду", "насчет", "помощи", "случае", "условии",
                    "погодя", "спустя", "благодаря", "начиная", "несмотря", "считая", "после",
                    "мимо", "внутри", "вдоль", "вдали", "вокруг", "и", "или", "без", "можно", "лет", "уверенный",
                   "опыт", "знание", "работа", "python", "разработка", "понимание", "experience", "умение", "python.",
                   "хороший", "of", "язык", "in", "программирование", "and", "высокий", "with", "коммерческий", "3", "владение",
                   "отличный", "python,", "/", "принцип", "работать", "1", "год", "менее", "один", "2-х","использование","технический",
                   "<highlighttext>python</highlighttext>", "года", "knowledge", "2", "иметь", "быть", "база", "написание",
                   "писать", "дать", "навык", "уровень", "образование", "years", "<highlighttext>development</highlighttext>", "с...",
                   "и...", "3-х","промышленный","3","базовый","паттерн","желание","данных","образование","разработки.","реляционный","как",
                   "структура","основный","система","код","strong","or","создание","современный","3.","good","проектирование","работы...'",
                   "необходимый","+", "лет.", "-", "х", "c", "5", "приложение", "разработчик", "rest", "development", "web"}

    requirement_list_lower = list(map(lambda x: x.lower(), requirement_list)) # приводим слова к нижнему регистру
    words_lemmed = [] # лемматизированный список
    morph = pymorphy2.MorphAnalyzer()
    for i in requirement_list_lower:
        words_lemmed.append(morph.parse(i)[0].normal_form) # приводим слова к лемме


    new_words = [word for word in words_lemmed if word not in other_words] # исключаем слова из стоп-листа

    # c = collections.Counter()
    # for i in new_words:
    #     c[i] +=1


    c = collections.Counter(new_words) #  делаем словарь, который позволяет считать кол-во объектов

    results = c.most_common(10) # возвращает список кортежей из наиболее часто встречающихся элементов, в порядке убывания встречаемости

    # преобразовываем список кортежей в список (убираем цифры, который обозначают частоту встречаемости)

    results_list = []
    for tuple_ in results:
        for i in range(len(tuple_)+1):
            if i == 0:
                results_list.append(tuple_[i])

    # возвращаем общее количество найденных вакансий, список навыков
    return results_all, results_list