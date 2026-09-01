import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base

class ParsingSession(Base):
    __tablename__ = "parsing_sessions"

    id = Column(String, primary_key=True, index=True) # UUID string
    title = Column(String, nullable=False)
    query = Column(String, nullable=False)
    limit = Column(Integer, default=20)
    filter_type = Column(String, default="all") # "all", "no_site", "whatsapp", "multilink"
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String, default="completed") # "running", "completed", "failed"
    total_leads = Column(Integer, default=0)
    leads_without_site = Column(Integer, default=0)

    leads = relationship("Lead", back_populates="session", cascade="all, delete-orphan")

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id = Column(String, ForeignKey("parsing_sessions.id", ondelete="CASCADE"), index=True)
    
    username = Column(String, nullable=False, index=True)
    full_name = Column(String, default="")
    profile_url = Column(String, nullable=False)
    avatar_url = Column(String, default="")
    followers_count = Column(Integer, default=0)
    biography = Column(Text, default="")
    
    # Link Analysis
    external_url = Column(String, default="")
    link_type = Column(String, default="no_site") # "no_site", "has_site", "whatsapp", "telegram", "multilink", "social"
    link_label = Column(String, default="Нет сайта")
    has_website = Column(Boolean, default=False)
    has_whatsapp = Column(Boolean, default=False)
    has_other_links = Column(Boolean, default=False)
    
    # CRM Lead Tracker fields
    contacted = Column(Boolean, default=False) # Чекбокс: Писал (Да/Нет)
    reply_status = Column(String, default="Не отправлено") # Статус ответа: "Не отправлено", "Ожидает ответа", "В диалоге", "Отказ", "Успешно / Заказ", "Думает"
    notes = Column(Text, default="")
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    session = relationship("ParsingSession", back_populates="leads")