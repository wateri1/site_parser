import React, { useState, useEffect } from "react";
import { 
  Database, Calendar, Users, GlobeX, Download, Trash2, 
  ExternalLink, Search, RefreshCw, ArrowUpRight, CheckCircle2 
} from "lucide-react";
import { api } from "../services/api";

export default function ArchivePage({ onSelectSession }) {
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchFilter, setSearchFilter] = useState("");

  const loadSessions = async () => {
    setLoading(true);
    try {
      const data = await api.getSessions();
      setSessions(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadSessions();
  }, []);

  const handleDeleteSession = async (e, sessionId) => {
    e.stopPropagation();
    if (!window.confirm("Вы уверены, что хотите удалить эту сохраненную таблицу?")) return;
    try {
      await api.deleteSession(sessionId);
      setSessions((prev) => prev.filter((s) => s.id !== sessionId));
    } catch (err) {
      alert("Ошибка при удалении сессии");
    }
  };

  const handleDownloadExcel = (e, sessionId) => {
    e.stopPropagation();
    window.open(api.getExportUrl(sessionId), "_blank");
  };

  const filteredSessions = sessions.filter((s) =>
    s.title?.toLowerCase().includes(searchFilter.toLowerCase()) ||
    s.query?.toLowerCase().includes(searchFilter.toLowerCase())
  );

  return (
    <div className="space-y-6">
      
      {/* Header bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl">
        <div>
          <div className="flex items-center space-x-2.5">
            <div className="w-9 h-9 rounded-xl bg-blue-500/10 text-blue-400 flex items-center justify-center">
              <Database className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-white tracking-tight">База сохраненных таблиц</h2>
              <p className="text-xs text-slate-400">История всех ваших парсингов и собранных баз лидов</p>
            </div>
          </div>
        </div>

        <div className="flex items-center space-x-2">
          <div className="relative flex-1 sm:flex-initial">
            <Search className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
            <input
              type="text"
              value={searchFilter}
              onChange={(e) => setSearchFilter(e.target.value)}
              placeholder="Поиск по сессиям..."
              className="pl-8 pr-3 py-1.5 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 w-full sm:w-48"
            />
          </div>

          <button
            onClick={loadSessions}
            disabled={loading}
            className="p-2 bg-slate-950 border border-slate-800 hover:border-slate-700 text-slate-300 rounded-xl text-xs flex items-center transition-colors"
            title="Обновить список"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? "animate-spin" : ""}`} />
          </button>
        </div>
      </div>

      {/* Grid of Sessions */}
      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-44 rounded-2xl bg-slate-900/50 border border-slate-800/60 animate-pulse" />
          ))}
        </div>
      ) : filteredSessions.length === 0 ? (
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-12 text-center text-slate-400 space-y-3">
          <Database className="w-12 h-12 text-slate-600 mx-auto" />
          <h3 className="text-base font-semibold text-slate-200">Пока нет сохраненных таблиц</h3>
          <p className="text-xs text-slate-400 max-w-md mx-auto">
            Запустите ваш первый поиск на главной странице, и сформированная таблица автоматически сохранится здесь.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredSessions.map((session) => {
            const formattedDate = new Date(session.created_at).toLocaleDateString("ru-RU", {
              day: "2-digit",
              month: "short",
              hour: "2-digit",
              minute: "2-digit"
            });

            return (
              <div
                key={session.id}
                onClick={() => onSelectSession(session.id)}
                className="group bg-slate-900 border border-slate-800 hover:border-blue-500/50 rounded-2xl p-5 shadow-lg transition-all hover:shadow-blue-500/5 cursor-pointer flex flex-col justify-between space-y-4 relative"
              >
                <div>
                  <div className="flex items-start justify-between">
                    <div>
                      <span className="text-[11px] font-mono px-2 py-0.5 rounded-full bg-slate-950 text-slate-400 border border-slate-800">
                        {formattedDate}
                      </span>
                      <h3 className="text-base font-bold text-white group-hover:text-blue-400 transition-colors mt-2 tracking-tight">
                        {session.title}
                      </h3>
                    </div>
                    <ArrowUpRight className="w-4 h-4 text-slate-500 group-hover:text-blue-400 transition-colors" />
                  </div>

                  {/* Badges / Metrics */}
                  <div className="grid grid-cols-2 gap-2 mt-4">
                    <div className="bg-slate-950/70 border border-slate-800/80 rounded-xl p-2.5">
                      <p className="text-[10px] text-slate-400 font-medium">Всего лидов</p>
                      <p className="text-base font-bold text-white mt-0.5 flex items-center gap-1">
                        <Users className="w-3.5 h-3.5 text-blue-400" />
                        {session.total_leads}
                      </p>
                    </div>

                    <div className="bg-rose-950/20 border border-rose-500/20 rounded-xl p-2.5">
                      <p className="text-[10px] text-rose-400 font-medium">БЕЗ сайта</p>
                      <p className="text-base font-bold text-rose-300 mt-0.5 flex items-center gap-1">
                        <GlobeX className="w-3.5 h-3.5 text-rose-400" />
                        {session.leads_without_site}
                      </p>
                    </div>
                  </div>
                </div>

                {/* Footer Buttons */}
                <div className="flex items-center justify-between pt-3 border-t border-slate-800/70">
                  <span className="text-[11px] text-slate-400 group-hover:text-blue-400 font-medium flex items-center gap-1">
                    Открыть в CRM
                  </span>

                  <div className="flex items-center space-x-1">
                    <button
                      type="button"
                      onClick={(e) => handleDownloadExcel(e, session.id)}
                      className="p-1.5 rounded-lg bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 border border-emerald-500/20 transition-colors"
                      title="Скачать Excel (.xlsx)"
                    >
                      <Download className="w-3.5 h-3.5" />
                    </button>

                    <button
                      type="button"
                      onClick={(e) => handleDeleteSession(e, session.id)}
                      className="p-1.5 rounded-lg bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 border border-rose-500/20 transition-colors"
                      title="Удалить таблицу"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </div>
                </div>

              </div>
            );
          })}
        </div>
      )}

    </div>
  );
}