import pandas as pd
from statsmodels.stats.proportion import proportions_ztest, confint_proportions_2indep

# очистка данных от ошибок
df = pd.read_csv('../База данных/data.csv')
df = df[
    ((df['group'] == 'control') & (df['landing_page'] == 'old_page')) |
    ((df['group'] == 'treatment') & (df['landing_page'] == 'new_page'))
]
df = df.drop_duplicates(subset=['user_id'])

# z-тест
grouped = df.groupby('group')
conv_counts = grouped['converted'].sum()  # количества конверсий
user_counts = grouped['converted'].count()  # количества пользователей
convs = conv_counts / user_counts  # конверсии
z, p = proportions_ztest(conv_counts, user_counts)

# расчёт доверительного интервала
ci = confint_proportions_2indep(
    count1=conv_counts['treatment'],
    nobs1=user_counts['treatment'],
    count2=conv_counts['control'],
    nobs2=user_counts['control']
)

# результат
print(f'\nКонверсия контрольной группы: {round(convs['control'] * 100, 2)}%')
print(f'Конверсия тестовой группы: {round(convs['treatment'] * 100, 2)}%')
print(f'Разница: {round((convs['treatment'] - convs['control']) * 100, 2)}%')

# проверка гипотезы
alpha = 0.05
print(f'\nz = {round(z, 2)}')
print(f'p-value = {round(p, 2)}')
print('Отклоняем нулевую гипотезу' if p < alpha else 'Не отклоняем нулевую гипотезу')

# доверительный интервал
print(f'\n95%-й доверительный интервал разницы: [{round(ci[0] * 100, 2)};{round(ci[1] * 100, 2)}]%')
print('Доверительный интервал содержит 0' if ci[0] * ci[1] < 0 else 'Доверительный интервал не содержит 0')

# вывод
print('\nВывод: собранные данные не дают оснований полагать, что после изменения конверсия вырастет')