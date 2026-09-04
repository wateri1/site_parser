from pydantic import BaseModel
from typing import Optional, List
import datetime

class ParseRequest(BaseModel):
    query: str
    limit: int = 20
    search_type: str = "user" # "user", "hashtag", "place"
    filter_type: str = "all" # "all", "no_site", "whatsapp", "multilink"
    apify_token: Optional[str] = None
    is_mock: bool = False

class LeadUpdate(BaseModel):
    contacted: Optional[bool] = None
    reply_status: Optional[str] = None
    notes: Optional[str] = None

class LeadResponse(BaseModel):
    id: int
    session_id: str
    username: str
    full_name: str
    profile_url: str
    avatar_url: Optional[str] = None
    followers_count: int
    biography: str
    external_url: Optional[str] = None
    link_type: str
    link_label: str
    has_website: bool
    has_whatsapp: bool
    has_other_links: bool
    contacted: bool
    reply_status: str
    notes: str
    created_at: datetime.datetime

    class Config:
        from_attributes = True

class SessionResponse(BaseModel):
    id: str
    title: str
    query: str
    limit: int
    filter_type: str
    created_at: datetime.datetime
    status: str
    total_leads: int
    leads_without_site: int
    contacted_count: Optional[int] = 0

    class Config:
        from_attributes = True

class SessionDetailResponse(SessionResponse):
    leads: List[LeadResponse] = []

class OfferRequest(BaseModel):
    username: str
    full_name: Optional[str] = ""
    niche: Optional[str] = ""
    link_type: Optional[str] = "no_site"
    link_label: Optional[str] = ""
    biography: Optional[str] = ""
    followers_count: Optional[int] = 0
    tone: str = "friendly" # "friendly", "business", "bold"
    mode: Optional[str] = "template" # "template" or "chatgpt"
    openai_api_key: Optional[str] = None

class OfferResponse(BaseModel):
    subject: str
    offer_text: str
    strategy_breakdown: Optional[str] = None
    subject_lines: Optional[List[str]] = []
    is_chatgpt: bool = False