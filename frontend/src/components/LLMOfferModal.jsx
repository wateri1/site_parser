import React, { useState, useEffect } from "react";
import { X, Sparkles, Copy, Check, Bot, RefreshCw, Send, Sliders, ExternalLink } from "lucide-react";
import { api } from "../services/api";

export default function LLMOfferModal({ isOpen, onClose, lead, onMarkContacted }) {
  const [tone, setTone] = useState("friendly");
  const [loading, setLoading] = useState(false);
  const [offerText, setOfferText] = useState("");
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    if (lead && isOpen) {
      loadOffer(tone);
    }
  }, [lead, isOpen, tone]);

  const loadOffer = async (selectedTone) => {
    if (!lead) return;
    setLoading(true);
    try {
      const res = await api.generateOffer({
        username: lead.username,
        full_name: lead.full_name,
        niche: lead.full_name || "вашей сферы",
        link_type: lead.link_type,
        tone: selectedTone
      });
      setOfferText(res.offer_text);
    } catch (e) {
      console.error(e);
      // Fallback text
      setOfferText(`Здравствуйте, ${lead.full_name || `@${lead.username}`}! Заметил, что у вас в профиле нет сайта для приема клиентов. Подготовил концепт сайта для вас!`);
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen || !lead) return null;

  const handleCopy = () => {
    navigator.clipboard.writeText(offerText);
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
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 backdrop-blur-sm p-4">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-xl shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-200">
        
        {/* Header */}
        <div className="flex items-center justify-between p-4 sm:p-5 border-b border-slate-800 bg-slate-950/40">
          <div className="flex items-center space-x-3">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-purple-600 to-blue-500 text-white flex items-center justify-center shadow-lg shadow-purple-500/20">
              <Bot className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <h3 className="text-base font-bold text-white">AI Генератор Оффера</h3>
                <span className="text-[10px] px-2 py-0.5 rounded-full bg-purple-500/10 text-purple-400 font-semibold border border-purple-500/20">
                  LLM Mock
                </span>
              </div>
              <p className="text-xs text-slate-400">
                Персонализированное коммерческое предложение для <span className="text-blue-400 font-medium">@{lead.username}</span>
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
        <div className="p-5 space-y-4">
          
          {/* Target Lead Badge Summary */}
          <div className="p-3 bg-slate-950/60 border border-slate-800 rounded-xl flex items-center justify-between text-xs">
            <div className="flex items-center space-x-2.5">
              <img
                src={lead.avatar_url || `https://api.dicebear.com/7.x/identicon/svg?seed=${lead.username}`}
                alt={lead.username}
                className="w-8 h-8 rounded-full border border-slate-700 bg-slate-800"
              />
              <div>
                <p className="font-semibold text-slate-200">{lead.full_name || lead.username}</p>
                <p className="text-slate-400">@{lead.username} • {lead.followers_count?.toLocaleString()} подписчиков</p>
              </div>
            </div>
            <div>
              <span className={`px-2 py-0.8 rounded-md text-[11px] font-medium border ${
                lead.link_type === "no_site"
                  ? "bg-rose-500/10 text-rose-300 border-rose-500/30"
                  : "bg-slate-800 text-slate-300 border-slate-700"
              }`}>
                {lead.link_label}
              </span>
            </div>
          </div>

          {/* Tone Selector */}
          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-2 flex items-center gap-1.5">
              <Sliders className="w-3.5 h-3.5 text-blue-400" />
              Стиль и тональность сообщения:
            </label>
            <div className="grid grid-cols-3 gap-2">
              <button
                type="button"
                onClick={() => setTone("friendly")}
                className={`p-2 rounded-xl text-xs font-medium border transition-all text-center ${
                  tone === "friendly"
                    ? "bg-blue-600/20 border-blue-500 text-blue-300 shadow-sm"
                    : "bg-slate-950 border-slate-800 text-slate-400 hover:text-slate-200 hover:bg-slate-800/40"
                }`}
              >
                ✨ Дружелюбный
              </button>

              <button
                type="button"
                onClick={() => setTone("business")}
                className={`p-2 rounded-xl text-xs font-medium border transition-all text-center ${
                  tone === "business"
                    ? "bg-blue-600/20 border-blue-500 text-blue-300 shadow-sm"
                    : "bg-slate-950 border-slate-800 text-slate-400 hover:text-slate-200 hover:bg-slate-800/40"
                }`}
              >
                💼 Деловой B2B
              </button>

              <button
                type="button"
                onClick={() => setTone("bold")}
                className={`p-2 rounded-xl text-xs font-medium border transition-all text-center ${
                  tone === "bold"
                    ? "bg-blue-600/20 border-blue-500 text-blue-300 shadow-sm"
                    : "bg-slate-950 border-slate-800 text-slate-400 hover:text-slate-200 hover:bg-slate-800/40"
                }`}
              >
                ⚡️ Прямой / Оффер
              </button>
            </div>
          </div>

          {/* Generated Textbox */}
          <div className="relative">
            <div className="flex items-center justify-between text-xs text-slate-400 mb-1.5">
              <span>Сгенерированный текст для отправки в Direct:</span>
              <button
                onClick={() => loadOffer(tone)}
                disabled={loading}
                className="text-blue-400 hover:text-blue-300 flex items-center space-x-1 transition-colors"
              >
                <RefreshCw className={`w-3 h-3 ${loading ? "animate-spin" : ""}`} />
                <span>Перегенерировать</span>
              </button>
            </div>

            <textarea
              rows={8}
              value={offerText}
              onChange={(e) => setOfferText(e.target.value)}
              className="w-full p-3.5 bg-slate-950 border border-slate-700/80 rounded-xl text-slate-200 text-xs sm:text-sm leading-relaxed focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 font-sans resize-none"
            />
          </div>

        </div>

        {/* Footer Actions */}
        <div className="flex flex-col sm:flex-row items-center justify-between p-4 bg-slate-950/60 border-t border-slate-800 gap-2">
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
              onClick={handleCopy}
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