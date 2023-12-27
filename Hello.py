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

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

# Загрузка данных из CSV
@st.cache
def load_data():
    data = pd.read_csv('flats_with_preds.csv')  # Замените 'your_data.csv' на имя вашего файла CSV
    return data

data = load_data()
print(data.columns)

# Заголовок приложения
st.title('Real Estate Explorer')

# Сайдбар для выбора квартиры
selected_flat_id = st.sidebar.selectbox('Выберите квартиру', data['id'])

# Отображение характеристик выбранной квартиры
selected_flat = data[data['id'] == selected_flat_id].squeeze()
st.subheader(f'Характеристики квартиры {selected_flat_id}')
st.write(selected_flat)

# Отображение карты с маркерами для всех квартир
st.subheader('Карта с маркерами для всех квартир')
m = folium.Map(location=[55.75, 37.61], zoom_start=10)  # Начальные координаты карты
for index, flat in data.iterrows():
    folium.Marker([flat['lat'], flat['lon']],
                  popup=f"{flat['city']}, {flat['price_sq']} руб/м²",
                  icon=folium.Icon(color='blue')).add_to(m)

# Отображение карты
folium_static(m)


if __name__ == "__main__":
    main()

    st.sidebar.success("Select a demo above.")



if __name__ == "__main__":
    run()
