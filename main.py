from parser import DgisParser
from excel_writer import save_to_excel

def main():
    city_name = input("Введите город: ").strip()
    query = input("Введите запрос: ").strip()
    
    max_pages = int(input("Введите максимальное количество страниц: "))
    page_size = int(input("Введите количество объектов на странице: "))

    parser = DgisParser(max_pages=max_pages, page_size=page_size)

    city_id = parser.get_city_id(city_name)

    companies = parser.get_companies_with_sites(query, city_id)

    save_to_excel(companies, query, city_name)
    print(f"\nЗавершено! Найдено {len(companies)} компаний с сайтом.")
    print(f"Всего запросов к API: {parser.request_count}")

if __name__ == "__main__":
    main()