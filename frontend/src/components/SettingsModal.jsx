import React, { useState } from "react";
import { X, Key, ExternalLink, ShieldCheck, Sparkles, AlertCircle } from "lucide-react";

export default function SettingsModal({
  isOpen,
  onClose,
  apifyToken,
  onSaveToken,
  openaiKey,
  onSaveOpenaiKey
}) {
  const [tokenInput, setTokenInput] = useState(apifyToken || "");
  const [openaiInput, setOpenaiInput] = useState(openaiKey || "");

  if (!isOpen) return null;

  const handleSave = () => {
    onSaveToken(tokenInput.trim());
    if (onSaveOpenaiKey) {
      onSaveOpenaiKey(openaiInput.trim());
    }
    onClose();
  };

  const handleClear = () => {
    setTokenInput("");
    setOpenaiInput("");
    onSaveToken("");
    if (onSaveOpenaiKey) {
      onSaveOpenaiKey("");
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 backdrop-blur-sm p-4">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-lg shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-200">
        
        {/* Header */}
        <div className="flex items-center justify-between p-5 border-b border-slate-800">
          <div className="flex items-center space-x-2.5">
            <div className="w-8 h-8 rounded-lg bg-blue-500/10 text-blue-400 flex items-center justify-center">
              <Key className="w-4 h-4" />
            </div>
            <h3 className="text-base font-semibold text-white">Настройки API (Apify + OpenAI)</h3>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-5">
          {/* Apify Token */}
          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1.5">
              Personal API Token (Apify Instagram Scraper)
            </label>
            <input
              type="password"
              value={tokenInput}
              onChange={(e) => setTokenInput(e.target.value)}
              placeholder="apify_api_xxxxxxxxxxxxxxxxxxxxxxxx"
              className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-700 rounded-xl text-sm text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors font-mono"
            />
            <p className="text-xs text-slate-400 mt-1.5 flex items-center gap-1">
              <span>Получить токен бесплатно можно в консоли</span>
              <a
                href="https://console.apify.com/account/integrations"
                target="_blank"
                rel="noreferrer"
                className="text-blue-400 hover:underline inline-flex items-center gap-0.5"
              >
                Apify Integrations <ExternalLink className="w-3 h-3" />
              </a>
            </p>
          </div>

          {/* OpenAI API Key */}
          <div>
            <div className="flex items-center justify-between mb-1.5">
              <label className="block text-xs font-medium text-slate-300">
                OpenAI API Key (ChatGPT для генерации офферов)
              </label>
              <span className="text-[10px] px-1.5 py-0.5 rounded bg-purple-500/10 text-purple-400 border border-purple-500/20 font-mono">
                GPT-4o
              </span>
            </div>
            <input
              type="password"
              value={openaiInput}
              onChange={(e) => setOpenaiInput(e.target.value)}
              placeholder="sk-proj-xxxxxxxxxxxxxxxxxxxxxxxx"
              className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-700 rounded-xl text-sm text-white placeholder-slate-500 focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500 transition-colors font-mono"
            />
            <p className="text-xs text-slate-400 mt-1.5">
              Используется для кнопки «Сгенерировать под наш бизнес» по методикам The Challenger Sale & Predictable Revenue.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
            <div className="flex items-center space-x-2 text-slate-300 font-medium text-xs">
              <Sparkles className="w-4 h-4 text-amber-400" />
              <span>Формат запроса к Apify (Instagram Search Scraper)</span>
            </div>
            <p className="text-xs text-slate-400 leading-relaxed">
              Парсинг работает по официальной структуре актора <code className="text-blue-400 font-mono">apify/instagram-search-scraper</code>:
            </p>
            <pre className="p-2.5 rounded-lg bg-slate-900 border border-slate-800 text-[11px] text-slate-300 font-mono overflow-x-auto">
{`{
  "search": "адвокат Алматы",
  "searchType": "user",
  "searchLimit": 20,
  "resultsLimit": 20
}`}
            </pre>
          </div>

          <div className="flex items-center space-x-2 text-xs text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 p-3 rounded-xl">
            <ShieldCheck className="w-4 h-4 flex-shrink-0" />
            <span>Токен сохраняется локально в вашем браузере (LocalStorage) и используется только для запросов к Apify.</span>
          </div>
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between p-4 bg-slate-950/50 border-t border-slate-800">
          <button
            onClick={handleClear}
            className="px-3 py-2 text-xs text-rose-400 hover:bg-rose-500/10 rounded-lg transition-colors"
          >
            Сбросить токен
          </button>

          <div className="flex items-center space-x-2">
            <button
              onClick={onClose}
              className="px-4 py-2 text-xs font-medium text-slate-300 hover:bg-slate-800 rounded-xl transition-colors"
            >
              Отмена
            </button>
            <button
              onClick={handleSave}
              className="px-4 py-2 text-xs font-semibold text-white bg-blue-600 hover:bg-blue-500 rounded-xl shadow-md shadow-blue-600/20 transition-all"
            >
              Сохранить
            </button>
          </div>
        </div>

      </div>
    </div>
  );
}