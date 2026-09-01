import React from "react";
import { Users, GlobeX, Send, MessageSquareCheck, CheckCircle, Percent } from "lucide-react";

export default function StatsCards({ leads = [] }) {
  const total = leads.length;
  const noSiteCount = leads.filter((l) => l.link_type === "no_site").length;
  const contactedCount = leads.filter((l) => l.contacted).length;
  const repliedCount = leads.filter((l) => 
    l.reply_status && !["Не отправлено", "Ожидает ответа"].includes(l.reply_status)
  ).length;

  const noSitePercentage = total > 0 ? Math.round((noSiteCount / total) * 100) : 0;
  const contactedPercentage = total > 0 ? Math.round((contactedCount / total) * 100) : 0;

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
      
      {/* 1. Total Leads */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-4 flex items-center justify-between">
        <div>
          <p className="text-xs font-medium text-slate-400">Всего найдено лидов</p>
          <p className="text-2xl font-bold text-white mt-1">{total}</p>
        </div>
        <div className="w-10 h-10 rounded-xl bg-blue-500/10 text-blue-400 flex items-center justify-center">
          <Users className="w-5 h-5" />
        </div>
      </div>

      {/* 2. Hot Targets - No Website */}
      <div className="bg-slate-900/90 border border-rose-500/20 bg-gradient-to-br from-slate-900 via-slate-900 to-rose-950/20 rounded-2xl p-4 flex items-center justify-between shadow-sm shadow-rose-950/20">
        <div>
          <div className="flex items-center space-x-1.5">
            <p className="text-xs font-semibold text-rose-400">БЕЗ сайта (Целевые)</p>
            <span className="text-[10px] px-1.5 py-0.2 bg-rose-500/20 text-rose-300 rounded-full font-mono">
              {noSitePercentage}%
            </span>
          </div>
          <p className="text-2xl font-bold text-rose-200 mt-1">{noSiteCount}</p>
        </div>
        <div className="w-10 h-10 rounded-xl bg-rose-500/10 text-rose-400 flex items-center justify-center">
          <GlobeX className="w-5 h-5" />
        </div>
      </div>

      {/* 3. Contacted */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-4 flex items-center justify-between">
        <div>
          <div className="flex items-center space-x-1.5">
            <p className="text-xs font-medium text-slate-400">Написали оффер</p>
            <span className="text-[10px] px-1.5 py-0.2 bg-emerald-500/20 text-emerald-300 rounded-full font-mono">
              {contactedPercentage}%
            </span>
          </div>
          <p className="text-2xl font-bold text-emerald-400 mt-1">{contactedCount}</p>
        </div>
        <div className="w-10 h-10 rounded-xl bg-emerald-500/10 text-emerald-400 flex items-center justify-center">
          <Send className="w-5 h-5" />
        </div>
      </div>

      {/* 4. Active dialogues */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-4 flex items-center justify-between">
        <div>
          <p className="text-xs font-medium text-slate-400">В диалоге / Ответили</p>
          <p className="text-2xl font-bold text-indigo-300 mt-1">{repliedCount}</p>
        </div>
        <div className="w-10 h-10 rounded-xl bg-indigo-500/10 text-indigo-400 flex items-center justify-center">
          <MessageSquareCheck className="w-5 h-5" />
        </div>
      </div>

    </div>
  );
}