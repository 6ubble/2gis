import requests
from config import API_KEY, BASE_URL_V3
import time
from typing import List, Dict


class DgisParser:
    def __init__(self, max_pages: int, page_size: int):
        self.request_count = 0
        self.max_pages = max_pages
        self.page_size = page_size
        self.delay = 0.3

    def get_city_id(self, city_name: str) -> str:
        url = f"{BASE_URL_V3}/items"
        params = {"q": city_name, "key": API_KEY}

        self.request_count += 1
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            raise ValueError(f"Ошибка при поиске города: {e}")

        items = data.get("result", {}).get("items", [])
        if not items:
            raise ValueError(f"Город '{city_name}' не найден.")

        city = next(
            (
                i for i in items
                if i.get("type") in ["adm_div.city", "adm_div.region", "adm_div.settlement"]
            ),
            None
        )

        if not city:
            city = items[0]
            print(f"Не найден явный тип 'city', используем: {city.get('name')}")

        print(f"Найден город: {city['name']} (ID: {city['id']})")
        return city["id"]

    def get_companies_with_sites(self, query: str, city_id: str) -> List[Dict]:
        url = f"{BASE_URL_V3}/items"
        
        all_companies = []
        page = 1
        
        print(f"\nПолучаем компании (только с сайтами)...")

        while page <= self.max_pages:
            params = {
                "q": query,
                "city_id": city_id,
                "has_site": "true",
                "key": API_KEY,
                "page": page,
                "page_size": self.page_size,
                "fields": "items.point,items.address_name,items.links"
            }

            self.request_count += 1
            
            try:
                response = requests.get(url, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
            except requests.RequestException as e:
                print(f"Ошибка запроса на странице {page}: {e}")
                break

            items = data.get("result", {}).get("items", [])
            
            if not items:
                break

            for item in items:
                point = item.get("point", {})
                lat = point.get("lat", "")
                lon = point.get("lon", "")
                coords = f"{lat}, {lon}" if lat and lon else ""
                
                company = {
                    "Название": item.get("name", ""),
                    "Адрес": item.get("address_name", ""),
                    "ID": item.get("id", ""),
                    "Тип": item.get("type", ""),
                    "Координаты": coords,
                }
                all_companies.append(company)

            page += 1
            time.sleep(self.delay)

        return all_companies