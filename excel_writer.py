import pandas as pd
import os

def save_to_excel(data, query, city_name):
    if not data:
        print("Нет данных для сохранения.")
        return

    os.makedirs("results", exist_ok=True)
    df = pd.DataFrame(data)

    filename = f"results/2gis_{query}_{city_name}.xlsx"

    df.to_excel(filename, index=False)
    print(f"Сохранено {len(data)} записей в файл: {filename}")