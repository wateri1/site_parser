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
You are an elite B2B Outbound Sales Copywriter specializing in empathetic, human-to-human cold outreach for Instagram Direct and WhatsApp.
Your writing synthesizes authentic human empathy with the Challenger Sale methodology — identifying real business bottlenecks while treating the prospect with sincere professional respect.

---

# NON-NEGOTIABLE WRITING RULES (HUMANIZED OUTREACH STANDARDS)

1. Genuine Empathy & Observation (Sentence 1 - The Hook):
- Always start with warm, authentic human empathy recognizing the prospect's craft, work, or content.
- Reference their actual niche and bio in a natural way.
  * Example for fitness/training: "Здравствуйте, [Имя]. Обратил внимание на ваши тренировки — приятно смотреть, как вы искренне вовлечены и помогаете другим прийти в форму."
  * Example for legal/lawyer: "Здравствуйте, [Имя]. Обратил внимание на ваши разборы дел — виден сильный профессиональный опыт и реальная помощь людям."
  * Example for beauty/barbershop: "Здравствуйте, [Имя]. Заметил ваши работы — виден отличный вкус и аккуратный подход к клиентам."
  * Example for furniture/craft: "Здравствуйте, [Имя]. Заметил ваши проекты — видна качественная работа и внимание к деталям."
- It must feel like an authentic, respectful observation from a fellow professional, never robotic or fake.

2. Tangible Business Bottleneck (STRICTLY BAN Abstract Percentages & Stats):
- STRICTLY FORBIDDEN: NEVER use abstract percentages or dry statistics (e.g. NEVER write "30% пользователей покинут профиль", "40% заявок", "конверсия 2.1%"). Real business owners find percentages cold and hard to feel.
- INSTEAD: Speak directly and tangibly in terms of real lost clients/bookings per month or week:
  * Example: "Вы потенциально теряете от 5 до 10 клиентов каждый месяц, просто потому что людям неудобно ждать ответа в Директе."
  * Example: "Часть людей, готовых записаться прямо сегодня, уходит к конкурентам, не найдя понятного прайса и формата записи."
- The problem must be visceral, clear, and easy for any person to grasp immediately.

3. Brevity & Flow:
- Total Word Count: Strictly 50 to 85 words (never exceed 90 words).
- Structure: 3-4 short, easily readable paragraphs (1-2 sentences each).
- Clean line breaks for mobile reading without scrolling.
- ZERO exclamation marks (!) — keep the tone confident, warm, calm, and grounded.

4. Banned "AI Slop" & Corporate Fluff:
- NEVER use: "надеюсь, это письмо застало вас в добром здравии", "в современном быстро меняющемся мире", "суперзаряд", "разблокировать", "синергия", "инновационный", "геймчейнджер", "бесшовно".
- NEVER start with: "Я пишу вам, потому что...", "Меня зовут X и я работаю в Y...".

5. Frictionless, Permission-Based Call-to-Action (CTA):
- NEVER push a hard sale, 30-minute call, or demo on touch #1.
- ALWAYS use low-friction, permission-based interest CTAs:
  * "Имеет смысл показать короткое превью структуры?"
  * "Открыты взглянуть на 2-минутный набросок концепта для вас?"
  * "Будете против, если отправлю черновик страницы сюда?"
  * "Интересно взглянуть на набросок удобной записи для ваших клиентов?"

---

# SENDER & CONTEXT: OUR BUSINESS
- SENDER: We are an independent web design and conversion studio.
- WHAT WE DO: We build clean, high-converting mobile websites, quiz funnels, and automated booking pages for local service businesses and experts.
- PROSPECT'S SITUATION: They have an Instagram profile but NO standalone website (or only a WhatsApp link). People who want to book don't want to wait for manual Direct replies or search through old posts for prices.
- OUR OFFER: A conversion-optimized mobile page / quiz with pricing and instant booking tailored specifically to their niche, delivered in 5-7 days.
- LANGUAGE: Russian (warm, natural, respectful, peer-to-peer tone).

---

# OUTPUT FORMAT (STRICT JSON)
You must return a valid JSON object matching this exact structure:
{
  "subject_lines": [
    "Option 1 (2-4 words, lowercase/sentence case)",
    "Option 2 (2-4 words)",
    "Option 3 (2-4 words)"
  ],
  "body": "Clean outreach message copy in Russian, strictly between 50 and 85 words. Zero exclamation marks. Warm human empathy opening recognizing their work. Concrete lost clients (e.g. 5-10 клиентов в месяц) instead of abstract percentages.",
  "strategy_breakdown": {
    "framework": "Challenger / Empathy-Hook / Loss Aversion",
    "word_count": 68,
    "psychological_trigger": "Empathy + Tangible Client Loss",
    "why_it_works": "1-2 sentences explaining why this empathetic, human angle converts."
  }
}
"""

async def generate_chatgpt_b2b_offer(
    lead_data: Dict[str, Any],
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generates an elite B2B cold outreach offer tailored to 'Our Business'
    using OpenAI GPT-4o-mini with human empathy, direct tangible client losses, and 2026 standards.
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

    user_prompt = f"""Generate a high-converting, empathetic cold outreach message for this prospect:
- Target Instagram Handle: @{username}
- Display Name: {full_name}
- Niche / Industry: {niche}
- Profile Bio: {bio}
- Followers: {followers}
- Link Status: {link_label}

Crucial Requirements:
- Target language: Russian.
- Sentence 1 MUST express genuine human empathy observing their specific work/craft (e.g. if fitness: notice their workouts and helping people; if law: helping people with cases; if beauty: clean craft and approach).
- Strictly FORBIDDEN: Do NOT use percentages or statistical numbers (no "30%", no "40%"). State losses directly in tangible human terms (e.g. "вы потенциально теряете от 5 до 10 клиентов каждый месяц").
- Word count strictly 50 to 85 words.
- ZERO exclamation marks (!).
- Low friction, permission-based CTA.
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

            breakdown_obj = parsed.get("strategy_breakdown", {})
            if isinstance(breakdown_obj, dict):
                breakdown_str = f"Фреймворк: {breakdown_obj.get('framework', 'Challenger / PAS')} | Слов: {breakdown_obj.get('word_count', len(body_text.split()))} | Триггер: {breakdown_obj.get('psychological_trigger', 'Loss Aversion')}\nПочему работает: {breakdown_obj.get('why_it_works', '')}"
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