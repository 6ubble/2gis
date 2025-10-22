import requests
from config import API_KEY, BASE_URL_V3
import time


class DgisParser:
    def __init__(self):
        self.request_count = 0

    def get_city_id(self, city_name):
        url = f"{BASE_URL_V3}/items"
        params = {"q": city_name, "key": API_KEY}

        self.request_count += 1
        response = requests.get(url, params=params)
        data = response.json()

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
            print(f"Не найден явный тип 'city', используем первый результат: {city['name']}")

        print(f"Найден город: {city['name']} (ID: {city['id']})")
        return city["id"]

    def get_companies_with_sites(self, query, city_id):
        url = f"{BASE_URL_V3}/items"
        params = {
            "q": query,
            "city_id": city_id,
            "has_site": "true",
            "key": API_KEY,
            "fields": "items.point,items.address_name,items.contact_groups,items.links"
        }

        all_companies = []
        page = 1

        while True:
            params["page"] = page
            self.request_count += 1

            response = requests.get(url, params=params)
            data = response.json()

            items = data.get("result", {}).get("items", [])
            if not items:
                break

            for item in items:
                site = ""
                links = item.get("links", [])
                if isinstance(links, list):
                    for l in links:
                        if isinstance(l, dict) and l.get("type") == "website":
                            site = l.get("url", "")
                            break
                        elif isinstance(l, str) and l.startswith("http"):
                            site = l
                            break

                company = {
                    "Название": item.get("name"),
                    "Адрес": item.get("address_name"),
                    "Сайт": site,
                    "ID": item.get("id"),
                    "Координаты": f"{item.get('point', {}).get('lat')}, {item.get('point', {}).get('lon')}",
                    "Тип": item.get("type"),
                    "Телефоны": ", ".join(
                        [c["value"] for g in item.get("contact_groups", [])
                         for c in g.get("contacts", []) if c["type"] == "phone"]
                    ),
                    "Email": ", ".join(
                        [c["value"] for g in item.get("contact_groups", [])
                         for c in g.get("contacts", []) if c["type"] == "email"]
                    )
                }
                all_companies.append(company)

            if not data["result"].get("next_page"):
                break

            page += 1
            time.sleep(0.5)

        return all_companies