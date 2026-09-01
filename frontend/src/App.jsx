import React, { useState, useEffect } from "react";
import Navbar from "./components/Navbar";
import SettingsModal from "./components/SettingsModal";
import MainPage from "./pages/MainPage";
import ArchivePage from "./pages/ArchivePage";
import { api } from "./services/api";

export default function App() {
  const [activeTab, setActiveTab] = useState("main");
  const [apifyToken, setApifyToken] = useState(() => localStorage.getItem("apify_token") || "");
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);

  // Search & Session State
  const [query, setQuery] = useState("");
  const [limit, setLimit] = useState(20);
  const [filterType, setFilterType] = useState("all");
  const [isLoading, setIsLoading] = useState(false);

  const [currentSession, setCurrentSession] = useState(null);
  const [leads, setLeads] = useState([]);
  const [sessionsCount, setSessionsCount] = useState(0);

  // Load existing sessions count
  const refreshSessionsCount = async () => {
    try {
      const data = await api.getSessions();
      setSessionsCount(data.length);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    refreshSessionsCount();
  }, []);

  const handleSaveToken = (token) => {
    setApifyToken(token);
    if (token) {
      localStorage.setItem("apify_token", token);
    } else {
      localStorage.removeItem("apify_token");
    }
  };

  // Start Parsing Action
  const handleStartParse = async () => {
    if (!query.trim()) return;
    setIsLoading(true);
    try {
      const data = await api.startParsing({
        query: query.trim(),
        limit,
        filter_type: filterType,
        apify_token: apifyToken,
        is_mock: !apifyToken
      });

      setCurrentSession(data);
      setLeads(data.leads || []);
      refreshSessionsCount();
    } catch (error) {
      console.error(error);
      alert(error.response?.data?.detail || "Произошла ошибка при парсинге данных через Apify.");
    } finally {
      setIsLoading(false);
    }
  };

  // Update single lead (contacted status, note, etc.)
  const handleUpdateLead = async (leadId, updates) => {
    // Optimistic UI update
    setLeads((prev) =>
      prev.map((lead) => (lead.id === leadId ? { ...lead, ...updates } : lead))
    );
    try {
      await api.updateLead(leadId, updates);
      refreshSessionsCount();
    } catch (e) {
      console.error("Failed to update lead", e);
    }
  };

  // Delete lead row
  const handleDeleteLead = async (leadId) => {
    setLeads((prev) => prev.filter((lead) => lead.id !== leadId));
    try {
      await api.deleteLead(leadId);
      refreshSessionsCount();
    } catch (e) {
      console.error("Failed to delete lead", e);
    }
  };

  // Select session from Archive Page to view in Main Page
  const handleSelectSession = async (sessionId) => {
    try {
      const data = await api.getSessionDetail(sessionId);
      setCurrentSession(data);
      setLeads(data.leads || []);
      setActiveTab("main");
    } catch (e) {
      console.error("Failed to fetch session detail", e);
      alert("Не удалось загрузить сессию");
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col selection:bg-blue-500 selection:text-white">
      {/* Top Navigation */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        onOpenSettings={() => setIsSettingsOpen(true)}
        apifyToken={apifyToken}
        sessionsCount={sessionsCount}
      />

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {activeTab === "main" ? (
          <MainPage
            currentSession={currentSession}
            leads={leads}
            onStartParse={handleStartParse}
            isLoading={isLoading}
            onUpdateLead={handleUpdateLead}
            onDeleteLead={handleDeleteLead}
            apifyToken={apifyToken}
            query={query}
            setQuery={setQuery}
            limit={limit}
            setLimit={setLimit}
            filterType={filterType}
            setFilterType={setFilterType}
          />
        ) : (
          <ArchivePage
            onSelectSession={handleSelectSession}
          />
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-900 bg-slate-950/80 py-4 text-center text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
          <span>LeadHunter • Apify Scraper & Lead Tracker CRM</span>
          <span>Разработано для поиска клиентов без веб-сайтов</span>
        </div>
      </footer>

      {/* Settings Modal */}
      <SettingsModal
        isOpen={isSettingsOpen}
        onClose={() => setIsSettingsOpen(false)}
        apifyToken={apifyToken}
        onSaveToken={handleSaveToken}
      />
    </div>
  );
}