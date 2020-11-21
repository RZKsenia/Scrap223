import pandas as pd
from bokeh.document import document
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import gridplot

class repressionStat(object):
    """
    Статистика по репрессированным
    """
    df = pd.DataFrame()
    filename = r'C:/Python_projects/Scrap223/Data/repression.csv'
    clmns = pd.Series()

    def uploadData(self):
        self.df = pd.read_csv(self.filename)

    def clearData(self, what_to_replace, new_value, regex=False):
        """
        Функция очистки данных
        :param what_to_replace: список строк - значений, которые нужно заменить. Если regex=True, то здесь будет
        регулярное выражение в списке
        :param new_value: на что заменить - строка
        :param regex: использовать или нет регулярные выражения
        :return: ничего не возвращает
        """
        self.df = self.df.replace(to_replace=what_to_replace,
                                  value=new_value,
                                  regex=regex)
        self.df.to_csv(self.filename, index=False)
        print('Очистка данных завершена')

    def stat_by_column(self, column_title):
        """
        Количественная статистика по столбцу
        Пустые значения не учитываются в подсчёте
        :return:
        """
        s = self.df[[column_title]].dropna()
        return s.value_counts(), [x[0] for x in s.value_counts().index.to_list()]

    def build_bokeh_vbar(self, data_frame, plot_width, plot_height, plot_title, x_range,
                         x_label_orientation, y_label_orientation, x_axis_title, y_axis_title):
        p = figure(
            x_range=x_range,
            plot_width=plot_width,
            plot_height=plot_height,
            title=plot_title,
            background_fill_color=colors['background']
            )
        p.title.text_font_size = '20px'
        p.title.text_color = colors['deep_dark']
        p.vbar(
            x=x_range,
            top=data_frame,
            width=0.5,
            color=colors['dark']
                )
        p.xaxis.axis_label = x_axis_title
        p.xaxis.major_label_orientation = x_label_orientation
        p.xgrid.grid_line_color = colors['medium']
        p.ygrid.grid_line_color = colors['medium']
        p.yaxis.axis_label = y_axis_title
        p.yaxis.major_label_text_color = colors['deep_dark']
        p.yaxis.major_label_orientation = y_label_orientation

        return p

colors = {
    'background':'#f5f0ce',
    'light':'#dfc3c4',
    'medium':'#dfc3c4',
    'dark':'#585b56',
    'deep_dark':'#1b2326'
}

rep = repressionStat()
rep.uploadData() # загружаем данные

"""rep.clearData(what_to_replace=[
    'неграмотн.',
    'неграмотная'
                                ],
              new_value='неграмотный') # очистка данных"""

output_file('C:/Python_projects/Scrap223/Output/stat.html')
document.title = 'Статистика политических репрессий в СССР'

ser_gender, col_titles_gender = rep.stat_by_column('Пол:') # получаем данные и наименования

ser_nationality, col_titles_nationality = rep.stat_by_column('Национальность:')
ser_nationality.sort_values()
ser_nationality = ser_nationality.head(15) # берём только 15 самых распространённых национальностей
col_titles_nationality = col_titles_nationality[:15]

ser_education, col_titles_education = rep.stat_by_column('Образование:') # получаем данные и наименования
ser_education.sort_values()
ser_education = ser_education.head(10)
col_titles_education = col_titles_education[:10]

p = rep.build_bokeh_vbar(x_range=col_titles_gender,
                         plot_width=400,
                         plot_height=400,
                         plot_title='Репрессированные: пол',
                         data_frame=ser_gender,
                         x_label_orientation=0,
                         y_label_orientation=0,
                         x_axis_title='Пол',
                         y_axis_title='Кол-во репрессированных')

p_nationality = rep.build_bokeh_vbar(
                         x_range=col_titles_nationality,
                         plot_width=600,
                         plot_height=400,
                         plot_title='Репрессированные: национальности',
                         data_frame=ser_nationality,
                         x_label_orientation=45,
                         y_label_orientation=45,
                         x_axis_title='Национальность',
                         y_axis_title='Кол-во представителей национальности')

p_education = rep.build_bokeh_vbar(
                         x_range=col_titles_education,
                         plot_width=400,
                         plot_height=400,
                         plot_title='Репрессированные: образование',
                         data_frame=ser_education,
                         x_label_orientation=45,
                         y_label_orientation=45,
                         x_axis_title='Вид образования',
                         y_axis_title='Кол-во репрессированных')

show(gridplot([[p, p_nationality],[p_education]]))