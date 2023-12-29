# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger
import pandas as pd
import folium
from streamlit_folium import folium_static
from streamlit_folium import st_folium
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import seaborn as sns
# Установка параметров страницы для отображения во весь экран
st.set_page_config(layout='wide')
LOGGER = get_logger(__name__)
# Загрузка данных из CSV___
@st.cache
def load_data():
    data = pd.read_csv('test_flats_data.csv')  # Замените 'your_data.csv' на имя вашего файла CSV
    return data
data = load_data()
print(data.columns)
# Заголовок приложения
st.subheader('Расчет проекта')

# Сайдбар для выбора города
selected_city = st.sidebar.selectbox('Выберите город', data['city'].unique())

# Фильтрация данных по выбранному городу
filtered_data = data[data['city'] == selected_city]

# Сайдбар для выбора квартиры из отфильтрованных данных
selected_flat_id = st.sidebar.selectbox('Выберите квартиру', filtered_data['id'])

# Допущения
renovation_cost_sq = st.sidebar.number_input('Стоимость ремонта за квадратный метр:', 35000 )
# Расчет комиссии агента
agent_commission = st.sidebar.number_input('Стоимость комиссии агента:', 100000 )

# Вывод адреса и района выбранной квартиры
selected_flat = data[data['id'] == selected_flat_id].squeeze()
st.write(f'{selected_flat["city"]}')
st.title(f'{selected_flat["street"]}, {selected_flat["address"]}')
#{selected_flat["floor"]} ком.кв., {selected_flat["city"]}, Площадь: {selected_flat["area"]}
st.write(f'Метро: {selected_flat["all_data.geo.undergrounds[0].name"]}, {selected_flat["all_data.geo.undergrounds[0].time"]} мин.')

# Расчет затрат на ремонт
renovation_cost = selected_flat['area'] * renovation_cost_sq
# Ожидаемая стоимость продажи (может быть заменена на реальные данные)
expected_sale_price = selected_flat['predicted_price']
# Расчет общих затрат и прибыли
total_expenses = selected_flat['price_sq'] + renovation_cost + agent_commission
profit = expected_sale_price - total_expenses

st.subheader(f'Цена входа: {selected_flat["price_sq"] * selected_flat["area"]} руб')
st.subheader(f'Цена выхода потенциальная: {expected_sale_price * selected_flat["area"]} руб')

col1, col2, col3, col4 = st.columns(4)
col1.metric("ROI","20%", "4%")
col2.metric("Индекс транспортной доступности", "5", "10")
col3.metric("Индекс доступности инфраструктуры", "6", "10")
col4.metric("Тренд", "4%", "100%")

# Отображение характеристик выбранной квартиры
selected_flat = data[data['id'] == selected_flat_id].squeeze()
st.subheader(f'Основные характеристики квартиры {selected_flat_id}')
st.write(selected_flat)

# Флиппинг-проект
st.markdown("---")

st.subheader(f'Финансовые показатели')
# Отображение результатов
st.subheader(f'Цена входа: {selected_flat["price_sq"]} руб')
st.subheader(f'Цена выхода потенциальная: {expected_sale_price} руб')
st.subheader(f'Затраты на ремонт: {renovation_cost} руб')
st.subheader(f'Комиссия агента: {agent_commission} руб')
st.subheader(f'Общие затраты: {total_expenses} руб')
st.subheader(f'Прибыль: {profit} руб')

st.subheader('Анализ стоимости квартиры')
# График цен за квадратный метр
chart, ax = plt.subplots(figsize=(8, 6))

# Фоновый график для всех квартир
sns.stripplot(
    data=data,
    y='price_sq',
    color='white',
    jitter=0.3,
    size=8,
    linewidth=1,
    edgecolor='gainsboro',
    alpha=0.7
)

# Выделение выбранной квартиры
sns.stripplot(
    data=data[data['id'] == selected_flat_id],
    y='price_sq',
    color='red',
    size=12,
    linewidth=1,
    edgecolor='black',
    label=f'Selected Flat {selected_flat_id}'
)

# Оформление графика
avg_price_m2 = data['price_sq'].median()
q1_price_m2 = data['price_sq'].quantile(0.25)
q3_price_m2 = data['price_sq'].quantile(0.75)

ax.axhline(y=avg_price_m2, color='#DA70D6', linestyle='--', lw=0.75)
ax.axhline(y=q1_price_m2, color='white', linestyle='--', lw=0.75)
ax.axhline(y=q3_price_m2, color='white', linestyle='--', lw=0.75)

ax.text(1.15, q1_price_m2, 'Q1', ha='center', va='center', color='white', fontsize=8, fontweight='bold')
ax.text(1.35, avg_price_m2, 'Median', ha='center', va='center', color='#DA70D6', fontsize=8, fontweight='bold')
ax.text(1.15, q3_price_m2, 'Q3', ha='center', va='center', color='white', fontsize=8, fontweight='bold')
ax.fill_betweenx([q1_price_m2, q3_price_m2], -2, 1, alpha=0.2, color='gray')
ax.set_xlim(-1, 1)

# Отображение графика
ax.set_ylabel('Стоимость квартиры за квадратный метр (R$)')
ax.set_title('Стоимость выбранной квартиры за квадратный метр')
ax.legend()
st.pyplot(chart)

# Разделение между графиком и таблицей
st.markdown("---")

# Таблица конкурентов в радиусе 1500 метров
st.subheader('Таблица конкурентов в радиусе 1500 метров')
# Фильтрация данных для отображения только конкурентов в радиусе 1500 метров
competitors_data = filtered_data.copy()
competitors_data['Distance (meters)'] = competitors_data.apply(
    lambda row: geodesic((row['lat'], row['lon']), (selected_flat['lat'], selected_flat['lon'])).meters,
    axis=1
)
competitors_data = competitors_data[competitors_data['Distance (meters)'] <= 1500]

# Выделение выбранной квартиры в таблице
competitors_data.loc[competitors_data['id'] == selected_flat_id, 'Selected'] = 'Selected'

# Отображение таблицы
st.dataframe(competitors_data[['id', 'city', 'price_sq', 'Distance (meters)', 'Selected']].reset_index(drop=True))

# Карта конкурентов в радиусе 1500 метров
st.subheader('Карта конкурентов в радиусе 1500 метров')
m = folium.Map(location=[selected_flat['lat'], selected_flat['lon']], zoom_start=14, tooltip=True)

# Перебор всех квартир и добавление маркеров в радиусе 1500 метров
for index, flat in competitors_data.iterrows():
    # Определение цвета маркера для выбранной квартиры
    marker_color = 'red' if flat['id'] == selected_flat_id else 'blue'
    
    folium.Marker([flat['lat'], flat['lon']],
                  popup=f"{flat['city']}, {flat['price_sq']} руб/м²",
                  tooltip=f"{flat['city']}, {flat['price_sq']} руб/м²",
                  icon=folium.Icon(color=marker_color),
                  auto_open=True).add_to(m)

# Отображение карты
folium_static(m)
