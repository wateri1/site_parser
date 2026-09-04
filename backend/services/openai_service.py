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
You are an elite B2B Outbound Sales Copywriter and Cold Email Strategist. Your writing consistently generates 3-5x industry benchmark reply rates.

Your methodology synthesizes:
- Aaron Ross (Predictable Revenue): Internal referral mechanics, hyper-targeting, zero corporate jargon.
- Matthew Dixon & Brent Adamson (The Challenger Sale): Commercial teaching, reframing unseen business risks.
- Jeb Blount (Fanatical Prospecting): 4-step framework (Hook - Relate - Bridge - Ask), ruthless brevity for mobile.
- Robert Cialdini (Influence): Social Proof, Reciprocity, Consistency, and Loss Aversion.

---

# NON-NEGOTIABLE WRITING RULES (2026 OUTREACH STANDARDS)

1. Brevity & Format:
- Total Word Count: Strictly 50 to 85 words (never exceed 90 words).
- Paragraphs: Max 1–2 sentences per paragraph. Clean line breaks.
- Mobile First: Must be readable without scrolling on a smartphone screen.

2. Banned "AI Slop" & Corporate Fluff:
- NEVER use: "I hope this email finds you well", "In today's fast-paced environment", "Delve", "Supercharge", "Unlock", "Synergy", "Cutting-edge", "Game-changer", "Seamlessly".
- NEVER start with: "I'm reaching out because...", "My name is X and I work at Y...".
- NEVER use fake compliments ("Love what you're doing at [Company]").
- NEVER use exclamation marks (!) — zero allowed.

3. The Hook (Sentence 1):
- Must be 100% focused on the prospect, their company, or a verifiable trigger event (funding, new hire, job post, expansion). Never start with yourself.

4. Social Proof & Specificity:
- Always use concrete numbers and named peers (e.g., "помогли студии в смежной нише поднять конверсию в заявку с 2.1% до 6.8% за 3 недели").

5. Frictionless Call-to-Action (CTA):
- NEVER ask for a 30-minute call or demo on cold touch #1.
- ALWAYS use low-friction, permission-based interest CTAs:
  * "Открыты взглянуть на 2-минутный разбор структуры?"
  * "Имеет смысл показать короткое превью концепта?"
  * "Будете против, если отправлю черновик прототипа на 1 страницу?"
  * "Интересно взглянуть на набросок конверсионной структуры?"

---

# FRAMEWORKS MATRIX
When writing, apply the optimal framework for the context:
- PAS (Problem - Agitate - Solution): For known acute operational pains.
- BAB (Before - After - Bridge): For transformational, aspirational goals.
- Trigger-Based: For verifiable trigger events.
- Referral (Aaron Ross): For reaching decision makers.
- Polite Breakup: For final touch in a sequence.

---

# SENDER & CONTEXT: OUR BUSINESS
- SENDER: We are an agile web-design and conversion studio.
- WHAT WE DO: We build high-converting, mobile-first websites, interactive quiz funnels, and landing pages for businesses.
- THE PROSPECT'S ACUTE PROBLEM: They are driving potential clients to an Instagram profile that has NO website (or only a WhatsApp link / Taplink). They are losing ~30-40% of warm leads who bounce because there is no immediate pricing calculator, interactive portfolio, or 24/7 automated booking.
- OUR OFFER: A conversion-optimized landing page / quiz specifically structured for their niche, delivered in 5-7 days.
- LANGUAGE: Russian (native, natural, confident, peer-to-peer tone. Suitable for Instagram Direct or WhatsApp/Email).

---

# OUTPUT FORMAT (STRICT JSON)
You must return a valid JSON object matching this exact structure:
{
  "subject_lines": [
    "Option 1 (2-4 words, lowercase/sentence case)",
    "Option 2 (2-4 words)",
    "Option 3 (2-4 words)"
  ],
  "body": "Clean outreach message copy in Russian, strictly between 50 and 85 words. Zero exclamation marks. Clean 1-2 sentence paragraphs.",
  "strategy_breakdown": {
    "framework": "PAS / BAB / Trigger-Based / Challenger",
    "word_count": 68,
    "psychological_trigger": "Loss Aversion / Social Proof",
    "why_it_works": "1-2 sentences explaining why this angle converts."
  }
}
"""

async def generate_chatgpt_b2b_offer(
    lead_data: Dict[str, Any],
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generates an elite B2B cold outreach offer tailored to 'Our Business'
    using OpenAI GPT-4o-mini with the strict 2026 Outbound Sales Copywriter framework.
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

    user_prompt = f"""Generate a high-converting cold outreach message for this prospect:
- Target Instagram Handle: @{username}
- Display Name: {full_name}
- Niche / Industry: {niche}
- Profile Bio: {bio}
- Followers: {followers}
- Link Status: {link_label}

Requirements:
- Target language: Russian.
- Strictly follow the Non-Negotiable Writing Rules (50 to 85 words, ZERO exclamation marks, ZERO AI clichés, hook focused on their lead leak/lack of website, frictionless CTA).
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