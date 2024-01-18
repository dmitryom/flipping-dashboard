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
from streamlit_extras.metric_cards import style_metric_cards


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

# Сайдбар для выбора объекта недвижимости из отфильтрованных данных
selected_flat_id = st.sidebar.selectbox('Выберите квартиру', filtered_data['id'])

# Допущения
renovation_cost_sq = st.sidebar.number_input('Стоимость ремонта за квадратный метр:', 35000 )
# Расчет комиссии агента
agent_commission = st.sidebar.number_input('Стоимость комиссии агента:', 100000 )

# Вывод адреса и района выбранного объекта недвижимости
selected_flat = data[data['id'] == selected_flat_id].squeeze()
st.subheader(f'{selected_flat["city"]}')
st.title(f'🏠 {selected_flat["street"]}, {selected_flat["address"]}')
#{selected_flat["floor"]} ком.кв., {selected_flat["city"]}, Площадь: {selected_flat["area"]}
st.write(f'Ⓜ️ Метро: {selected_flat["all_data.geo.undergrounds[0].name"]}, {selected_flat["all_data.geo.undergrounds[0].time"]} мин.')
st.write(f'{selected_flat["all_data.geo.address[2].title"]}, {selected_flat["all_data.geo.address[1].title"]}')
# Расчет затрат на ремонт
renovation_cost = selected_flat['area'] * renovation_cost_sq
# Ожидаемая стоимость продажи (может быть заменена на реальные данные)
expected_sale_price = selected_flat['predicted_price']
# Расчет общих затрат и прибыли
total_expenses = selected_flat['price_sq'] + renovation_cost + agent_commission
profit = expected_sale_price - total_expenses

# components

col1, col2, col3, col4 = st.columns(4)
col1.metric("🔄 ROI","20%", "4%")
col2.metric("🚌 Индекс транспортной доступности", "5", "10")
col3.metric("📍 Индекс доступности инфраструктуры", "6", "10")
col4.metric("📊 Тренд", "4%", "100%")
style_metric_cards()


col1, col2, col3, col4 = st.columns(4)
col1.metric(
    "💰 Цена входа:",
    f'{selected_flat["bargainTerms.price"]} руб.',
    help="Цена в объявлении",
    )
col2.metric(
    "💸 Цена выхода потенциальная:",
    f'{expected_sale_price * selected_flat["area"]} руб.',
    help="Цена выхода по оценке искусственного интеллекта (ИИ)",
    )
col3.metric(
    "💸 Прибль:",
    f'{profit} руб.',
    help="Прибль",
    )



# Отображение характеристик выбранного объекта недвижимости
selected_flat = data[data['id'] == selected_flat_id].squeeze()
col1, col2, col3 = st.columns(3)
with col1:
    st.subheader(f'1. Характеристики')
    st.write(f'* Комнат: {selected_flat["rooms"]}')
    st.write(f'* Общая площадь: {selected_flat["area"]}')
    st.write(f'* Жилая площадь: {selected_flat["all_data.livingArea"]}')
    st.write(f'* Площадь кухни: {selected_flat["kitchen_area"]}')
    st.write(f'* Этаж: {selected_flat["floor"]} из {selected_flat["house_floors"]}')
    st.write(f'* Санузел: {selected_flat["bathroom_type"]}')
    st.write(f'* Лифт: пассажирский {selected_flat["lifts"]} грузовой {selected_flat["freight_lifts"]} ')
    st.write(f'* Материал дома: {selected_flat["house_wall_type"]}')
    st.write(f'* Год постройки: {selected_flat["build_year"]}')
with col2:
    st.subheader(f'2. Финансовые показатели')
    # Отображение результатов
    st.write(f'* Цена входа: {selected_flat["bargainTerms.price"]} руб.')
    st.write(f'* Цена выхода потенциальная: {expected_sale_price * selected_flat["area"]} руб.')
    st.write(f'* Затраты на ремонт: {renovation_cost} руб.')
    st.write(f'* Комиссия агента: {agent_commission} руб.')
    st.write(f'* Общие затраты: {total_expenses} руб.')
    st.write(f'* Прибыль: {profit} руб.')

st.subheader(f'3. Анализ стоимости объекта недвижимости')
# График цен за квадратный метр

# Выберите квартиру и получите соответствующие данные
selected_flat = data[data['id'] == selected_flat_id].squeeze()

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

# Выделение выбранного объекта недвижимости в таблице
competitors_data.loc[competitors_data['id'] == selected_flat_id, 'Selected'] = 'Selected'
st.dataframe(competitors_data[['id', 'city', 'price_sq', 'Distance (meters)', 'Selected']].reset_index(drop=True))

# Карта конкурентов в радиусе 1500 метров
st.subheader('Карта конкурентов в радиусе 1500 метров')
m = folium.Map(location=[selected_flat['lat'], selected_flat['lon']], zoom_start=14, tooltip=True)

# Перебор всех объектов недвижимости и добавление маркеров в радиусе 1500 метров
for index, flat in competitors_data.iterrows():
    # Определение цвета маркера для выбранной объекта недвижимости
    marker_color = 'red' if flat['id'] == selected_flat_id else 'blue'
    
    folium.Marker([flat['lat'], flat['lon']],
                  popup=f"{flat['city']}, {flat['price_sq']} руб/м²",
                  tooltip=f"{flat['city']}, {flat['price_sq']} руб/м²",
                  icon=folium.Icon(color=marker_color),
                  auto_open=True).add_to(m)

# Отображение карты
folium_static(m, width=1000, height=600)
