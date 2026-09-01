import os
import re
import random
import httpx
from typing import List, Dict, Any
from .analyzer import analyze_profile_links

# Realistic Mock Data Generator for Instagram Leads (when testing / demo mode / no token)
MOCK_NICHES = {
    "барбершоп": {
        "names": ["OldBoy Barbershop", "Chop-Chop Premium", "Бритва & Стиль", "Borodach Club", "TopGun Studio", "Gentleman Cuts", "Black Beard", "Razor & Fade"],
        "bios": [
            "✂️ Мужские стрижки и моделирование бороды\n☕️ Кофе и PlayStation\n📍 Центр города\nЗапись в Директ",
            "Стильные мужские стрижки | Камуфляж седины\n🔥 Скидка 20% на первый визит\nРаботаем с 10:00 до 22:00",
            "Барбершоп премиум класса. Создаем стиль с 2018 года.\nЗапись через WhatsApp или Direct 💈",
            "Твой любимый барбершоп на Пресне! Чай, виски, мужские разговоры 🥃\nЗапись в шапке профиля!"
        ],
        "link_samples": [
            "",
            "",
            "https://wa.me/79991234567",
            "https://taplink.cc/barbershop_pro",
            "https://linktr.ee/razorcut",
            "https://vk.com/barber_club",
            "https://barbershop-premium.ru"
        ]
    },
    "косметолог": {
        "names": ["Dr. Смирнова Косметолог", "Beauty Lab Studio", "Эстетик Клиник", "Face & Body Spa", "Dr. Elena Чистка & Уход", "Glow Skin Lab"],
        "bios": [
            "👩‍⚕️ Врач-косметолог с опытом 8 лет\n✨ Контурная пластика, чистки, пилинги\n💉 Только сертифицированные препараты\nКонсультация в Direct",
            "Идеальная кожа без фильтров ✨\nАппаратная косметология & SMAS лифтинг\nПрием по предварительной записи!",
            "Твой личный эксперт по красоте 🌿\nПомогаю забыть о тональном креме за 3 процедуры.\nЗапись в WhatsApp",
            "Эстетическая косметология | Москва Сити 🏙\nГубы твоей мечты за 30 минут 💋"
        ],
        "link_samples": [
            "",
            "",
            "https://wa.me/79039876543",
            "https://taplink.cc/dr_beauty_skin",
            "https://instagram.com",
            "https://t.me/dr_cosmetolog_bot",
            "https://glow-cosmetics-clinic.ru"
        ]
    },
    "ремонт": {
        "names": ["Ремонт Эксперт", "СтройДизайн Групп", "Квадратный Метр", "Ремонт Под Ключ", "ProRemont Studio", "Идеальный Дом Ремонт"],
        "bios": [
            "🔨 Капитальный и дизайнерский ремонт квартир под ключ\n📐 Бесплатный замер и смета за 24 часа!\nДоговор и гарантия 3 года 📄",
            "Ремонт квартир и коттеджей в новостройках 🏙\nСобственные бригады, работаем без предоплаты!\nПишите в Директ или WA",
            "Дизайн интерьера + Ремонт под ключ 🔑\nЭкономим до 20% на материалах от партнеров\nПортфолио в актуальном!",
            "Комплексный ремонт любой сложности ⚡️\nПоэтапная оплата, видеонаблюдение на объекте 24/7"
        ],
        "link_samples": [
            "",
            "",
            "https://wa.me/79165554433",
            "https://taplink.cc/pro_remont_msk",
            "https://mssg.me/remont_expert",
            "https://stroy-remont-pro.ru"
        ]
    },
    "дизайн": {
        "names": ["Studio Interior Design", "Архитектор & Дизайнер Анна", "Modern Living Interiors", "ArtSpace Design Studio", "Cozy Home Decor"],
        "bios": [
            "🏡 Создаю интерьеры для жизни и бизнеса\n📐 От планировки до реализации и авторского надзора\nПишите в Direct для консультации",
            "Дизайн жилых и коммерческих пространств ✨\nБолее 70 реализованных проектов\nЗаказать проект можно в WhatsApp",
            "Современные стильные интерьеры | Минимализм & Джапанди\nКомплектация мебелью со скидками 🌿",
            "Авторский дизайн квартир и домов 🪄\n3D визуализации, чертежи, комплектация"
        ],
        "link_samples": [
            "",
            "",
            "https://wa.me/79261112233",
            "https://beacons.ai/interior_anna",
            "https://taplink.cc/artspace_design",
            "https://interior-studio-design.com"
        ]
    }
}

DEFAULT_NICHE = {
    "names": ["Pro Studio", "Elite Business", "Prime Agency", "Master & Co", "Urban Service", "Nova Group", "Craft Workshop"],
    "bios": [
        "🌟 Профессиональные услуги и индивидуальный подход\n📍 Работаем каждый день\n📞 Связь в Direct или по телефону",
        "Качество, проверенное временем 🏆\nСпециальные предложения для новых клиентов!\nПишите для консультации",
        "Твой надежный партнер в городе 🚀\nБыстро, надежно, с гарантией качества."
    ],
    "link_samples": [
        "",
        "",
        "https://wa.me/79998887766",
        "https://taplink.cc/prime_agency",
        "https://t.me/pro_studio_manager",
        "https://elite-business-site.ru"
    ]
}

def generate_mock_leads(query: str, limit: int = 20, filter_type: str = "all") -> List[Dict[str, Any]]:
    # Match query to niche
    query_lower = query.lower()
    selected_niche = DEFAULT_NICHE
    for key, data in MOCK_NICHES.items():
        if key in query_lower:
            selected_niche = data
            break
            
    leads = []
    translit_query = re.sub(r'[^a-zA-Z0-9]', '', query.lower()) or "lead"
    
    # Weight links to ensure a good ratio of "no site" (target audience!)
    # ~50% no site, ~25% whatsapp/multilink, ~25% has site
    for i in range(1, limit * 2 + 10):
        if len(leads) >= limit:
            break
            
        name_prefix = random.choice(selected_niche["names"])
        username = f"{translit_query}_{random.randint(10, 999)}_{random.choice(['studio', 'pro', 'club', 'team', 'group', 'msk', 'spb', 'official'])}"
        full_name = f"{name_prefix} {random.choice(['| Эксперт', '| Москва', '| СПБ', '• Официально', ''])}".strip()
        bio = random.choice(selected_niche["bios"])
        
        # Select link with realistic distribution
        raw_link = random.choice(selected_niche["link_samples"])
        
        analysis = analyze_profile_links(raw_link, bio)
        
        # Apply filter if requested
        if filter_type == "no_site" and analysis["link_type"] != "no_site":
            continue
        if filter_type == "whatsapp" and analysis["link_type"] != "whatsapp":
            continue
        if filter_type == "multilink" and analysis["link_type"] != "multilink":
            continue
            
        followers = random.randint(850, 48000)
        
        lead_data = {
            "username": username,
            "full_name": full_name,
            "profile_url": f"https://instagram.com/{username}",
            "avatar_url": f"https://api.dicebear.com/7.x/identicon/svg?seed={username}",
            "followers_count": followers,
            "biography": bio,
            "external_url": analysis["detected_url"] or raw_link,
            "link_type": analysis["link_type"],
            "link_label": analysis["link_label"],
            "has_website": analysis["has_website"],
            "has_whatsapp": analysis["has_whatsapp"],
            "has_other_links": analysis["has_other_links"],
            "contacted": False,
            "reply_status": "Не отправлено",
            "notes": ""
        }
        leads.append(lead_data)
        
    return leads[:limit]

async def fetch_apify_leads(
    query: str,
    limit: int = 20,
    filter_type: str = "all",
    apify_token: str = None
) -> List[Dict[str, Any]]:
    """
    Fetches leads from Apify Instagram Scraper Actor.
    Falls back to high-quality mock data if no token or if Apify request fails.
    """
    token = apify_token or os.getenv("APIFY_API_TOKEN", "")
    
    if not token or token.strip().lower() in ["demo", "mock", "test", ""]:
        # Demo / Mock mode
        return generate_mock_leads(query, limit, filter_type)
        
    # Real Apify API Call using Instagram Search Scraper actor (apify/instagram-search-scraper)
    try:
        actor_id = "apify~instagram-search-scraper"
        api_url = f"https://api.apify.com/v2/acts/{actor_id}/run-sync-get-dataset-items?token={token}&timeout=120"
        
        payload = {
            "search": query,
            "searchType": "user",
            "resultsLimit": limit
        }
        
        async with httpx.AsyncClient(timeout=130.0) as client:
            response = await client.post(api_url, json=payload)
            if response.status_code in [200, 201]:
                items = response.json()
                if not isinstance(items, list):
                    items = []
                
                leads = []
                for item in items:
                    username = item.get("username") or item.get("ownerUsername") or ""
                    if not username:
                        continue
                        
                    full_name = item.get("fullName") or item.get("name") or username
                    bio = item.get("biography") or item.get("bio") or ""
                    
                    # Extract external URL
                    external_url = item.get("externalUrl") or item.get("website") or ""
                    if not external_url and item.get("externalUrls") and len(item.get("externalUrls")) > 0:
                        first_ext = item.get("externalUrls")[0]
                        if isinstance(first_ext, dict):
                            external_url = first_ext.get("url", "")
                        elif isinstance(first_ext, str):
                            external_url = first_ext
                    
                    followers = item.get("followersCount") or item.get("followers") or 0
                    avatar = item.get("profilePicUrlHD") or item.get("profilePicUrl") or f"https://api.dicebear.com/7.x/identicon/svg?seed={username}"
                    
                    analysis = analyze_profile_links(external_url, bio)
                    
                    if filter_type == "no_site" and analysis["link_type"] != "no_site":
                        continue
                    if filter_type == "whatsapp" and analysis["link_type"] != "whatsapp":
                        continue
                    if filter_type == "multilink" and analysis["link_type"] != "multilink":
                        continue
                        
                    leads.append({
                        "username": username,
                        "full_name": full_name,
                        "profile_url": f"https://instagram.com/{username}",
                        "avatar_url": avatar,
                        "followers_count": followers,
                        "biography": bio,
                        "external_url": analysis["detected_url"] or external_url,
                        "link_type": analysis["link_type"],
                        "link_label": analysis["link_label"],
                        "has_website": analysis["has_website"],
                        "has_whatsapp": analysis["has_whatsapp"],
                        "has_other_links": analysis["has_other_links"],
                        "contacted": False,
                        "reply_status": "Не отправлено",
                        "notes": ""
                    })
                    
                if leads:
                    return leads[:limit]
                    
    except Exception as e:
        print(f"Apify call failed ({e}), falling back to simulated data.")
        
    # If API fails or returns 0 items, fallback to mock data for reliability
    return generate_mock_leads(query, limit, filter_type)