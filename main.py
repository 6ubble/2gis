from parser import DgisParser
from excel_writer import save_to_excel

def main():
    city_name = input("Введите город (например, 'Москва'): ").strip()
    query = input("Введите запрос (например, 'красота', 'кафе', 'ремонт'): ").strip()

    parser = DgisParser()

    city_id = parser.get_city_id(city_name)

    print("\n Получаем компании (только с сайтами)...")
    companies = parser.get_companies_with_sites(query, city_id)

    save_to_excel(companies, query, city_id)
    print(f"\n Завершено! Найдено {len(companies)} компаний с сайтом.")
    print(f" Всего запросов к API: {parser.request_count}")

if __name__ == "__main__":
    main()