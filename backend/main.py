import uuid
import datetime
from fastapi import FastAPI, Depends, HTTPException, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional

from database import engine, get_db, Base
import models
import schemas
from services.apify_service import fetch_apify_leads
from services.exporter import generate_excel_export

# Initialize Database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Lead Hunter & Tracker API", version="1.0.0")

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "ok", "app": "Lead Hunter & Tracker API"}

@app.post("/api/parse", response_model=schemas.SessionDetailResponse)
async def create_parsing_session(
    payload: schemas.ParseRequest,
    db: Session = Depends(get_db)
):
    query_clean = payload.query.strip()
    if not query_clean:
        raise HTTPException(status_code=400, detail="Поисковый запрос не может быть пустым")

    session_id = str(uuid.uuid4())
    session_title = f"{query_clean} ({datetime.datetime.now().strftime('%d.%m %H:%M')})"

    # Create new session entry
    new_session = models.ParsingSession(
        id=session_id,
        title=session_title,
        query=query_clean,
        limit=payload.limit,
        filter_type=payload.filter_type,
        status="running",
        created_at=datetime.datetime.utcnow()
    )
    db.add(new_session)
    db.commit()

    try:
        # Fetch leads from Apify / Analyzer
        raw_leads = await fetch_apify_leads(
            query=query_clean,
            limit=payload.limit,
            filter_type=payload.filter_type,
            apify_token=payload.apify_token
        )

        leads_to_create = []
        without_site_count = 0

        for item in raw_leads:
            if item["link_type"] == "no_site":
                without_site_count += 1

            lead_obj = models.Lead(
                session_id=session_id,
                username=item["username"],
                full_name=item["full_name"],
                profile_url=item["profile_url"],
                avatar_url=item.get("avatar_url", ""),
                followers_count=item.get("followers_count", 0),
                biography=item.get("biography", ""),
                external_url=item.get("external_url", ""),
                link_type=item.get("link_type", "no_site"),
                link_label=item.get("link_label", "Нет сайта"),
                has_website=item.get("has_website", False),
                has_whatsapp=item.get("has_whatsapp", False),
                has_other_links=item.get("has_other_links", False),
                contacted=False,
                reply_status="Не отправлено",
                notes=""
            )
            leads_to_create.append(lead_obj)

        db.bulk_save_objects(leads_to_create)
        
        new_session.status = "completed"
        new_session.total_leads = len(leads_to_create)
        new_session.leads_without_site = without_site_count
        db.commit()
        db.refresh(new_session)

    except Exception as e:
        new_session.status = "failed"
        db.commit()
        raise HTTPException(status_code=500, detail=f"Ошибка парсинга: {str(e)}")

    # Fetch with leads
    session_with_leads = db.query(models.ParsingSession).filter(models.ParsingSession.id == session_id).first()
    return session_with_leads

@app.get("/api/sessions", response_model=List[schemas.SessionResponse])
def get_all_sessions(db: Session = Depends(get_db)):
    sessions = db.query(models.ParsingSession).order_by(models.ParsingSession.created_at.desc()).all()
    results = []
    for s in sessions:
        contacted_count = db.query(models.Lead).filter(models.Lead.session_id == s.id, models.Lead.contacted == True).count()
        s_dict = schemas.SessionResponse.from_orm(s)
        s_dict.contacted_count = contacted_count
        results.append(s_dict)
    return results

@app.get("/api/sessions/{session_id}", response_model=schemas.SessionDetailResponse)
def get_session_detail(session_id: str, db: Session = Depends(get_db)):
    session_obj = db.query(models.ParsingSession).filter(models.ParsingSession.id == session_id).first()
    if not session_obj:
        raise HTTPException(status_code=404, detail="Сессия парсинга не найдена")
    return session_obj

@app.delete("/api/sessions/{session_id}")
def delete_session(session_id: str, db: Session = Depends(get_db)):
    session_obj = db.query(models.ParsingSession).filter(models.ParsingSession.id == session_id).first()
    if not session_obj:
        raise HTTPException(status_code=404, detail="Сессия не найдена")
    db.delete(session_obj)
    db.commit()
    return {"status": "deleted", "id": session_id}

@app.patch("/api/leads/{lead_id}", response_model=schemas.LeadResponse)
def update_lead(lead_id: int, payload: schemas.LeadUpdate, db: Session = Depends(get_db)):
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Лид не найден")

    if payload.contacted is not None:
        lead.contacted = payload.contacted
        if payload.contacted and lead.reply_status == "Не отправлено":
            lead.reply_status = "Ожидает ответа"
        elif not payload.contacted and lead.reply_status == "Ожидает ответа":
            lead.reply_status = "Не отправлено"

    if payload.reply_status is not None:
        lead.reply_status = payload.reply_status
        if payload.reply_status not in ["Не отправлено", "Отказ"] and not lead.contacted:
            lead.contacted = True

    if payload.notes is not None:
        lead.notes = payload.notes

    db.commit()
    db.refresh(lead)
    return lead

@app.delete("/api/leads/{lead_id}")
def delete_lead(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Лид не найден")
    
    session_id = lead.session_id
    db.delete(lead)
    db.commit()

    # Recalculate counts
    session_obj = db.query(models.ParsingSession).filter(models.ParsingSession.id == session_id).first()
    if session_obj:
        session_obj.total_leads = db.query(models.Lead).filter(models.Lead.session_id == session_id).count()
        session_obj.leads_without_site = db.query(models.Lead).filter(models.Lead.session_id == session_id, models.Lead.link_type == "no_site").count()
        db.commit()

    return {"status": "deleted", "lead_id": lead_id}

@app.get("/api/sessions/{session_id}/export")
def export_session_excel(session_id: str, db: Session = Depends(get_db)):
    session_obj = db.query(models.ParsingSession).filter(models.ParsingSession.id == session_id).first()
    if not session_obj:
        raise HTTPException(status_code=404, detail="Сессия не найдена")

    leads = db.query(models.Lead).filter(models.Lead.session_id == session_id).order_by(models.Lead.id.asc()).all()
    excel_stream = generate_excel_export(session_obj.title, leads)

    filename = f"leads_{session_id[:8]}_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"

    return StreamingResponse(
        excel_stream,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )

@app.post("/api/generate-offer", response_model=schemas.OfferResponse)
def generate_ai_offer(req: schemas.OfferRequest):
    """
    UI Mock / Template generator for AI-generated outreach offers
    """
    name = req.full_name or f"@{req.username}"
    niche = req.niche or "бизнеса"
    
    if req.tone == "business":
        subject = f"Коммерческое предложение по сайту для {name}"
        text = f"""Здравствуйте, {name}!

Меня зовут [Ваше Имя], я веб-разработчик.
Обратил внимание на ваш профиль в Instagram — у вас отличный контент и сильное позиционирование в сфере {niche}.

Заметил, что у вас пока нет отдельного сайта для приема заявок и презентации услуг. 
Наличие конверсионного сайта позволило бы:
1. Забирать горячих клиентов из поисковиков (Яндекс / Google).
2. Автоматизировать запись и прием оплат 24/7 без ручной переписки.
3. Повысить средний чек за счет премиального визуала.

Я разработал концепт современного сайта именно под вашу нишу. Могу отправить короткое видео-превью или ссылку на концепт. 

Вам было бы интересно взглянуть?"""
    elif req.tone == "bold":
        subject = f"Теряете до 40% заявок без сайта | Предложение для {name}"
        text = f"""Приветствую! 

У вас классный профиль @{req.username}, но прямо сейчас вы отдаете часть клиентов конкурентам, просто потому что у вас нет быстрого сайта-лендинга.

Людям неудобно ждать ответа в Директе — им нужен понятный прайс, отзывы и запись в 2 клика.

Я могу упаковать ваш бренд в стильный продающий сайт за 4–6 дней под ключ.
Уже сделал набросок структуры под ваше направление. 

Прислать набросок сюда?"""
    else: # Friendly default
        subject = f"Идея для развития @{req.username} ✨"
        text = f"""Здравствуйте, {name}! 👋

Очень понравился ваш профиль и подход к делу! 

Обратил внимание, что в шапке профиля нет ссылки на сайт. Сейчас как раз собираю портфолио для сильных проектов в вашей нише и подготовил индивидуальный макет удобного сайта для записи и демонстрации ваших работ.

Сайт отлично открывается с телефонов, сразу ведет клиентов в WhatsApp/Telegram и поднимает доверие.

С удовольствием покажу бесплатный прототип. Отправить вам ссылку посмотреть?"""

    return schemas.OfferResponse(subject=subject, offer_text=text)