import React, { useState } from "react";
import { 
  Download, Columns, Trash2, Sparkles, ExternalLink, Globe, 
  MessageCircle, Link as LinkIcon, CheckCircle2, Circle, AlertCircle, 
  Search, Filter, ChevronRight, UserMinus, ShieldAlert
} from "lucide-react";
import { api } from "../services/api";

const STATUS_OPTIONS = [
  { value: "Не отправлено", label: "Не отправлено", color: "bg-slate-800 text-slate-400 border-slate-700" },
  { value: "Ожидает ответа", label: "Ожидает ответа", color: "bg-amber-500/10 text-amber-400 border-amber-500/30" },
  { value: "В диалоге", label: "В диалоге", color: "bg-blue-500/10 text-blue-400 border-blue-500/30" },
  { value: "Думает", label: "Думает", color: "bg-purple-500/10 text-purple-400 border-purple-500/30" },
  { value: "Отказ", label: "Отказ / Не надо", color: "bg-rose-500/10 text-rose-400 border-rose-500/30" },
  { value: "Успешно / Заказ", label: "Заказ сайта 🎉", color: "bg-emerald-500/10 text-emerald-300 border-emerald-500/40" },
];

export default function LeadTrackerTable({
  session,
  leads = [],
  onUpdateLead,
  onDeleteLead,
  columns,
  onOpenColumnSettings,
  onOpenOfferModal
}) {
  const [searchTerm, setSearchTerm] = useState("");
  const [filterLinkType, setFilterLinkType] = useState("all");

  // Local filtering
  const filteredLeads = leads.filter((lead) => {
    const matchesSearch =
      lead.username.toLowerCase().includes(searchTerm.toLowerCase()) ||
      lead.full_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      lead.biography?.toLowerCase().includes(searchTerm.toLowerCase());

    const matchesLink =
      filterLinkType === "all" ||
      (filterLinkType === "no_site" && lead.link_type === "no_site") ||
      (filterLinkType === "has_site" && lead.link_type === "has_site") ||
      (filterLinkType === "whatsapp" && lead.link_type === "whatsapp") ||
      (filterLinkType === "multilink" && lead.link_type === "multilink");

    return matchesSearch && matchesLink;
  });

  const handleToggleContacted = (lead) => {
    const newContacted = !lead.contacted;
    onUpdateLead(lead.id, {
      contacted: newContacted,
      reply_status: newContacted && lead.reply_status === "Не отправлено" ? "Ожидает ответа" : lead.reply_status
    });
  };

  const handleStatusChange = (leadId, newStatus) => {
    onUpdateLead(leadId, { reply_status: newStatus });
  };

  const handleNotesChange = (leadId, notes) => {
    onUpdateLead(leadId, { notes });
  };

  const handleExcelExport = () => {
    if (!session?.id) return;
    window.open(api.getExportUrl(session.id), "_blank");
  };

  const renderLinkBadge = (lead) => {
    switch (lead.link_type) {
      case "no_site":
        return (
          <div className="flex flex-col space-y-1">
            <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold bg-rose-500/10 text-rose-300 border border-rose-500/30 w-fit">
              <span className="w-1.5 h-1.5 rounded-full bg-rose-400 mr-1.5 animate-pulse"></span>
              {lead.link_label || "БЕЗ сайта (Клиент!)"}
            </span>
            {lead.external_url && (
              <a
                href={lead.external_url.startsWith("http") ? lead.external_url : `https://${lead.external_url}`}
                target="_blank"
                rel="noreferrer"
                className="text-[11px] text-slate-400 hover:text-rose-300 truncate max-w-[140px] flex items-center gap-0.5"
                title={lead.external_url}
              >
                {lead.external_url} <ExternalLink className="w-2.5 h-2.5 flex-shrink-0" />
              </a>
            )}
          </div>
        );
      case "whatsapp":
        return (
          <div className="flex flex-col space-y-1">
            <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 w-fit">
              <MessageCircle className="w-3 h-3 mr-1" />
              {lead.link_label || "WhatsApp"}
            </span>
            {lead.external_url && (
              <a
                href={lead.external_url.startsWith("http") ? lead.external_url : `https://${lead.external_url}`}
                target="_blank"
                rel="noreferrer"
                className="text-[11px] text-slate-400 hover:text-emerald-400 truncate max-w-[140px] flex items-center gap-0.5"
              >
                {lead.external_url} <ExternalLink className="w-2.5 h-2.5 flex-shrink-0" />
              </a>
            )}
          </div>
        );
      case "multilink":
        return (
          <div className="flex flex-col space-y-1">
            <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-purple-500/10 text-purple-300 border border-purple-500/30 w-fit">
              <LinkIcon className="w-3 h-3 mr-1" />
              {lead.link_label || "Мультиссылка (Taplink)"}
            </span>
            {lead.external_url && (
              <a
                href={lead.external_url.startsWith("http") ? lead.external_url : `https://${lead.external_url}`}
                target="_blank"
                rel="noreferrer"
                className="text-[11px] text-slate-400 hover:text-purple-300 truncate max-w-[140px] flex items-center gap-0.5"
              >
                {lead.external_url} <ExternalLink className="w-2.5 h-2.5 flex-shrink-0" />
              </a>
            )}
          </div>
        );
      case "has_site":
        return (
          <div className="flex flex-col space-y-1">
            <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-slate-800 text-slate-300 border border-slate-700 w-fit">
              <Globe className="w-3 h-3 mr-1 text-slate-400" />
              {lead.link_label || "Есть сайт"}
            </span>
            {lead.external_url && (
              <a
                href={lead.external_url.startsWith("http") ? lead.external_url : `https://${lead.external_url}`}
                target="_blank"
                rel="noreferrer"
                className="text-[11px] text-blue-400 hover:underline truncate max-w-[140px] flex items-center gap-0.5"
              >
                {lead.external_url} <ExternalLink className="w-2.5 h-2.5 flex-shrink-0" />
              </a>
            )}
          </div>
        );
      default:
        return (
          <span className="text-xs text-slate-400">{lead.link_label || "—"}</span>
        );
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl overflow-hidden">
      
      {/* Table Toolbar Header */}
      <div className="p-4 sm:p-5 border-b border-slate-800 flex flex-col md:flex-row items-start md:items-center justify-between gap-3 bg-slate-950/40">
        
        {/* Title and Badge */}
        <div>
          <div className="flex items-center space-x-2.5">
            <h2 className="text-base font-bold text-white tracking-tight">
              Лид-трекер: <span className="text-blue-400">{session?.title || "Текущая сессия"}</span>
            </h2>
            <span className="text-xs px-2.5 py-0.5 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20 font-mono">
              {filteredLeads.length} из {leads.length}
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-0.5">
            Интерактивная таблица для ведения контактов и рассылки предложений
          </p>
        </div>

        {/* Toolbar Controls */}
        <div className="flex flex-wrap items-center gap-2 w-full md:w-auto">
          
          {/* Fast Table Search */}
          <div className="relative flex-1 sm:flex-initial">
            <Search className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Поиск в таблице..."
              className="pl-8 pr-3 py-1.5 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 w-full sm:w-44"
            />
          </div>

          {/* Quick link filter */}
          <select
            value={filterLinkType}
            onChange={(e) => setFilterLinkType(e.target.value)}
            className="px-2.5 py-1.5 bg-slate-950 border border-slate-800 rounded-xl text-xs text-slate-300 focus:outline-none cursor-pointer"
          >
            <option value="all">Все ссылки</option>
            <option value="no_site">🔴 Только БЕЗ сайта</option>
            <option value="whatsapp">🟡 Только WhatsApp</option>
            <option value="multilink">🟣 Taplink / Мульти</option>
            <option value="has_site">🟢 Есть сайт</option>
          </select>

          {/* Column Settings Toggle */}
          <button
            onClick={onOpenColumnSettings}
            className="p-1.5 bg-slate-950 border border-slate-800 hover:border-slate-700 text-slate-300 rounded-xl text-xs flex items-center gap-1 transition-colors"
            title="Управление столбцами"
          >
            <Columns className="w-4 h-4 text-blue-400" />
            <span className="hidden sm:inline">Столбцы</span>
          </button>

          {/* Excel Download Button */}
          <button
            onClick={handleExcelExport}
            className="px-3 py-1.5 bg-emerald-600/20 hover:bg-emerald-600/30 text-emerald-300 border border-emerald-500/30 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition-colors shadow-sm"
          >
            <Download className="w-3.5 h-3.5 text-emerald-400" />
            <span>Скачать Excel (.xlsx)</span>
          </button>

        </div>
      </div>

      {/* Table Container */}
      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs border-collapse">
          <thead>
            <tr className="bg-slate-950/80 border-b border-slate-800 text-slate-400 uppercase tracking-wider text-[11px]">
              {columns.index?.visible && (
                <th className="py-3 px-3 w-12 text-center">№</th>
              )}
              {columns.profile?.visible && (
                <th className="py-3 px-4 min-w-[200px]">Профиль Instagram</th>
              )}
              {columns.followers?.visible && (
                <th className="py-3 px-3 text-center">Подписчики</th>
              )}
              {columns.linkStatus?.visible && (
                <th className="py-3 px-4 min-w-[170px]">Наличие сайта / Статус</th>
              )}
              {columns.contacted?.visible && (
                <th className="py-3 px-4 text-center min-w-[110px]">Писал?</th>
              )}
              {columns.replyStatus?.visible && (
                <th className="py-3 px-4 min-w-[160px]">Статус ответа</th>
              )}
              {columns.notes?.visible && (
                <th className="py-3 px-4 min-w-[180px]">Заметка</th>
              )}
              {columns.actions?.visible && (
                <th className="py-3 px-3 text-center w-28">Действия</th>
              )}
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            {filteredLeads.length === 0 ? (
              <tr>
                <td colSpan={8} className="py-12 text-center text-slate-500">
                  <div className="flex flex-col items-center justify-center space-y-2">
                    <ShieldAlert className="w-8 h-8 text-slate-600" />
                    <p className="text-sm font-medium text-slate-400">Лиды не найдены</p>
                    <p className="text-xs text-slate-500">Попробуйте изменить поисковый запрос или фильтры</p>
                  </div>
                </td>
              </tr>
            ) : (
              filteredLeads.map((lead, idx) => {
                const isTargetNoSite = lead.link_type === "no_site";
                return (
                  <tr
                    key={lead.id}
                    className={`transition-colors hover:bg-slate-800/40 ${
                      lead.contacted
                        ? "bg-slate-900/40"
                        : isTargetNoSite
                        ? "bg-rose-950/10 hover:bg-rose-950/20"
                        : ""
                    }`}
                  >
                    {/* 1. Index */}
                    {columns.index?.visible && (
                      <td className="py-3.5 px-3 text-center font-mono text-slate-500 text-[11px]">
                        {idx + 1}
                      </td>
                    )}

                    {/* 2. Instagram Profile */}
                    {columns.profile?.visible && (
                      <td className="py-3.5 px-4">
                        <div className="flex items-center space-x-3">
                          <img
                            src={lead.avatar_url || `https://api.dicebear.com/7.x/identicon/svg?seed=${lead.username}`}
                            alt={lead.username}
                            className="w-9 h-9 rounded-full bg-slate-800 border border-slate-700 flex-shrink-0"
                            loading="lazy"
                          />
                          <div className="min-w-0">
                            <a
                              href={lead.profile_url}
                              target="_blank"
                              rel="noreferrer"
                              className="font-semibold text-white hover:text-blue-400 transition-colors flex items-center gap-1 group truncate"
                            >
                              <span>@{lead.username}</span>
                              <ExternalLink className="w-3 h-3 text-slate-500 group-hover:text-blue-400" />
                            </a>
                            {lead.full_name && (
                              <p className="text-slate-400 text-[11px] truncate max-w-[200px]">
                                {lead.full_name}
                              </p>
                            )}
                            {lead.biography && (
                              <p className="text-slate-500 text-[10px] truncate max-w-[220px] mt-0.5" title={lead.biography}>
                                {lead.biography.slice(0, 60)}...
                              </p>
                            )}
                          </div>
                        </div>
                      </td>
                    )}

                    {/* 3. Followers */}
                    {columns.followers?.visible && (
                      <td className="py-3.5 px-3 text-center">
                        <span className="px-2 py-0.5 rounded-md bg-slate-950 text-slate-300 font-mono text-[11px] border border-slate-800">
                          {lead.followers_count ? lead.followers_count.toLocaleString() : "—"}
                        </span>
                      </td>
                    )}

                    {/* 4. Link & Website Status */}
                    {columns.linkStatus?.visible && (
                      <td className="py-3.5 px-4">
                        {renderLinkBadge(lead)}
                      </td>
                    )}

                    {/* 5. Contacted Checkbox */}
                    {columns.contacted?.visible && (
                      <td className="py-3.5 px-4 text-center">
                        <button
                          type="button"
                          onClick={() => handleToggleContacted(lead)}
                          className={`inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold transition-all border ${
                            lead.contacted
                              ? "bg-emerald-500/20 text-emerald-300 border-emerald-500/40 shadow-sm shadow-emerald-500/10"
                              : "bg-slate-950 text-slate-400 border-slate-800 hover:border-slate-700 hover:text-slate-200"
                          }`}
                        >
                          {lead.contacted ? (
                            <>
                              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                              <span>ДА</span>
                            </>
                          ) : (
                            <>
                              <Circle className="w-3.5 h-3.5 text-slate-600" />
                              <span>НЕТ</span>
                            </>
                          )}
                        </button>
                      </td>
                    )}

                    {/* 6. Reply Status Selector */}
                    {columns.replyStatus?.visible && (
                      <td className="py-3.5 px-4">
                        <select
                          value={lead.reply_status || "Не отправлено"}
                          onChange={(e) => handleStatusChange(lead.id, e.target.value)}
                          className={`w-full text-xs font-medium px-2.5 py-1.5 rounded-xl border focus:outline-none transition-colors cursor-pointer ${
                            STATUS_OPTIONS.find((s) => s.value === lead.reply_status)?.color || "bg-slate-950 text-slate-300 border-slate-800"
                          }`}
                        >
                          {STATUS_OPTIONS.map((opt) => (
                            <option key={opt.value} value={opt.value} className="bg-slate-900 text-white">
                              {opt.label}
                            </option>
                          ))}
                        </select>
                      </td>
                    )}

                    {/* 7. Notes */}
                    {columns.notes?.visible && (
                      <td className="py-3.5 px-4">
                        <input
                          type="text"
                          defaultValue={lead.notes || ""}
                          placeholder="Добавить заметку..."
                          onBlur={(e) => handleNotesChange(lead.id, e.target.value)}
                          className="w-full px-2.5 py-1.5 bg-slate-950/70 border border-slate-800/80 rounded-lg text-xs text-slate-200 placeholder-slate-600 focus:outline-none focus:border-blue-500"
                        />
                      </td>
                    )}

                    {/* 8. Actions (AI Offer & Delete) */}
                    {columns.actions?.visible && (
                      <td className="py-3.5 px-3 text-center">
                        <div className="flex items-center justify-center space-x-1">
                          
                          {/* AI Offer Generator */}
                          <button
                            type="button"
                            onClick={() => onOpenOfferModal(lead)}
                            title="Сгенерировать AI-оффер через LLM"
                            className="p-1.5 rounded-lg bg-purple-500/10 hover:bg-purple-500/25 text-purple-400 border border-purple-500/20 transition-all hover:scale-105"
                          >
                            <Sparkles className="w-3.5 h-3.5" />
                          </button>

                          {/* Delete Lead */}
                          <button
                            type="button"
                            onClick={() => onDeleteLead(lead.id)}
                            title="Удалить лида из таблицы"
                            className="p-1.5 rounded-lg bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 border border-rose-500/20 transition-all hover:scale-105"
                          >
                            <Trash2 className="w-3.5 h-3.5" />
                          </button>

                        </div>
                      </td>
                    )}

                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>

    </div>
  );
}