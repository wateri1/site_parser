import os
import json
import httpx
from pathlib import Path
from typing import Dict, Any, Optional

def _load_env_key():
    key = os.getenv("OPENAI_API_KEY", "")
    if key:
        return key.strip()
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("OPENAI_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return ""

SYSTEM_PROMPT = """# ROLE & IDENTITY
You are an elite B2B Outbound Copywriter specializing in warm, respectful, high-converting outreach for Instagram Direct and WhatsApp.
Your writing combines authentic human empathy with soft consultative selling: zero aggression, zero accusatory language, clear tangible value, and ultra-scannable mobile formatting.

---

# NON-NEGOTIABLE WRITING RULES (WHATSAPP & DIRECT RAPID-SCAN)

1. Warm Empathy & Craft Observation (Paragraph 1):
- Greet warmly by name, noticing their specific craft, results, or approach to clients.
- Tone: warm, respectful peer-to-peer.
- Length: strictly 1 short sentence.
- Example: "Здравствуйте, Даурен. Обратил внимание на ваши тренировки — здорово, как детально вы показываете работу с техникой и результат подопечных."

2. Zero Aggression & Zero Defensiveness (Paragraph 2):
- STRICTLY BANNED: Never accuse the prospect or point fingers (NEVER write "Вы теряете", "Вы упускаете", "Вы делаете ошибку"). People hate strangers telling them they are losing business.
- INSTEAD: Describe natural buyer friction from the client's perspective:
  * "Заметил, что запись сейчас идет через Директ: по опыту, до 5–10 человек в месяц отсеиваются просто потому, что людям неудобно ждать ответа в переписке или хочется сразу увидеть прайс."
  * "Многие клиенты хотят сразу глянуть цены и свободные окошки, а когда нужно писать и ждать — часто откладывают или закрывают профиль."
- Length: strictly 1 short sentence.

3. Specific Tangible Deliverable (Paragraph 3):
- STRICTLY BANNED: Vague expressions like "набросок удобной страницы" or "какой-то концепт".
- INSTEAD: Name the exact 2-3 components built for their niche:
  * For fitness/coaching: "Я набросал черновик мини-сайта для вас: там сразу видны тарифы на тренировки, отзывы до/после и кнопка быстрой записи в 2 клика."
  * For beauty/salons: "Я набросал черновик мини-сайта под ваши услуги: там сразу вынесен прайс, фото работ и онлайн-запись без долгой переписки."
  * For legal/consulting: "Я набросал черновик страницы: там сразу понятны форматы консультаций, отзывы по делам и кнопка быстрой связи."
  * For home/furniture: "Я собрал черновик каталога: там наглядно видны готовые проекты, ориентир цен и кнопка расчета в WhatsApp."
- Length: strictly 1 short sentence.

4. Frictionless, Permission-Based Call-to-Action (Paragraph 4):
- Low pressure, respectful permission check.
- Length: strictly 1 short sentence.
- Examples:
  * "Удобно, если отправлю короткое 1-минутное видео с разбором сюда?"
  * "Интересно взглянуть на готовый набросок?"
  * "Будете против, если пришлю ссылку на черновик посмотреть?"

5. Ultra-Scannable WhatsApp Layout:
- Strictly 4 short paragraphs separated by clean blank lines.
- Each paragraph is strictly 1 single sentence.
- Total word count: Strictly 50 to 75 words (never exceed 80 words).
- ZERO exclamation marks (!) — calm, grounded confidence.
- NO abstract percentages or statistical jargon (no "30%", no "40%").

---

# OUTPUT FORMAT (STRICT JSON)
You must return a valid JSON object matching this exact structure:
{
  "subject_lines": [
    "Option 1 (2-4 words, lowercase/sentence case)",
    "Option 2 (2-4 words)",
    "Option 3 (2-4 words)"
  ],
  "body": "Clean outreach message copy in Russian, formatted into 4 short single-sentence paragraphs separated by double line breaks. Zero exclamation marks. No accusatory phrases ('вы теряете'). Specific deliverable (pricing, reviews, 2-click booking).",
  "strategy_breakdown": {
    "framework": "Empathy-Observation / Client-Friction / Tangible-Solution / Soft-CTA",
    "word_count": 62,
    "psychological_trigger": "Respect + Reduced Buyer Friction",
    "why_it_works": "1-2 предложения на русском языке с объяснением, почему этот подход дает высокую конверсию."
  }
}
"""

async def generate_chatgpt_b2b_offer(
    lead_data: Dict[str, Any],
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generates an elite B2B cold outreach offer tailored to 'Our Business'
    using OpenAI GPT-4o-mini with human empathy, non-aggressive friction framing, concrete deliverable, and WhatsApp scannable layout.
    """
    key = api_key or _load_env_key()
    if not key or not key.strip():
        raise Exception("Не указан OpenAI API Key. Добавьте его в настройках или в файле .env.")

    username = lead_data.get("username", "").strip()
    full_name = lead_data.get("full_name", "").strip() or f"@{username}"
    niche = lead_data.get("niche", "").strip() or "вашей сфере"
    bio = lead_data.get("biography", "").strip()
    link_label = lead_data.get("link_label", "").strip() or "Нет сайта"
    followers = lead_data.get("followers_count", 0)

    user_prompt = f"""Generate a high-converting, non-aggressive cold outreach message for this prospect:
- Target Instagram Handle: @{username}
- Display Name: {full_name}
- Niche / Industry: {niche}
- Profile Bio: {bio}
- Followers: {followers}
- Link Status: {link_label}

Crucial Requirements:
- Target language: Russian. All text including strategy breakdown must be in Russian.
- Paragraph 1: Warm human greeting + genuine craft observation (strictly 1 sentence).
- Paragraph 2: Client friction from buyer perspective — STRICTLY BANNED: 'вы теряете', 'вы упускаете', 'вы делаете ошибку' (strictly 1 sentence).
- Paragraph 3: Specific deliverable naming exact elements: mini-site with clear pricing, reviews/cases, and 2-click booking (strictly 1 sentence).
- Paragraph 4: Soft permission-based CTA (strictly 1 sentence).
- Formatting: Strictly 4 separate paragraphs separated by double linebreaks (\\n\\n).
- Word count: strictly 50 to 75 words.
- ZERO exclamation marks (!).
- Return valid JSON only.
"""

    headers = {
        "Authorization": f"Bearer {key.strip()}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4o-mini",
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.6,
        "max_tokens": 600
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload
            )

            if response.status_code == 401:
                raise Exception("Неверный OpenAI API ключ (401 Unauthorized).")
            elif response.status_code == 429:
                raise Exception("Превышен лимит запросов OpenAI или закончился баланс (429 Too Many Requests).")
            elif response.status_code != 200:
                raise Exception(f"Ошибка OpenAI API ({response.status_code}): {response.text[:200]}")

            data = response.json()
            raw_content = data["choices"][0]["message"]["content"]
            parsed = json.loads(raw_content)

            body_text = parsed.get("body", "").strip()
            # Enforce zero exclamation marks strictly
            body_text = body_text.replace("!", ".")

            # Ensure proper double-newline paragraph separation for WhatsApp/Direct readability
            if "\n" not in body_text:
                import re
                parts = [p.strip() for p in re.split(r'(?<=[.?])\s+(?=[А-ЯA-Z])', body_text) if p.strip()]
                if len(parts) >= 3:
                    body_text = "\n\n".join(parts)

            breakdown_obj = parsed.get("strategy_breakdown", {})
            if isinstance(breakdown_obj, dict):
                breakdown_str = f"Фреймворк: {breakdown_obj.get('framework', 'Challenger / Empathy')} | Слов: {breakdown_obj.get('word_count', len(body_text.split()))} | Триггер: {breakdown_obj.get('psychological_trigger', 'Respect + Reduced Friction')}\nПочему работает: {breakdown_obj.get('why_it_works', '')}"
            else:
                breakdown_str = str(breakdown_obj)

            return {
                "subject": (parsed.get("subject_lines") or ["Идея по сайту"])[0],
                "subject_lines": parsed.get("subject_lines", []),
                "offer_text": body_text,
                "strategy_breakdown": breakdown_str,
                "is_chatgpt": True
            }

    except json.JSONDecodeError:
        raise Exception("Не удалось распарсить ответ от OpenAI в формате JSON.")
    except httpx.TimeoutException:
        raise Exception("Превышено время ожидания ответа от OpenAI (таймаут 30с).")
    except Exception as e:
        raise Exception(f"{str(e)}")