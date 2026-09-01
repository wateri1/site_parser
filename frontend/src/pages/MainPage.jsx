import React, { useState } from "react";
import SearchControl from "../components/SearchControl";
import StatsCards from "../components/StatsCards";
import LeadTrackerTable from "../components/LeadTrackerTable";
import ColumnSettingsModal, { DEFAULT_COLUMNS } from "../components/ColumnSettingsModal";
import LLMOfferModal from "../components/LLMOfferModal";
import { Sparkles, Layers, ShieldCheck } from "lucide-react";
import confetti from "canvas-confetti";

export default function MainPage({
  currentSession,
  leads,
  onStartParse,
  isLoading,
  onUpdateLead,
  onDeleteLead,
  apifyToken,
  query,
  setQuery,
  limit,
  setLimit,
  searchType,
  setSearchType,
  filterType,
  setFilterType
}) {
  const [columns, setColumns] = useState(DEFAULT_COLUMNS);
  const [isColumnModalOpen, setIsColumnModalOpen] = useState(false);
  const [selectedLeadForOffer, setSelectedLeadForOffer] = useState(null);

  const handleMarkContactedFromOffer = (leadId) => {
    onUpdateLead(leadId, { contacted: true, reply_status: "Ожидает ответа" });
    try {
      confetti({
        particleCount: 50,
        spread: 60,
        origin: { y: 0.8 }
      });
    } catch (e) {}
  };

  return (
    <div className="space-y-6">
      
      {/* Hero Welcome banner if no session active */}
      {!currentSession && leads.length === 0 && (
        <div className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-blue-900/40 via-indigo-900/20 to-purple-900/30 border border-blue-500/20 p-6 sm:p-8 text-left shadow-2xl">
          <div className="max-w-3xl space-y-3 relative z-10">
            <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-semibold">
              <Sparkles className="w-3.5 h-3.5 text-amber-300" />
              <span>Поиск клиентов под веб-разработку и лендинги</span>
            </div>
            <h1 className="text-2xl sm:text-4xl font-extrabold text-white tracking-tight leading-tight">
              Находите клиентов <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-indigo-300 to-purple-400">без сайтов</span> за секунды
            </h1>
            <p className="text-sm sm:text-base text-slate-300 leading-relaxed">
              Введите ключевое слово ниши и города. Парсер проверит профили в Instagram, определит у кого нет сайта (или есть только WhatsApp / Taplink), сформирует персональную CRM-таблицу и поможет составить продающий оффер.
            </p>
          </div>
          <div className="absolute right-0 top-0 bottom-0 w-1/3 bg-radial from-blue-500/10 to-transparent pointer-events-none" />
        </div>
      )}

      {/* 1. Search Control Box */}
      <SearchControl
        query={query}
        setQuery={setQuery}
        limit={limit}
        setLimit={setLimit}
        searchType={searchType}
        setSearchType={setSearchType}
        filterType={filterType}
        setFilterType={setFilterType}
        onStartParse={onStartParse}
        isLoading={isLoading}
        apifyToken={apifyToken}
      />

      {/* 2. Stats Summary Cards (only when leads exist) */}
      {leads.length > 0 && (
        <StatsCards leads={leads} />
      )}

      {/* 3. Interactive Lead Tracker Table */}
      {leads.length > 0 && (
        <LeadTrackerTable
          session={currentSession}
          leads={leads}
          onUpdateLead={onUpdateLead}
          onDeleteLead={onDeleteLead}
          columns={columns}
          onOpenColumnSettings={() => setIsColumnModalOpen(true)}
          onOpenOfferModal={(lead) => setSelectedLeadForOffer(lead)}
        />
      )}

      {/* Column Visibility Settings Modal */}
      <ColumnSettingsModal
        isOpen={isColumnModalOpen}
        onClose={() => setIsColumnModalOpen(false)}
        columns={columns}
        setColumns={setColumns}
      />

      {/* LLM Offer Generator Modal */}
      <LLMOfferModal
        isOpen={!!selectedLeadForOffer}
        onClose={() => setSelectedLeadForOffer(null)}
        lead={selectedLeadForOffer}
        onMarkContacted={handleMarkContactedFromOffer}
      />

    </div>
  );
}