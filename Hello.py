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

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )


def display_info(info_dict, header):
    st.header(header)
    df = pd.DataFrame(info_dict.items(), columns=["Параметр", "Значение"])
    st.table(df)

def calculate_taxes_and_profit(net_profit, renovation_cost, other_expenses):
    taxes_13_percent = net_profit * 0.13
    taxes_6_percent = net_profit * 0.06
    net_profit_after_taxes = net_profit - taxes_13_percent - taxes_6_percent
    return taxes_13_percent, taxes_6_percent, net_profit_after_taxes

def calculate_location_score(location_ratings):
    # Пример: Среднее арифметическое оценок по разным характеристикам
    return sum(location_ratings.values()) / len(location_ratings)

def main():
    st.title("Информация о проекте недвижимости")

    # Раздел 1: Общая информация
    general_info = {
        "Адрес": "Улица Примерная, д. 123, кв. 456",
        "Дата публикации": "01.01.2023",
        "Количество просмотров общее": 1000,
        "Количество просмотров за день": 50,
        "Цена покупки": 2000000,
        "Цена продажи": 2200000,
        "Цена за квм": 40000,
        "Продавец": "Иванов Иван",
        "Время до метро": "10 минут",
        "Расстояние до метро": "500 метров",
    }
    display_info(general_info, "1. Общая информация")

    # Раздел 2: Информация о квартире
    flat_info = {
        "Состояние": "Хорошее",
        "Комнаты": 2,
        "Общая площадь": 60,
        "Кухня": 10,
        "Балкон": "Есть",
        "Этаж": 5,
        "Серия дома": "Кирпичная",
        "Тип дома": "Многоквартирный",
        "Год постройки": 2000,
        "Капитальный ремонт": "Да",
    }
    display_info(flat_info, "2. Информация о квартире")

    # Раздел 3: Смета проекта
    st.header("3. Смета проекта")
    renovation_cost_per_sqm = st.number_input("Стоимость ремонта за квадратный метр", min_value=0, value=1000)
    total_area = flat_info["Общая площадь"]
    renovation_cost = total_area * renovation_cost_per_sqm
    other_expenses = st.number_input("Прочие расходы", min_value=0)
    deal_price = general_info["Цена продажи"]
    net_profit = deal_price - (general_info["Цена покупки"] - st.number_input("Торг", min_value=0)) - renovation_cost - other_expenses
    taxes_13_percent, taxes_6_percent, net_profit_after_taxes = calculate_taxes_and_profit(net_profit, renovation_cost, other_expenses)

    # Вывод результатов
    st.subheader("Смета проекта")
    st.write(f"Стоимость ремонта: {renovation_cost}")
    st.write(f"Прочие расходы: {other_expenses}")
    st.write(f"Прибыль до налогов: {net_profit}")
    st.write(f"Налоги при ставке 13%: {taxes_13_percent}")
    st.write(f"Налоги при ставке 6%: {taxes_6_percent}")
    st.write(f"Чистая прибыль: {net_profit_after_taxes}")

    # Раздел 4: Доходность проекта
    st.header("4. Доходность проекта")
    roi = (net_profit_after_taxes / (renovation_cost + other_expenses)) * 100
    irr = (net_profit_after_taxes / (renovation_cost + other_expenses)) * (12 / st.number_input("Срок проекта (в месяцах)", min_value=1)) * 100
    gap = general_info["Цена продажи"] / general_info["Цена покупки"]
    st.write(f"ROI (рентабельность инвестиций): {roi}%")
    st.write(f"IRR (внутренняя норма доходности): {irr}%")
    st.write(f"GAP (На сколько ремонта увеличит стоимость квартиры): {gap}")

    # Раздел 5: Оценка локации
    st.header("5. Оценка локации")
    location_ratings = {
        "Близость к общественному транспорту": st.slider("Оценка близости", min_value=1, max_value=10, value=5),
        "Инфраструктура района": st.slider("Оценка инфраструктуры", min_value=1, max_value=10, value=5),
        # Добавьте дополнительные параметры для оценки локации
    }
    location_score = calculate_location_score(location_ratings)
    st.write(f"Общая оценка локации: {location_score}")

if __name__ == "__main__":
    main()

    st.sidebar.success("Select a demo above.")



if __name__ == "__main__":
    run()
