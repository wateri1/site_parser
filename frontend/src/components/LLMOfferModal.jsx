import React, { useState, useEffect } from "react";
import { 
  X, Sparkles, Copy, Check, Bot, RefreshCw, Send, Sliders, ExternalLink, 
  Zap, BrainCircuit, ShieldAlert, CheckCircle2, ChevronDown, ChevronUp, FileText, Mail
} from "lucide-react";
import { api } from "../services/api";

export default function LLMOfferModal({ isOpen, onClose, lead, onMarkContacted, openaiApiKey }) {
  const [activeTab, setActiveTab] = useState("chatgpt"); // "chatgpt" or "template"
  const [tone, setTone] = useState("business");
  const [loading, setLoading] = useState(false);
  const [offerText, setOfferText] = useState("");
  const [subjectLines, setSubjectLines] = useState([]);
  const [strategyBreakdown, setStrategyBreakdown] = useState("");
  const [isChatGptResult, setIsChatGptResult] = useState(false);
  const [copied, setCopied] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");
  const [showBreakdown, setShowBreakdown] = useState(true);

  // Auto-generate on open
  useEffect(() => {
    if (lead && isOpen) {
      setErrorMsg("");
      loadOffer(activeTab, tone);
    }
  }, [lead, isOpen]);

  const loadOffer = async (modeToUse = activeTab, selectedTone = tone) => {
    if (!lead) return;
    setLoading(true);
    setErrorMsg("");
    try {
      const res = await api.generateOffer({
        username: lead.username,
        full_name: lead.full_name,
        niche: lead.full_name || "вашей нише",
        link_type: lead.link_type,
        link_label: lead.link_label,
        biography: lead.biography,
        followers_count: lead.followers_count,
        tone: selectedTone,
        mode: modeToUse,
        openai_api_key: openaiApiKey
      });

      setOfferText(res.offer_text);
      setSubjectLines(res.subject_lines || []);
      setStrategyBreakdown(res.strategy_breakdown || "");
      setIsChatGptResult(!!res.is_chatgpt);
    } catch (e) {
      console.error(e);
      const err = e.response?.data?.detail || e.message || "Ошибка при генерации оффера";
      setErrorMsg(err);
      // If ChatGPT failed, fallback to base template
      if (modeToUse === "chatgpt") {
        setOfferText(`Здравствуйте, ${lead.full_name || `@${lead.username}`}!\n\nЗаметил, что у вас в профиле нет сайта для приема клиентов. Мы разработали концепт конверсионного сайта под вашу сферу с автоматической записью.\n\nИмеет смысл показать короткое превью структуры?`);
        setIsChatGptResult(false);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleModeSwitch = (newMode) => {
    setActiveTab(newMode);
    loadOffer(newMode, tone);
  };

  const handleToneSelect = (newTone) => {
    setTone(newTone);
    setActiveTab("template");
    loadOffer("template", newTone);
  };

  const handleTriggerChatGpt = () => {
    setActiveTab("chatgpt");
    loadOffer("chatgpt", tone);
  };

  if (!isOpen || !lead) return null;

  const wordCount = offerText ? offerText.trim().split(/\s+/).filter(Boolean).length : 0;
  const hasExclamation = offerText.includes("!");

  const handleCopy = (textToCopy = offerText) => {
    navigator.clipboard.writeText(textToCopy);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleCopyAndMark = () => {
    handleCopy();
    if (onMarkContacted) {
      onMarkContacted(lead.id);
    }
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/85 backdrop-blur-sm p-3 sm:p-4 overflow-y-auto">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-2xl shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-200 my-auto">
        
        {/* Header */}
        <div className="flex items-center justify-between p-4 sm:p-5 border-b border-slate-800 bg-slate-950/50">
          <div className="flex items-center space-x-3">
            <div className={`w-9 h-9 rounded-xl flex items-center justify-center shadow-lg ${
              isChatGptResult 
                ? "bg-gradient-to-tr from-purple-600 via-indigo-600 to-blue-500 text-white shadow-purple-500/20"
                : "bg-slate-800 text-blue-400 border border-slate-700"
            }`}>
              {isChatGptResult ? <Zap className="w-5 h-5 text-amber-300" /> : <Bot className="w-5 h-5" />}
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <h3 className="text-base font-bold text-white">Генератор B2B Офферов</h3>
                {isChatGptResult ? (
                  <span className="text-[10px] px-2 py-0.5 rounded-full bg-gradient-to-r from-purple-500/20 to-blue-500/20 text-purple-300 font-semibold border border-purple-500/30 flex items-center gap-1">
                    <Sparkles className="w-2.5 h-2.5 text-amber-400" />
                    ChatGPT • Elite B2B
                  </span>
                ) : (
                  <span className="text-[10px] px-2 py-0.5 rounded-full bg-slate-800 text-slate-400 font-medium border border-slate-700">
                    Базовый шаблон
                  </span>
                )}
              </div>
              <p className="text-xs text-slate-400">
                Оффер на разработку сайта для <span className="text-blue-400 font-medium">@{lead.username}</span>
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Body */}
        <div className="p-4 sm:p-5 space-y-4 max-h-[75vh] overflow-y-auto scrollbar-thin scrollbar-thumb-slate-800">
          
          {/* Target Lead Badge Summary */}
          <div className="p-3 bg-slate-950/60 border border-slate-800 rounded-xl flex items-center justify-between text-xs gap-2">
            <div className="flex items-center space-x-2.5 min-w-0">
              <img
                src={lead.avatar_url || `https://api.dicebear.com/7.x/identicon/svg?seed=${lead.username}`}
                alt={lead.username}
                className="w-8 h-8 rounded-full border border-slate-700 bg-slate-800 flex-shrink-0"
              />
              <div className="min-w-0">
                <p className="font-semibold text-slate-200 truncate">{lead.full_name || lead.username}</p>
                <p className="text-slate-400 truncate">@{lead.username} • {lead.followers_count?.toLocaleString()} подписчиков</p>
              </div>
            </div>
            <div className="flex-shrink-0">
              <span className={`px-2 py-0.5 rounded-md text-[11px] font-medium border ${
                lead.link_type === "no_site"
                  ? "bg-rose-500/10 text-rose-300 border-rose-500/30"
                  : "bg-slate-800 text-slate-300 border-slate-700"
              }`}>
                {lead.link_label}
              </span>
            </div>
          </div>

          {/* PRIMARY ACTION: Generate for OUR BUSINESS with ChatGPT */}
          <div className="p-3.5 rounded-xl bg-gradient-to-r from-purple-950/40 via-indigo-950/30 to-blue-950/40 border border-purple-500/30 space-y-2.5 shadow-lg shadow-purple-950/30">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <BrainCircuit className="w-4 h-4 text-purple-400" />
                <span className="text-xs font-bold text-purple-200 uppercase tracking-wider">
                  Промпт 2026: Elite B2B Outbound Copywriter
                </span>
              </div>
              <span className="text-[10px] text-purple-300/80 font-mono hidden sm:inline">
                Challenger Sale • PAS • 50-85 слов
              </span>
            </div>

            <button
              type="button"
              onClick={handleTriggerChatGpt}
              disabled={loading}
              className="w-full py-2.5 px-4 bg-gradient-to-r from-purple-600 via-indigo-600 to-blue-600 hover:from-purple-500 hover:to-blue-500 disabled:opacity-50 text-white rounded-xl text-xs sm:text-sm font-bold flex items-center justify-center space-x-2 shadow-lg shadow-purple-600/30 transition-all active:scale-[0.99]"
            >
              {loading && activeTab === "chatgpt" ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin text-white" />
                  <span>ChatGPT анализирует боли профиля и пишет оффер...</span>
                </>
              ) : (
                <>
                  <Zap className="w-4 h-4 text-amber-300 fill-amber-300" />
                  <span>⚡️ Сгенерировать под наш бизнес (ChatGPT)</span>
                </>
              )}
            </button>
            <p className="text-[11px] text-slate-400 leading-tight text-center sm:text-left">
              Генерирует строго целевое сообщение под наш продукт (продажа сайтов и квизов тем, у кого только WhatsApp / нет сайта) без «воды», клише и спам-триггеров.
            </p>
          </div>

          {/* SECONDARY: Standard Templates Selector */}
          <div className="pt-1">
            <div className="flex items-center justify-between mb-2">
              <label className="text-xs font-semibold text-slate-400 flex items-center gap-1.5">
                <Sliders className="w-3.5 h-3.5 text-blue-400" />
                Или выберите базовый быстрый шаблон:
              </label>
              <span className="text-[10px] text-slate-500">Без расхода токенов AI</span>
            </div>
            <div className="grid grid-cols-3 gap-2">
              <button
                type="button"
                onClick={() => handleToneSelect("friendly")}
                className={`p-2 rounded-xl text-xs font-medium border transition-all text-center ${
                  activeTab === "template" && tone === "friendly"
                    ? "bg-blue-600/20 border-blue-500 text-blue-300 shadow-sm"
                    : "bg-slate-950/60 border-slate-800 text-slate-400 hover:text-slate-200 hover:bg-slate-800/40"
                }`}
              >
                ✨ Дружелюбный
              </button>

              <button
                type="button"
                onClick={() => handleToneSelect("business")}
                className={`p-2 rounded-xl text-xs font-medium border transition-all text-center ${
                  activeTab === "template" && tone === "business"
                    ? "bg-blue-600/20 border-blue-500 text-blue-300 shadow-sm"
                    : "bg-slate-950/60 border-slate-800 text-slate-400 hover:text-slate-200 hover:bg-slate-800/40"
                }`}
              >
                💼 Деловой B2B
              </button>

              <button
                type="button"
                onClick={() => handleToneSelect("bold")}
                className={`p-2 rounded-xl text-xs font-medium border transition-all text-center ${
                  activeTab === "template" && tone === "bold"
                    ? "bg-blue-600/20 border-blue-500 text-blue-300 shadow-sm"
                    : "bg-slate-950/60 border-slate-800 text-slate-400 hover:text-slate-200 hover:bg-slate-800/40"
                }`}
              >
                ⚡️ Прямой / Оффер
              </button>
            </div>
          </div>

          {/* Error Message if any */}
          {errorMsg && (
            <div className="p-3 rounded-xl bg-rose-500/10 border border-rose-500/20 text-xs text-rose-300 flex items-center space-x-2">
              <ShieldAlert className="w-4 h-4 flex-shrink-0 text-rose-400" />
              <span>{errorMsg}</span>
            </div>
          )}

          {/* Subject Lines Pill if present */}
          {subjectLines && subjectLines.length > 0 && isChatGptResult && (
            <div className="p-2.5 rounded-xl bg-slate-950/80 border border-slate-800 space-y-1.5">
              <span className="text-[11px] font-semibold text-slate-400 flex items-center gap-1">
                <Mail className="w-3 h-3 text-purple-400" />
                Варианты тем (для почты / заголовка):
              </span>
              <div className="flex flex-wrap gap-1.5">
                {subjectLines.map((subj, idx) => (
                  <button
                    key={idx}
                    type="button"
                    onClick={() => handleCopy(subj)}
                    title="Нажмите, чтобы скопировать тему"
                    className="px-2.5 py-1 rounded-lg text-xs bg-slate-900 border border-slate-700/80 hover:border-purple-500 text-purple-300 hover:text-white transition-colors flex items-center gap-1.5 font-mono"
                  >
                    <span>{subj}</span>
                    <Copy className="w-2.5 h-2.5 opacity-60" />
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Generated Textbox */}
          <div className="space-y-1.5">
            <div className="flex items-center justify-between text-xs text-slate-400">
              <span className="font-medium text-slate-300 flex items-center gap-1.5">
                <FileText className="w-3.5 h-3.5 text-blue-400" />
                Готовое сообщение для отправки в Direct / WhatsApp:
              </span>
              <div className="flex items-center space-x-2 text-[11px]">
                {isChatGptResult && (
                  <span className={`px-2 py-0.5 rounded font-mono ${
                    wordCount >= 50 && wordCount <= 85 
                      ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20" 
                      : "bg-slate-800 text-slate-400"
                  }`}>
                    {wordCount} слов {wordCount >= 50 && wordCount <= 85 ? "✓" : ""}
                  </span>
                )}
                <button
                  onClick={() => loadOffer(activeTab, tone)}
                  disabled={loading}
                  className="text-blue-400 hover:text-blue-300 flex items-center space-x-1 transition-colors"
                >
                  <RefreshCw className={`w-3 h-3 ${loading ? "animate-spin" : ""}`} />
                  <span>Обновить</span>
                </button>
              </div>
            </div>

            <textarea
              rows={7}
              value={offerText}
              onChange={(e) => setOfferText(e.target.value)}
              placeholder={loading ? "Генерация персонализированного оффера..." : ""}
              className="w-full p-3.5 bg-slate-950 border border-slate-700/80 rounded-xl text-slate-200 text-xs sm:text-sm leading-relaxed focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500 font-sans resize-none"
            />
          </div>

          {/* Strategy Breakdown Card (When generated by ChatGPT) */}
          {strategyBreakdown && isChatGptResult && (
            <div className="rounded-xl border border-slate-800 bg-slate-950/60 overflow-hidden">
              <button
                type="button"
                onClick={() => setShowBreakdown(!showBreakdown)}
                className="w-full px-3.5 py-2 flex items-center justify-between text-xs font-semibold text-slate-400 hover:text-slate-200 transition-colors"
              >
                <div className="flex items-center space-x-1.5">
                  <Sparkles className="w-3.5 h-3.5 text-amber-400" />
                  <span>Разбор B2B-стратегии и психологии оффера</span>
                </div>
                {showBreakdown ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
              </button>
              {showBreakdown && (
                <div className="px-3.5 pb-3 pt-1 text-[11px] text-slate-300 font-mono leading-relaxed whitespace-pre-wrap border-t border-slate-800/60 bg-slate-950/40">
                  {strategyBreakdown}
                </div>
              )}
            </div>
          )}

        </div>

        {/* Footer Actions */}
        <div className="flex flex-col sm:flex-row items-center justify-between p-4 bg-slate-950/70 border-t border-slate-800 gap-2.5">
          <a
            href={lead.profile_url}
            target="_blank"
            rel="noreferrer"
            className="text-xs text-slate-400 hover:text-blue-400 flex items-center gap-1 transition-colors order-2 sm:order-1"
          >
            <span>Открыть Instagram @{lead.username}</span>
            <ExternalLink className="w-3 h-3" />
          </a>

          <div className="flex items-center space-x-2 w-full sm:w-auto order-1 sm:order-2">
            <button
              onClick={() => handleCopy()}
              className="flex-1 sm:flex-initial px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-xl text-xs font-semibold flex items-center justify-center space-x-1.5 transition-colors"
            >
              {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
              <span>{copied ? "Скопировано!" : "Скопировать"}</span>
            </button>

            <button
              onClick={handleCopyAndMark}
              className="flex-1 sm:flex-initial px-4 py-2 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white rounded-xl text-xs font-semibold flex items-center justify-center space-x-1.5 shadow-md shadow-blue-600/20 transition-all"
            >
              <Send className="w-3.5 h-3.5" />
              <span>Скопировать и отметить "Писал"</span>
            </button>
          </div>
        </div>

      </div>
    </div>
  );
}