import pandas as pd
from statsmodels.stats.proportion import proportions_ztest


# очистка данных от ошибок
df = pd.read_csv('../База данных/data.csv')
df = df[
    ((df['group'] == 'control') & (df['landing_page'] == 'old_page')) |
    ((df['group'] == 'treatment') & (df['landing_page'] == 'new_page'))
]
df = df.drop_duplicates(subset=['user_id'])

# z-тест
grouped = df.groupby('group')
conversion = grouped['converted'].mean()  # конверсия
convs = grouped['converted'].sum()  # количества конверсий
users = grouped['converted'].count()  # количества пользователей
z, p = proportions_ztest(convs, users)

# проверка гипотезы
alpha = 0.05
print('Отклоняем H0' if p < alpha else 'Не отклоняем H0')

# результат
print('Конверсия контрольной группы:', round(conversion['control'] * 100, 2), '%')
print('Конверсия экспериментальной группы:', round(conversion['treatment'] * 100, 2), '%')
print('Разница:', round((conversion['treatment'] - conversion['control']) * 100, 3), '%')
print('z =', round(z, 3))
print('p-value =', round(p, 3))