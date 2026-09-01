import re
from typing import Dict, Any, List, Union
from urllib.parse import urlparse

MAPS_AND_DIRECTORY_DOMAINS = [
    "2gis.ru", "2gis.com", "go.2gis.com", "2gis.kz", "2gis.by", "2gis.ua",
    "yandex.ru/maps", "yandex.com/maps", "maps.yandex.ru", "yandex.ru/profile", "yandex.ru/sprav", "y.at/",
    "maps.google.com", "google.com/maps", "goo.gl/maps", "maps.app.goo.gl",
    "zoon.ru", "zoon.kz", "flamp.ru", "prodoctorov.ru", "doctu.ru", "docdoc.ru", "sberhealth.ru",
    "tripadvisor.ru", "tripadvisor.com", "restoclub.ru", "otzovik.com", "irecommend.ru",
    "avito.ru", "youla.ru", "kudago.com", "afisha.ru", "pulscen.ru", "tiu.ru", "blizko.ru",
    "yell.ru", "orgpage.ru", "spravker.ru", "allinform.ru"
]

BOOKING_WIDGET_DOMAINS = [
    "yclients.com", "dikidi.net", "dikidi.ru", "sonline.su", "mst.link",
    "gnom.guru", "rubitime.ru", "beautyagent.ru", "nethouse.id", "alfa-crm.ru",
    "arnica.pro", "appevent.ru", "bnovo.ru", "travelline.ru", "bronirui.online",
    "mastersapp.ru", "wlaunch.ru", "fitbase.io", "impulsecrm.ru"
]

MULTILINK_DOMAINS = [
    "taplink.cc", "taplink.ws", "linktr.ee", "beacons.ai", "hipolink.net",
    "mssg.me", "heylink.me", "msha.ke", "bio.link", "campsite.bio",
    "snipfeed.co", "sends.link", "clck.ru", "vk.link", "mssg.biz", "me-qr.com",
    "tap.link", "swip.link", "mylink.is", "mssg.im"
]

WHATSAPP_DOMAINS = [
    "wa.me", "api.whatsapp.com", "chat.whatsapp.com", "whatsapp.com"
]

TELEGRAM_DOMAINS = [
    "t.me", "telegram.me", "telegram.org"
]

SOCIAL_DOMAINS = [
    "vk.com", "vk.me", "youtube.com", "youtu.be", "tiktok.com", "facebook.com", "fb.me",
    "pinterest.com", "threads.net", "ok.ru", "instagram.com"
]

CLOUD_DOMAINS = [
    "drive.google.com", "disk.yandex.ru", "disk.yandex.com", "cloud.mail.ru", "dropbox.com"
]

def extract_domain(url: str) -> str:
    try:
        clean_url = url.strip()
        if not clean_url.startswith("http://") and not clean_url.startswith("https://"):
            clean_url = "https://" + clean_url
        parsed = urlparse(clean_url)
        domain = parsed.netloc.lower()
        if domain.startswith("www."):
            domain = domain[4:]
        return domain
    except Exception:
        return ""

def classify_single_url(raw_url: str) -> Dict[str, Any]:
    url = (raw_url or "").strip().lower()
    if not url:
        return {"category": "empty", "domain": "", "url": ""}
        
    domain = extract_domain(url)
    
    # Check categories
    if any(wa in url for wa in WHATSAPP_DOMAINS):
        return {"category": "whatsapp", "domain": domain, "url": raw_url}
    if any(tg in url for tg in TELEGRAM_DOMAINS):
        return {"category": "telegram", "domain": domain, "url": raw_url}
    if any(ml in url for ml in MULTILINK_DOMAINS):
        return {"category": "multilink", "domain": domain, "url": raw_url}
    if any(bw in url for bw in BOOKING_WIDGET_DOMAINS):
        return {"category": "booking", "domain": domain, "url": raw_url}
    if any(map_d in url for map_d in MAPS_AND_DIRECTORY_DOMAINS):
        return {"category": "directory", "domain": domain, "url": raw_url}
    if any(soc in url for soc in SOCIAL_DOMAINS):
        return {"category": "social", "domain": domain, "url": raw_url}
    if any(cld in url for cld in CLOUD_DOMAINS):
        return {"category": "cloud", "domain": domain, "url": raw_url}
        
    # If it is a valid domain or web url not belonging to any of the above, it's a REAL WEBSITE
    if "." in domain or url.startswith("http"):
        return {"category": "has_site", "domain": domain, "url": raw_url}
        
    return {"category": "other", "domain": domain, "url": raw_url}

def analyze_profile_links(raw_input: Union[str, List[Any]] = "", biography: str = "") -> Dict[str, Any]:
    """
    Analyzes ALL links found in an Instagram profile:
    - Primary externalUrl
    - Additional links from the expandable drawer / sheet (bio_links, externalUrls)
    - Links embedded inside the biography text
    
    Ensures that if ANY link in the drawer is a real website, the profile is marked as 'has_site'.
    """
    found_urls = []
    
    # 1. Collect from raw_input (could be string, list of strings, or list of dicts from Apify)
    if isinstance(raw_input, str) and raw_input.strip():
        # Might contain multiple links separated by comma, newline or space
        for item in re.split(r'[\s,\n]+', raw_input.strip()):
            if item.strip() and len(item.strip()) > 3:
                found_urls.append(item.strip())
    elif isinstance(raw_input, list):
        for item in raw_input:
            if isinstance(item, str) and item.strip():
                found_urls.append(item.strip())
            elif isinstance(item, dict):
                url_val = item.get("url") or item.get("link") or item.get("externalUrl") or ""
                if url_val and isinstance(url_val, str) and url_val.strip():
                    found_urls.append(url_val.strip())

    # 2. Extract links mentioned in bio text
    bio = (biography or "").strip()
    if bio:
        bio_matches = re.findall(r'(https?://[^\s,;]+|www\.[^\s,;]+|[a-zA-Z0-9-]+\.(?:ru|com|kz|by|uz|net|org|io|me|cc|pro|app|site|dev|store|su|link)[/\w.-]*)', bio)
        for m in bio_matches:
            found_urls.append(m.strip())

    # 3. Deduplicate URLs keeping order
    unique_urls = []
    seen = set()
    for u in found_urls:
        normalized = u.lower().rstrip("/")
        if normalized and normalized not in seen:
            seen.add(normalized)
            unique_urls.append(u)

    # If no links found at all
    if not unique_urls:
        bio_lower = bio.lower()
        if "wa.me" in bio_lower or "whatsapp" in bio_lower or "ватсап" in bio_lower:
            return {
                "link_type": "whatsapp",
                "link_label": "Только WhatsApp (в био)",
                "has_website": False,
                "has_whatsapp": True,
                "has_other_links": False,
                "detected_url": "",
                "all_urls": []
            }
        return {
            "link_type": "no_site",
            "link_label": "Нет ссылок / сайта",
            "has_website": False,
            "has_whatsapp": False,
            "has_other_links": False,
            "detected_url": "",
            "all_urls": []
        }

    # 4. Classify each unique URL
    classified = [classify_single_url(u) for u in unique_urls]
    
    site_links = [c for c in classified if c["category"] == "has_site"]
    whatsapp_links = [c for c in classified if c["category"] == "whatsapp"]
    multilink_links = [c for c in classified if c["category"] == "multilink"]
    telegram_links = [c for c in classified if c["category"] == "telegram"]
    booking_links = [c for c in classified if c["category"] == "booking"]
    directory_links = [c for c in classified if c["category"] == "directory"]
    social_links = [c for c in classified if c["category"] == "social"]
    cloud_links = [c for c in classified if c["category"] == "cloud"]

    has_whatsapp = len(whatsapp_links) > 0 or "whatsapp" in bio.lower() or "ватсап" in bio.lower() or "wa.me" in bio.lower()
    total_count = len(classified)

    # 🚨 CRITICAL RULE: If ANY link in the entire drawer is a real website -> 'has_site'
    if len(site_links) > 0:
        primary_site = site_links[0]
        domain = primary_site["domain"] or "сайт"
        
        if total_count > 1:
            label = f"Есть сайт в шторке ({domain})"
        else:
            label = f"Есть сайт ({domain})"

        return {
            "link_type": "has_site",
            "link_label": label,
            "has_website": True,
            "has_whatsapp": has_whatsapp,
            "has_other_links": total_count > 1,
            "detected_url": primary_site["url"],
            "all_urls": unique_urls
        }

    # NO real website found in any of the links (Target Lead for Web Development!)
    # Determine the most representative label and type:
    
    if len(multilink_links) > 0:
        primary_url = multilink_links[0]["url"]
        extra = f" (+{total_count-1} в шторке)" if total_count > 1 else ""
        return {
            "link_type": "multilink",
            "link_label": f"Мультиссылка (Taplink){extra}",
            "has_website": False,
            "has_whatsapp": has_whatsapp,
            "has_other_links": total_count > 1,
            "detected_url": primary_url,
            "all_urls": unique_urls
        }
        
    if len(whatsapp_links) > 0:
        primary_url = whatsapp_links[0]["url"]
        if len(telegram_links) > 0 or len(directory_links) > 0:
            extra_names = []
            if telegram_links: extra_names.append("TG")
            if directory_links: extra_names.append("2ГИС")
            if booking_links: extra_names.append("Виджет")
            label = f"WhatsApp + {', '.join(extra_names)} (в шторке, без сайта)"
        elif total_count > 1:
            label = f"Только WhatsApp ({total_count} ссылки в шторке, без сайта)"
        else:
            label = "Только WhatsApp"
            
        return {
            "link_type": "whatsapp",
            "link_label": label,
            "has_website": False,
            "has_whatsapp": True,
            "has_other_links": total_count > 1,
            "detected_url": primary_url,
            "all_urls": unique_urls
        }
        
    if len(booking_links) > 0:
        primary_url = booking_links[0]["url"]
        label = "Виджет записи (YClients/Дикиди, без сайта)"
        return {
            "link_type": "no_site",
            "link_label": label,
            "has_website": False,
            "has_whatsapp": has_whatsapp,
            "has_other_links": total_count > 1,
            "detected_url": primary_url,
            "all_urls": unique_urls
        }

    if len(directory_links) > 0:
        primary_url = directory_links[0]["url"]
        domain = directory_links[0]["domain"]
        label = "2ГИС / Карты (без сайта)" if "2gis" in domain else "Карты / Каталог (без сайта)"
        return {
            "link_type": "no_site",
            "link_label": label,
            "has_website": False,
            "has_whatsapp": has_whatsapp,
            "has_other_links": total_count > 1,
            "detected_url": primary_url,
            "all_urls": unique_urls
        }

    if len(telegram_links) > 0:
        primary_url = telegram_links[0]["url"]
        return {
            "link_type": "telegram",
            "link_label": "Только Telegram (без сайта)",
            "has_website": False,
            "has_whatsapp": has_whatsapp,
            "has_other_links": total_count > 1,
            "detected_url": primary_url,
            "all_urls": unique_urls
        }

    if len(social_links) > 0 or len(cloud_links) > 0:
        first_item = social_links[0] if social_links else cloud_links[0]
        return {
            "link_type": "social",
            "link_label": "Только соцсеть / Диск (без сайта)",
            "has_website": False,
            "has_whatsapp": has_whatsapp,
            "has_other_links": total_count > 1,
            "detected_url": first_item["url"],
            "all_urls": unique_urls
        }

    # Fallback if unknown domain
    return {
        "link_type": "no_site",
        "link_label": "Без сайта",
        "has_website": False,
        "has_whatsapp": has_whatsapp,
        "has_other_links": total_count > 1,
        "detected_url": unique_urls[0] if unique_urls else "",
        "all_urls": unique_urls
    }