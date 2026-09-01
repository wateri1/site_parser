import React from "react";
import { Search, Database, Settings, Sparkles, Key, CheckCircle2 } from "lucide-react";

export default function Navbar({ activeTab, setActiveTab, onOpenSettings, apifyToken, sessionsCount = 0 }) {
  return (
    <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur-md sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        
        {/* Logo */}
        <div className="flex items-center space-x-3 cursor-pointer" onClick={() => setActiveTab("main")}>
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 via-indigo-500 to-purple-500 flex items-center justify-center shadow-lg shadow-blue-500/20 text-white">
            <Sparkles className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="text-lg font-bold text-white tracking-tight">LeadHunter</span>
              <span className="text-xs px-2 py-0.5 rounded-full bg-blue-500/10 text-blue-400 font-semibold border border-blue-500/20">
                Apify AI
              </span>
            </div>
            <p className="text-xs text-slate-400 hidden sm:block">Парсер лидов без сайтов & CRM-трекер</p>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="flex items-center space-x-1 sm:space-x-2 bg-slate-950/60 p-1 rounded-xl border border-slate-800">
          <button
            onClick={() => setActiveTab("main")}
            className={`flex items-center space-x-2 px-3.5 py-1.5 rounded-lg text-sm font-medium transition-all ${
              activeTab === "main"
                ? "bg-blue-600 text-white shadow-md shadow-blue-600/30"
                : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/60"
            }`}
          >
            <Search className="w-4 h-4" />
            <span>Парсер & Трекер</span>
          </button>

          <button
            onClick={() => setActiveTab("archive")}
            className={`flex items-center space-x-2 px-3.5 py-1.5 rounded-lg text-sm font-medium transition-all ${
              activeTab === "archive"
                ? "bg-blue-600 text-white shadow-md shadow-blue-600/30"
                : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/60"
            }`}
          >
            <Database className="w-4 h-4" />
            <span>База сессий</span>
            {sessionsCount > 0 && (
              <span className="ml-1.5 px-1.5 py-0.5 text-xs rounded-full bg-slate-800 text-slate-300 font-mono">
                {sessionsCount}
              </span>
            )}
          </button>
        </nav>

        {/* Settings & Status */}
        <div className="flex items-center space-x-2">
          <button
            onClick={onOpenSettings}
            className={`flex items-center space-x-2 px-3 py-1.5 rounded-lg text-xs font-medium border transition-colors ${
              apifyToken
                ? "bg-emerald-500/10 border-emerald-500/30 text-emerald-400 hover:bg-emerald-500/20"
                : "bg-slate-800/60 border-slate-700 text-slate-300 hover:bg-slate-800"
            }`}
            title="Настройки Apify API"
          >
            {apifyToken ? (
              <>
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                <span className="hidden md:inline">Apify подключен</span>
              </>
            ) : (
              <>
                <Key className="w-3.5 h-3.5 text-amber-400" />
                <span className="hidden md:inline">Apify (Демо-режим)</span>
              </>
            )}
            <Settings className="w-3.5 h-3.5 ml-1 text-slate-400" />
          </button>
        </div>

      </div>
    </header>
  );
}