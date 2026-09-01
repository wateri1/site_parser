import os
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
token = os.getenv("APIFY_API_TOKEN", "")

print("Запускаем реальный парсинг через Apify API по запросу 'косметолог москва'...")
response = client.post("/api/parse", json={
    "query": "косметолог москва",
    "limit": 5,
    "filter_type": "all",
    "apify_token": token,
    "is_mock": False
})

print("HTTP Статус:", response.status_code)
if response.status_code == 200:
    data = response.json()
    print(f"Сессия создана: {data['title']}")
    print(f"Всего лидов найдено: {len(data['leads'])}")
    print(f"Из них БЕЗ сайта (целевые): {data['leads_without_site']}")
    print("\n--- Полученные реальные лиды ---")
    for l in data["leads"]:
        print(f"• @{l['username']} | {l['full_name']} | Статус: {l['link_label']} | Ссылка: {l['external_url'] or 'НЕТ'}")
else:
    print("Ошибка:", response.text)