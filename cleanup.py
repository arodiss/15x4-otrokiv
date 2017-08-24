import pandas as pd
import os


def get_conversion(id, name, responses):
    return 100 * sum(responses['lecture'] == name) / int(os.popen('cat data/raw/survey.log | grep "id {}" | wc -l'.format(id)).read())


youtube = pd.read_csv('data/raw/youtube.csv')
responses = pd.read_csv('data/raw/responses.csv')
del(responses['Timestamp'])
del(youtube['rating'])

youtube = youtube.replace("15 минут про говорящих обезьян", "monkey")
responses = responses.replace("15 минут о говорщих обезьянах", "monkey")
youtube = youtube.replace("15 минут про боль", "pain")
responses = responses.replace("15 минут о боли", "pain")
youtube = youtube.replace("15 минут про антибиотики", "antibiotics")
responses = responses.replace("15 минут об антибиотиках", "antibiotics")
youtube = youtube.replace("15 минут о викингах", "vikings")
responses = responses.replace("15 минут о викингах", "vikings")
youtube = youtube.replace("15 минут о бессмертии", "immortality")
responses = responses.replace("15 минут о бессмертии", "immortality")
youtube = youtube.replace("15 минут про мультики Дисней", "disney")
responses = responses.replace("15 минут о мультиках Дисней", "disney")
youtube = youtube.replace("15 минут об эволюционной экономике", "economics")
responses = responses.replace("15 минут об эволюционной экономике", "economics")
youtube = youtube.replace("15 минут про ВИЧ-диссидентство", "aids")
responses = responses.replace("15 минут о ВИЧ-диссидентах", "aids")
responses = responses.replace("Да, я в секте", 1)
responses = responses.replace("Нет, я только иногда смотрю ваши ролики / хожу на ивенты", 0)

responses = responses.rename(columns={
    'Какую лекцию вы посмотрели?': "lecture",
    'Как вам понравилась лекция': "score",
    'Лекция была познавательной? Вы узнали что-то новое и полезное?': "knowledge",
    'Материал научный? Нет ли логических ошибок, есть ли данные экспериментов и исследований?  ': "science",
    'Как дела с повествованием? Рассказ складывается в целостную и гладкую историю?': "narrative",
    'А что с развлекательность частью? Интересно ли слушать автора и вовлекаться в лекцию?': "fun",
    'Оцените качество слайдов': "slides",
    'Как вам кажется, лектор харизматичный? ': "charisma",
    'Оцените качество видео/звука в лекции': "video_sound",
    'Оцените, насколько лектор владеет материалом': "understanding",
    'Последний вопрос :) Вы сами из 15х4?': "in_15x4",
})
responses.to_csv('data/responses-norm.csv')

in_sect_responses = responses[responses['in_15x4'] == 1]
out_sect_responses = responses[responses['in_15x4'] == 0]

overall_means = responses.groupby('lecture').mean()
in_sect_means = in_sect_responses.groupby('lecture').mean()
out_sect_means = out_sect_responses.groupby('lecture').mean()

del(overall_means['in_15x4'])
del(in_sect_means['in_15x4'])
del(out_sect_means['in_15x4'])

in_sect_means.columns = ['in_' + str(col) for col in in_sect_means.columns]
out_sect_means.columns = ['out_' + str(col) for col in out_sect_means.columns]

youtube = youtube.set_index('title')
youtube.columns = ['youtube_' + str(col) for col in youtube.columns]
youtube['is_hard_science'] = 1
youtube.set_value('vikings', 'is_hard_science', 0)
youtube.set_value('disney', 'is_hard_science', 0)
youtube.set_value('economics', 'is_hard_science', 0)
youtube['conversion'] = 0
youtube.set_value('economics', 'conversion', get_conversion(80, 'economics', responses))
youtube.set_value('vikings', 'conversion', get_conversion(207, 'vikings', responses))
youtube.set_value('pain', 'conversion', get_conversion(75, 'pain', responses))
youtube.set_value('antibiotics', 'conversion', get_conversion(104, 'antibiotics', responses))
youtube.set_value('aids', 'conversion', get_conversion(94, 'aids', responses))
youtube.set_value('disney', 'conversion', get_conversion(82, 'disney', responses))
youtube.set_value('monkey', 'conversion', get_conversion(63, 'monkey', responses))
youtube.set_value('immortality', 'conversion', get_conversion(12, 'immortality', responses))


pd\
    .concat([youtube, overall_means, in_sect_means, out_sect_means], axis=1)\
    .to_csv('data/concatenated.csv', decimal=".")
