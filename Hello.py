import streamlit as st
from streamlit.logger import get_logger
import pandas as pd
import folium
from streamlit_folium import folium_static
from geopy.distance import geodesic
import seaborn as sns
from streamlit_extras.metric_cards import style_metric_cards
import streamlit.components.v1 as components

# Установка параметров страницы для отображения во весь экран
st.set_page_config(layout='wide')

LOGGER = get_logger(__name__)

# Загрузка данных из CSV
@st.cache_data
def load_data():
    data = pd.read_csv('test_flats_data.csv')
    return data

data = load_data()

# Заголовок приложения
st.title('📊 Анализ инвестиционного проекта недвижимости')

# Сайдбар для выбора города и квартиры
st.sidebar.header('Фильтры')


selected_city = st.sidebar.selectbox('Выберите город', data['city'].unique())
filtered_data = data[data['city'] == selected_city]
selected_flat_id = st.sidebar.selectbox('Выберите квартиру', filtered_data['id'])

# Допущения
refresh_cost_sq = st.sidebar.number_input('Стоимость ремонта за квадратный метр:', 35000)
agent_commission = st.sidebar.number_input('Стоимость комиссии агента:', 100000)

# Вывод информации о выбранной квартире
selected_flat = filtered_data[filtered_data['id'] == selected_flat_id].squeeze()
st.header(f"{selected_flat['city']}, {selected_flat['street']}, {selected_flat['address']}")

# Расчет затрат на ремонт и общую стоимость
refresh_cost = selected_flat['area'] * refresh_cost_sq
expected_sale_price = selected_flat['predicted_price']
total_expenses = selected_flat['price_sq'] + refresh_cost + agent_commission
profit = expected_sale_price - total_expenses

# Форматируем числа и заменяем точки на запятые
price_in = f'{selected_flat["bargainTerms.price"]:,}'.replace(",", " ").replace(".", ",") + " руб."
price_out = f'{(expected_sale_price * selected_flat["area"]):,}'.replace(",", " ").replace(".", ",") + " руб."
profit_display = f'{profit:,}'.replace(",", " ").replace(".", ",") + " руб."

# Отражение финансовых показателей
st.subheader('Финансовые показатели')
col1, col2, col3,col4 = st.columns(4)
col1.metric("💰 **Цена входа:**", price_in)
col2.metric("💸 **Цена выхода:**", price_out)
col3.metric("💸 **Прибыль:**", profit_display)
col4.metric("📊 **Тренд рынка**", "4%", "100%")
# Отображение метрик
col1, col2, col3 = st.columns(3)
col1.metric("🔄 **ROI**", "20%", "4%")
col2.metric("🚌 **Индекс транспортной доступности**", "5", "10")
col3.metric("📍 **Индекс доступности инфраструктуры**", "6", "10")

style_metric_cards()

# Отображение характеристика квартиры
st.subheader('Характеристики квартиры')
st.write(f"*Комнат:* ***{selected_flat['rooms']}***")
st.write(f"*Этаж:* ***{selected_flat['floor']} из {selected_flat['house_floors']}***")
st.write(f"*Площадь:* ***{selected_flat['area']} м²***")
st.write(f"*Жилая площадь:* ***{selected_flat['all_data.livingArea']} м²***")
st.write(f"*Площадь кухни:* ***{selected_flat['kitchen_area']} м²***")
st.write(f"*Санузел:* ***{selected_flat['bathroom_type']}***")
st.write(f"*Лифт:* ***пассажирский {selected_flat['lifts']} грузовой {selected_flat['freight_lifts']}***")
st.write(f"*Материал дома:* ***{selected_flat['house_wall_type']}***")
st.write(f"*Год постройки:* ***{selected_flat['build_year']}***")

# Анализ стоимости объекта недвижимости
st.subheader('Анализ стоимости объекта недвижимости')

# Отображение таблицы конкурентов в радиусе 1500 метров
st.markdown("---")
tab1, tab2 = st.tabs(["Карта конкурентов", "Таблица конкурентов"])

competes_data = filtered_data.copy()
competes_data['Расстояние (метры)'] = competes_data.apply(
    lambda row: geodesic((row['lat'], row['lon']), (selected_flat['lat'], selected_flat['lon'])).meters,
    axis=1
)
competes_data = competes_data[competes_data['Расстояние (метры)'] <= 1500]
competes_data.loc[competes_data['id'] == selected_flat_id, 'Выбрано'] = "Выбранные"
competes_data['Разница в цене'] = competes_data['price_sq'] - selected_flat['price_sq']

with tab2:
    st.subheader('Таблица конкурентов')
    st.dataframe(competes_data[[
        'city', 'street', 'address', 'rooms', 'area', 'kitchen_area', 'renovation', 'floor', 'house_floors', 
        'house_wall_type', 'build_year', 'time_on_foot_to_subway', 'Расстояние (метры)', 'price_sq', 
        'bargainTerms.price', 'Разница в цене', 'Выбрано'
    ]].reset_index(drop=True))

with tab1:
    st.subheader('Карта конкурентов')
    m = folium.Map(location=[selected_flat['lat'], selected_flat['lon']], zoom_start=14)
    for index, flat in competes_data.iterrows():
        marker_color = 'red' if flat['id'] == selected_flat_id else 'blue'
        folium.Marker([flat['lat'], flat['lon']],
                      popup=f"{flat['city']}, {flat['price_sq']} руб/м²",
                      tooltip=f"{flat['city']}, {flat['price_sq']} руб/м²",
                      icon=folium.Icon(color=marker_color)).add_to(m)
    folium_static(m, width=1000, height=600)

# Интеграция с Яндекс.Картами
st.subheader('Яндекс.Карта')
YOUR_APIKEY = "14a66a7c-9302-4fbb-9102-44edd5c98dc2"
location_yandex_map = [selected_flat['lat'], selected_flat['lon']]

yandex_map_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1" />
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap" rel="stylesheet">
<script src="https://api-maps.yandex.ru/2.1/?apikey={YOUR_APIKEY}&lang=ru_RU" type="text/javascript"></script>
<style>
html, body, #app {{ width: 100%; height: 100%; margin: 0; padding: 0; font-family: Arial, Helvetica, sans-serif; }}
</style>
</head>
<body>
<div id="app" style="width: 100%; height: 600px;"></div>
<script>
ymaps.ready(init);
function init() {{
    var map = new ymaps.Map('app', {{ center: {location_yandex_map}, zoom: 13 }});
    var selectedMarker = new ymaps.Placemark([{location_yandex_map[0]}, {location_yandex_map[1]}], {{
        balloonContent: '<strong>Выбранный объект</strong><br/>Стоимость за кв.м.: {selected_flat["price_sq"]} руб',
        iconColor: 'red'
    }});
    map.geoObjects.add(selectedMarker);
    var competesData = {competes_data[['lat', 'lon', 'id', 'price_sq']].to_json(orient='records', date_format='iso')};
    for (var i = 0; i < competesData.length; i++) {{
        var competitorMarker = new ymaps.Placemark(
            [competesData[i]['lat'], competesData[i]['lon']],
            {{
                balloonContent: '<strong>Competitor Property</strong><br/>Cost per sq.m.: ' + competesData[i]['price_sq'] + ' rub'
            }}
        );
        map.geoObjects.add(competitorMarker);
    }}
}}
</script>
</body>
</html>
"""

components.html(yandex_map_html, height=600)


st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
    * {
        font-family: 'Montserrat', sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
