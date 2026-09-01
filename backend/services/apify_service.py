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
    },
    "адвокат": {
        "names": ["Адвокат Аскаров", "Юридическая защита & Партнеры", "Адвокатский кабинет Садыкова", "Legal Group Almaty", "Адвокат по уголовным и гражданским делам", "Юрист Права"],
        "bios": [
            "⚖️ Профессиональная юридическая помощь в судах\n📍 Опыт работы более 12 лет. Консультации\n📞 Запись на консультацию в WhatsApp",
            "Адвокатская защита бизнеса и физлиц 🏛\nГражданские, семейные, уголовные споры\nПишите в Direct или по номеру ниже",
            "Юрист / Адвокат Алматы ⚖️\nПомощь при ДТП, банкротстве, сделках с недвижимостью\nСвязь через WhatsApp",
            "Правовая защита 24/7 🛡\nРешение сложных споров в досудебном и судебном порядке\nЗапись на аудит дела"
        ],
        "link_samples": [
            "",
            "",
            "https://wa.me/77015554433",
            ["https://wa.me/77015554433", "https://2gis.kz/almaty/firm/70000001018"],
            ["https://wa.me/77015554433", "https://t.me/advokat_almaty", "https://2gis.kz/almaty/firm/70000001018"],
            "https://taplink.cc/advokat_almaty",
            ["https://wa.me/77015554433", "https://advokat-almaty-pro.kz"],
            "https://advokat-almaty-pro.kz"
        ]
    },
    "юрист": {
        "names": ["Юрист Консалт", "Правовой Центр Защита", "Юрист Эксперт", "Юридическая компания Фемида", "Бизнес Юрист"],
        "bios": [
            "📋 Юридическое сопровождение бизнеса и граждан\n⚖️ Споры, взыскание долгов, банкротство\nЗапись на консультацию в WA",
            "Защищаем ваши права в суде 🏛\nСоставление договоров, исков, претензий\nБесплатный первичный разбор в Директ",
            "Юридическая помощь под ключ 🛡\nГарантия по договору. 95% выигранных дел\nСвязь в WhatsApp"
        ],
        "link_samples": [
            "",
            "",
            "https://wa.me/79051234567",
            ["https://wa.me/79051234567", "https://t.me/jurist_lawyer"],
            "https://taplink.cc/jurist_expert",
            ["https://wa.me/79051234567", "https://urist-pravo-group.ru"]
        ]
    },
    "мебель": {
        "names": ["Кухни & Мебель На Заказ", "WoodCraft Studio", "Мебельная Фабрика Комфорт", "Loft & Modern Мебель", "Кухни Премиум"],
        "bios": [
            "🪵 Производство корпусной мебели и кухонь по размерам\n📐 3D-проект и выезд дизайнера бесплатно!\nСвязь в WhatsApp для расчета цены",
            "Стильная мебель на заказ от производителя ✨\nЭкологичные материалы, гарантия 5 лет\nРассчитайте стоимость в шапке профиля",
            "Кухни вашей мечты под ключ 🍳\nСобственное производство, сроки от 14 дней\nПишите в Директ или WA"
        ],
        "link_samples": [
            "",
            "",
            "https://wa.me/79184443322",
            ["https://wa.me/79184443322", "https://taplink.cc/mebel_kuhni_pro"],
            ["https://wa.me/79184443322", "https://kuhni-mebel-custom.ru"]
        ]
    },
    "таро": {
        "names": ["Таролог Амина", "Таро & Астрология Алматы", "Tarot Guide Lab", "Магика Таро", "Таролог-Психолог Динара"],
        "bios": [
            "🔮 Расклады на Таро | Отношения, финансы, предназначение\n✨ Более 1000 довольных клиентов\nЗапись на консультацию в WhatsApp",
            "Таролог Алматы 🕯\nПомогаю найти ответы на волнующие вопросы\nПишите в Директ или WA для записи на расклад",
            "Глубокий анализ ситуаций на картах Таро 🃏\nКонфиденциально, онлайн по всему миру\nСсылка на запись ниже"
        ],
        "link_samples": [
            "",
            "",
            "https://wa.me/77071234567",
            ["https://wa.me/77071234567", "https://t.me/taro_almaty_consult"],
            "https://taplink.cc/taro_almaty",
            ["https://wa.me/77071234567", "https://taro-online-expert.kz"]
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
        ["https://wa.me/79998887766", "https://t.me/pro_studio_manager"],
        "https://taplink.cc/prime_agency",
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
    for i in range(1, limit * 2 + 20):
        if len(leads) >= limit:
            break
            
        name_prefix = random.choice(selected_niche["names"])
        username = f"{translit_query}_{random.randint(10, 999)}_{random.choice(['studio', 'pro', 'club', 'team', 'group', 'kz', 'msk', 'spb', 'official'])}"
        full_name = f"{name_prefix} {random.choice(['| Эксперт', '| Алматы', '| Москва', '| СПБ', '• Официально', ''])}".strip()
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
    search_type: str = "user",
    filter_type: str = "all",
    apify_token: str = None
) -> List[Dict[str, Any]]:
    """
    Fetches leads from Apify Instagram Search Scraper Actor (apify/instagram-search-scraper).
    Uses exact payload schema:
    {
        "search": query,
        "searchType": search_type,
        "searchLimit": limit,
        "resultsLimit": limit
    }
    Falls back to high-quality mock data if no token or if Apify request fails.
    """
    token = apify_token or os.getenv("APIFY_API_TOKEN", "")
    
    if not token or token.strip().lower() in ["demo", "mock", "test", ""]:
        # Demo / Mock mode when no token is provided
        return generate_mock_leads(query, limit, filter_type)
        
    # Real Apify API Call using Instagram Search Scraper actor (apify/instagram-search-scraper)
    actor_id = "apify~instagram-search-scraper"
    api_url = f"https://api.apify.com/v2/acts/{actor_id}/run-sync-get-dataset-items?token={token}&timeout=180"
    
    payload = {
        "search": query,
        "searchType": search_type or "user",
        "searchLimit": limit,
        "resultsLimit": limit
    }
    
    try:
        async with httpx.AsyncClient(timeout=190.0) as client:
            response = await client.post(api_url, json=payload)
            
            if response.status_code not in [200, 201]:
                error_body = response.text[:300]
                if response.status_code == 401:
                    raise Exception("Неверный токен Apify (401 Unauthorized). Проверьте токен в консоли Apify.")
                elif response.status_code == 402:
                    raise Exception("Закончился баланс на аккаунте Apify (402 Payment Required).")
                elif response.status_code == 404:
                    raise Exception(f"Актор {actor_id} не найден на Apify (404).")
                else:
                    raise Exception(f"Apify API вернул ошибку {response.status_code}: {error_body}")
            
            items = response.json()
            if not isinstance(items, list):
                items = []
                
            if len(items) == 0:
                # Return empty list or raise informative error
                return []
            
            leads = []
            for item in items:
                user_data = item.get("user") if isinstance(item.get("user"), dict) else {}
                
                # Extract username
                username = (
                    item.get("username") or 
                    item.get("ownerUsername") or 
                    user_data.get("username") or 
                    item.get("name") or 
                    ""
                ).strip()
                
                if not username:
                    continue
                    
                # Extract full name
                full_name = (
                    item.get("fullName") or 
                    item.get("full_name") or 
                    item.get("name") or 
                    user_data.get("full_name") or 
                    username
                ).strip()
                
                # Extract biography
                bio = (
                    item.get("biography") or 
                    item.get("bio") or 
                    item.get("caption") or 
                    user_data.get("biography") or 
                    ""
                ).strip()
                
                # Collect ALL links from the profile (including the expandable drawer / sheet)
                all_extracted_links = []
                
                # 1. Main externalUrl / website
                for k in ["externalUrl", "external_url", "website"]:
                    val = item.get(k) or user_data.get(k)
                    if val and isinstance(val, str):
                        all_extracted_links.append(val)
                        
                # 2. bio_links / bioLinks list (the modern Instagram links sheet / шторка)
                for k in ["bio_links", "bioLinks"]:
                    bio_list = item.get(k) or user_data.get(k)
                    if isinstance(bio_list, list):
                        for b_item in bio_list:
                            if isinstance(b_item, dict):
                                u = b_item.get("url") or b_item.get("link") or ""
                                if u: all_extracted_links.append(u)
                            elif isinstance(b_item, str):
                                all_extracted_links.append(b_item)
                                
                # 3. externalUrls / external_urls list
                for k in ["externalUrls", "external_urls"]:
                    ext_list = item.get(k) or user_data.get(k)
                    if isinstance(ext_list, list):
                        for ext_item in ext_list:
                            if isinstance(ext_item, dict):
                                u = ext_item.get("url") or ext_item.get("link") or ""
                                if u: all_extracted_links.append(u)
                            elif isinstance(ext_item, str):
                                all_extracted_links.append(ext_item)

                # Followers count
                followers = (
                    item.get("followersCount") or 
                    item.get("followers") or 
                    user_data.get("follower_count") or 
                    user_data.get("followers_count") or 
                    0
                )
                
                # Avatar URL
                avatar = (
                    item.get("profilePicUrlHD") or 
                    item.get("profilePicUrl") or 
                    item.get("profile_pic_url_hd") or 
                    user_data.get("profile_pic_url") or 
                    f"https://api.dicebear.com/7.x/identicon/svg?seed={username}"
                )
                
                # Comprehensive link & drawer analysis
                analysis = analyze_profile_links(all_extracted_links, bio)
                
                # Filter matching
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
                    "external_url": analysis["detected_url"] or (all_extracted_links[0] if all_extracted_links else ""),
                    "link_type": analysis["link_type"],
                    "link_label": analysis["link_label"],
                    "has_website": analysis["has_website"],
                    "has_whatsapp": analysis["has_whatsapp"],
                    "has_other_links": analysis["has_other_links"],
                    "contacted": False,
                    "reply_status": "Не отправлено",
                    "notes": ""
                })
                
            return leads[:limit]
                
    except httpx.TimeoutException:
        raise Exception("Превышено время ожидания ответа от Apify (таймаут 180с). Попробуйте уменьшить лимит или повторить запрос.")
    except Exception as e:
        # If real token was passed, report the real exception so user knows what went wrong!
        raise Exception(f"Ошибка парсинга Apify: {str(e)}")