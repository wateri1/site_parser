import React from "react";
import { Search, Filter, Loader2, Sparkles, SlidersHorizontal, ArrowRight } from "lucide-react";

const SUGGESTIONS = [
  "Барбершоп Москва",
  "Косметолог СПб",
  "Ремонт квартир Казань",
  "Дизайн интерьера Екатеринбург",
  "Фитнес тренер Сочи",
  "Маникюр Самара"
];

export default function SearchControl({
  query,
  setQuery,
  limit,
  setLimit,
  filterType,
  setFilterType,
  onStartParse,
  isLoading
}) {
  const handleSubmit = (e) => {
    e.preventDefault();
    if (!query.trim() || isLoading) return;
    onStartParse();
  };

  return (
    <div className="bg-slate-900 border border-slate-800/80 rounded-2xl p-5 shadow-xl shadow-slate-950/50 space-y-4">
      
      {/* Search Input Form */}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="flex flex-col md:flex-row gap-3">
          
          {/* Query Field */}
          <div className="relative flex-1">
            <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-500">
              <Search className="w-5 h-5 text-blue-400" />
            </div>
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Введите нишу и город (например: барбершоп москва, косметолог спб)..."
              className="w-full pl-11 pr-4 py-3 bg-slate-950 border border-slate-700/80 rounded-xl text-white placeholder-slate-500 text-sm focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-all shadow-inner"
              disabled={isLoading}
            />
          </div>

          {/* Manual Limit Input */}
          <div className="w-full md:w-48 flex items-center bg-slate-950 border border-slate-700/80 rounded-xl px-3 py-1.5 focus-within:border-blue-500 focus-within:ring-2 focus-within:ring-blue-500/20 transition-all">
            <span className="text-xs text-slate-400 mr-2 whitespace-nowrap">Искать до:</span>
            <input
              type="number"
              min={1}
              max={1000}
              value={limit || ""}
              onChange={(e) => {
                const val = e.target.value;
                setLimit(val === "" ? "" : Math.max(1, parseInt(val) || 1));
              }}
              onBlur={() => {
                if (!limit || limit < 1) setLimit(20);
              }}
              placeholder="20"
              disabled={isLoading}
              className="bg-transparent text-white font-semibold text-sm w-full focus:outline-none font-mono"
            />
            <span className="text-xs text-slate-500 ml-1">лидов</span>
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={isLoading || !query.trim()}
            className="w-full md:w-auto px-6 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed text-white text-sm font-semibold rounded-xl shadow-lg shadow-blue-600/30 flex items-center justify-center space-x-2 transition-all active:scale-[0.98]"
          >
            {isLoading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin text-white" />
                <span>Парсинг через Apify...</span>
              </>
            ) : (
              <>
                <Sparkles className="w-4 h-4 text-amber-300" />
                <span>Найти лидов</span>
                <ArrowRight className="w-4 h-4 opacity-70" />
              </>
            )}
          </button>
        </div>

        {/* Filter Buttons & Suggestions */}
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-3 pt-2 border-t border-slate-800/60">
          
          {/* Target Link Filters */}
          <div className="flex flex-wrap items-center gap-1.5">
            <span className="text-xs font-medium text-slate-400 mr-1 flex items-center gap-1">
              <Filter className="w-3 h-3 text-blue-400" />
              Фильтр сайта:
            </span>

            <button
              type="button"
              onClick={() => setFilterType("all")}
              className={`px-2.5 py-1 rounded-lg text-xs font-medium transition-all ${
                filterType === "all"
                  ? "bg-slate-700 text-white shadow"
                  : "bg-slate-800/40 text-slate-400 hover:text-slate-200 hover:bg-slate-800"
              }`}
            >
              Все подряд
            </button>

            <button
              type="button"
              onClick={() => setFilterType("no_site")}
              className={`px-2.5 py-1 rounded-lg text-xs font-semibold flex items-center space-x-1.5 transition-all ${
                filterType === "no_site"
                  ? "bg-rose-500/20 text-rose-300 border border-rose-500/40 shadow-sm shadow-rose-500/10"
                  : "bg-slate-800/40 text-rose-400/80 hover:text-rose-300 hover:bg-rose-500/10 border border-transparent"
              }`}
            >
              <span className="w-1.5 h-1.5 rounded-full bg-rose-400 animate-pulse"></span>
              <span>Только БЕЗ сайта (Целевые)</span>
            </button>

            <button
              type="button"
              onClick={() => setFilterType("whatsapp")}
              className={`px-2.5 py-1 rounded-lg text-xs font-medium flex items-center space-x-1 transition-all ${
                filterType === "whatsapp"
                  ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/40"
                  : "bg-slate-800/40 text-slate-400 hover:text-slate-200 hover:bg-slate-800 border border-transparent"
              }`}
            >
              <span>Только с WhatsApp</span>
            </button>

            <button
              type="button"
              onClick={() => setFilterType("multilink")}
              className={`px-2.5 py-1 rounded-lg text-xs font-medium flex items-center space-x-1 transition-all ${
                filterType === "multilink"
                  ? "bg-purple-500/20 text-purple-300 border border-purple-500/40"
                  : "bg-slate-800/40 text-slate-400 hover:text-slate-200 hover:bg-slate-800 border border-transparent"
              }`}
            >
              <span>С мультиссылкой (Taplink)</span>
            </button>
          </div>

          {/* Quick Suggestions */}
          <div className="flex items-center gap-1.5 overflow-x-auto pb-1 lg:pb-0 text-xs text-slate-500 scrollbar-none">
            <span className="text-slate-400 whitespace-nowrap">Быстрый выбор:</span>
            {SUGGESTIONS.slice(0, 4).map((s) => (
              <button
                key={s}
                type="button"
                onClick={() => setQuery(s)}
                className="px-2 py-0.5 rounded-md bg-slate-800/60 hover:bg-slate-800 hover:text-slate-300 text-slate-400 transition-colors whitespace-nowrap"
              >
                {s}
              </button>
            ))}
          </div>

        </div>

      </form>
    </div>
  );
}