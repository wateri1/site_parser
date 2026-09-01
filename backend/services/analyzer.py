import re
from typing import Dict, Any

MAPS_AND_DIRECTORY_DOMAINS = [
    "2gis.ru", "2gis.com", "go.2gis.com", "2gis.kz", "2gis.by", "2gis.ua",
    "yandex.ru/maps", "yandex.com/maps", "maps.yandex.ru", "yandex.ru/profile", "yandex.ru/sprav", "y.at/",
    "maps.google.com", "google.com/maps", "goo.gl/maps", "maps.app.goo.gl",
    "zoon.ru", "zoon.kz", "flamp.ru", "prodoctorov.ru", "doctu.ru", "docdoc.ru", "sberhealth.ru",
    "tripadvisor.ru", "tripadvisor.com", "restoclub.ru", "otzovik.com", "irecommend.ru",
    "avito.ru", "youla.ru", "kudago.com", "afisha.ru", "pulscen.ru", "tiu.ru", "blizko.ru"
]

BOOKING_WIDGET_DOMAINS = [
    "yclients.com", "dikidi.net", "dikidi.ru", "sonline.su", "mst.link",
    "gnom.guru", "rubitime.ru", "beautyagent.ru", "nethouse.id", "alfa-crm.ru",
    "arnica.pro", "appevent.ru"
]

MULTILINK_DOMAINS = [
    "taplink.cc", "taplink.ws", "linktr.ee", "beacons.ai", "hipolink.net",
    "mssg.me", "heylink.me", "msha.ke", "bio.link", "campsite.bio",
    "snipfeed.co", "sends.link", "clck.ru", "vk.link"
]

WHATSAPP_DOMAINS = [
    "wa.me", "api.whatsapp.com", "chat.whatsapp.com", "whatsapp.com"
]

TELEGRAM_DOMAINS = [
    "t.me", "telegram.me"
]

SOCIAL_DOMAINS = [
    "vk.com", "vk.me", "youtube.com", "youtu.be", "tiktok.com", "facebook.com", "pinterest.com"
]

def analyze_profile_links(external_url: str = "", biography: str = "") -> Dict[str, Any]:
    url = (external_url or "").strip().lower()
    bio = (biography or "").strip().lower()
    
    # Check if URL exists in bio if external_url is empty
    if not url:
        url_match = re.search(r'(https?://[^\s]+|www\.[^\s]+|[a-zA-Z0-9-]+\.(?:ru|com|net|org|io|me|cc|by|kz|uz|co|store|pro|dev|ai|app|su)[/\w.-]*)', bio)
        if url_match:
            url = url_match.group(0)

    # 1. No link found
    if not url:
        # Check if whatsapp mentioned in bio
        if "wa.me" in bio or "whatsapp" in bio or "ватсап" in bio:
            return {
                "link_type": "whatsapp",
                "link_label": "Только WhatsApp (в био)",
                "has_website": False,
                "has_whatsapp": True,
                "has_other_links": False,
                "detected_url": ""
            }
        return {
            "link_type": "no_site",
            "link_label": "Нет сайта",
            "has_website": False,
            "has_whatsapp": False,
            "has_other_links": False,
            "detected_url": ""
        }

    # 2. Maps & Catalogs (2GIS, Yandex Maps, Google Maps, Zoon) -> Only directory listing, NO actual website! (Target lead)
    if any(map_d in url for map_d in MAPS_AND_DIRECTORY_DOMAINS):
        label = "2ГИС / Карты (Нет сайта)" if "2gis" in url else "Карты / Каталог (Нет сайта)"
        return {
            "link_type": "no_site",
            "link_label": label,
            "has_website": False,
            "has_whatsapp": False,
            "has_other_links": True,
            "detected_url": url
        }

    # 3. Booking Widget (YClients, Dikidi, Sonline) -> Perfect candidate for a full website! (Target lead)
    if any(bw in url for bw in BOOKING_WIDGET_DOMAINS):
        return {
            "link_type": "no_site",
            "link_label": "Только виджет записи (YClients/Дикиди)",
            "has_website": False,
            "has_whatsapp": False,
            "has_other_links": True,
            "detected_url": url
        }

    # 4. WhatsApp
    if any(wa in url for wa in WHATSAPP_DOMAINS):
        return {
            "link_type": "whatsapp",
            "link_label": "Только WhatsApp",
            "has_website": False,
            "has_whatsapp": True,
            "has_other_links": False,
            "detected_url": url
        }

    # 5. Telegram
    if any(tg in url for tg in TELEGRAM_DOMAINS):
        return {
            "link_type": "telegram",
            "link_label": "Только Telegram",
            "has_website": False,
            "has_whatsapp": False,
            "has_other_links": True,
            "detected_url": url
        }

    # 6. Multilink (Taplink, Linktree, etc.)
    if any(ml in url for ml in MULTILINK_DOMAINS):
        return {
            "link_type": "multilink",
            "link_label": "Мультиссылка (Taplink)",
            "has_website": False,
            "has_whatsapp": False,
            "has_other_links": True,
            "detected_url": url
        }

    # 7. Social networks
    if any(soc in url for soc in SOCIAL_DOMAINS):
        return {
            "link_type": "social",
            "link_label": "Соцсеть (VK/YouTube)",
            "has_website": False,
            "has_whatsapp": False,
            "has_other_links": True,
            "detected_url": url
        }

    # 8. Has real standalone website
    return {
        "link_type": "has_site",
        "link_label": "Есть сайт",
        "has_website": True,
        "has_whatsapp": False,
        "has_other_links": False,
        "detected_url": url
    }