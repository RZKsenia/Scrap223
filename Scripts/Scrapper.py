import urllib.request as rq
import urllib.parse as prs
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
from urllib.parse import quote
import pandas as pd

class Scrapper(object):
    """
    Класс скрапинга сайтов
    """
    def read_search_page(self, page_num):
        """
        открывает страницу
        :return:
        возвращает ссылки со страниц поиска
        """
        list_url_result = pd.Series([]) # здесь будет список ссылок на страницы репрессированных

        # параметры поиска:
        params = {"olsearch-name": "*",
                  "olsearch-birth_min": "",
                  "olsearch-birth_max": "",
                  "olsearch-death_min": "",
                  "olsearch-death_max": "",
                  "olsearch-birthplace": "",
                  "olsearch-liveplace": "",
                  "olsearch-nationality": "",
                  "olsearch-social": "",
                  "olsearch-profession": "",
                  "olsearch-deathplace": "",
                  "olsearch-burialplace": "",
                  "olsearch-body": "",
                  "olsearch-categories": "",
                  "olsearch-arrest_min": "",
                  "olsearch-arrest_max": "",
                  "olsearch-indictment": "",
                  "olsearch-conviction_min": "",
                  "olsearch-conviction_max": "",
                  "olsearch-conviction-org": "",
                  "olsearch-sentence": "",
                  "olsearch-detentionplace": "",
                  "olsearch-release_min": "",
                  "olsearch-release_max": "",
                  "olsearch-execution_min": "",
                  "olsearch-execution_max": "",
                  "olsearch-archive-case-number": "",
                  "olsearch-run": "1",
                  "olsearch-advform": "1"}


        if page_num !=1:
            params["olsearch-page"] = str(page_num)

        url = ("https://ru.openlist.wiki/{0}").format(quote("Служебная"))
        url = url + ":OlSearch?"
        url = url + prs.urlencode(params)

        try:
            html = rq.urlopen(url=url)
        except HTTPError as e:
            print ("не удалось открыть страницу")
            return None
        try:
            bsObj = BeautifulSoup(html.read(), features="html.parser")
        except AttributeError as e:
            return None

        td = bsObj.find("table")
        href = td.find_all("a")

        # получаем ссылки на страницы:
        for h in href:
            ref = h.get('href')
            list_url_result[list_url_result.size] = ref
            print('Добавляем ссылки на страницы...')

        print('Все ссылки собраны и готовы для отработки')
        return list_url_result

    def scrap_page(self, href, page_num):
        """
        Скрапинг страницы отдельного человека
        :param href: список ссылок на страницы
        :return:
        """
        cntr = 0
        if page_num == 1:
            result_df = pd.DataFrame()
        else:
            result_df = pd.read_csv(r'C:/Python_projects/Scrap223/Data/repression.csv', dtype='str') # для вывода результата

        for h in href:
            try:
                url = 'https://ru.openlist.wiki' + h # дополняем адресом сайта слева
                # print('url = ' + url)
                html = rq.urlopen(url=url) # открываем страницу
                bsObj = BeautifulSoup(html.read(), features="html.parser") # парсим страницу
                person_block = bsObj.find('div', {'id':'custom-person'})
                # если найден такой блок, значит это страница человека:
                if person_block is not None:
                    name_of_person = bsObj.find('h1').get_text() # получаем имя человека

                    prop_ch = bsObj.find('div', {'id':'custom-person'}) # блок с информацией о человеке
                    prop_titles = prop_ch.ul.find_all('span') # заголовки данных
                    #person_properties = prop_ch.ul.find_all('b') # в этих блоках находится информация о человеке

                    titles = ['Имя:']
                    values = [str(name_of_person)]
                    # заполняем заголовки данных
                    for t in prop_titles:
                        cur_title = str(t.get_text())
                        titles.append(cur_title)
                        p = t.parent
                        person_properties = p.find_all('b')
                        if person_properties != []:
                            for p in person_properties:
                                cur_value = str(p.get_text())
                                values.append(cur_value)
                        else:
                            values.append("-")
                        #print(t.parent)
                    # заполняем данные
                    #for p in person_properties:
                    #    cur_value = str(p.get_text())
                    #    values.append(cur_value)
                    # собираем всё в словарь
                    dict_values = dict(zip(titles, values))
                    # создаём объект на основе данных
                    df = pd.DataFrame(dict_values, index=[0], dtype=str)
                    # добавляем объект в результат
                    result_df = pd.concat([result_df, df])
                    result_df.to_csv(r'C:/Python_projects/Scrap223/Data/repression.csv', index=False)

                    print(name_of_person)
                    print(titles)
                    print(values)
                    print('===============================================')
                    # print('Отработана ссылка ' + url)

            except HTTPError:
                pass
            #except ValueError:
            #    pass
            except AttributeError:
                pass
            except URLError:
                pass


scr = Scrapper()
for page_num in range(1,301): # всего страниц 32220
    print ('Обрабатывается страница номер ' + str(page_num))
    href = scr.read_search_page(page_num= page_num) # получаем список ссылок на страницы людей
    scr.scrap_page(href, page_num= page_num) # получаем данные для всех людей со страницы
    print('станица полностью обработана')