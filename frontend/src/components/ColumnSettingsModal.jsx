import React from "react";
import { X, Columns, CheckSquare, Square, RotateCcw } from "lucide-react";

export const DEFAULT_COLUMNS = {
  index: { id: "index", label: "№", visible: true },
  profile: { id: "profile", label: "Профиль Instagram", visible: true },
  followers: { id: "followers", label: "Подписчики", visible: true },
  linkStatus: { id: "linkStatus", label: "Наличие сайта / Ссылки", visible: true },
  contacted: { id: "contacted", label: "Писал? (Чекбокс)", visible: true },
  replyStatus: { id: "replyStatus", label: "Статус ответа", visible: true },
  notes: { id: "notes", label: "Заметки", visible: true },
  actions: { id: "actions", label: "Действия (Оффер / Удалить)", visible: true }
};

export default function ColumnSettingsModal({ isOpen, onClose, columns, setColumns }) {
  if (!isOpen) return null;

  const toggleColumn = (key) => {
    setColumns((prev) => ({
      ...prev,
      [key]: {
        ...prev[key],
        visible: !prev[key].visible
      }
    }));
  };

  const handleReset = () => {
    setColumns(DEFAULT_COLUMNS);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 backdrop-blur-sm p-4">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-md shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-200">
        
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-slate-800">
          <div className="flex items-center space-x-2">
            <Columns className="w-4 h-4 text-blue-400" />
            <h3 className="text-sm font-semibold text-white">Управление столбцами таблицы</h3>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Content */}
        <div className="p-5 space-y-3">
          <p className="text-xs text-slate-400">
            Включайте и отключайте видимость столбцов в лид-трекере. Настройки сохраняются мгновенно.
          </p>

          <div className="space-y-1.5 pt-1">
            {Object.entries(columns).map(([key, col]) => (
              <div
                key={key}
                onClick={() => toggleColumn(key)}
                className="flex items-center justify-between p-2.5 rounded-xl bg-slate-950/60 border border-slate-800/80 hover:border-slate-700 cursor-pointer select-none transition-colors"
              >
                <span className="text-xs font-medium text-slate-200">{col.label}</span>
                <div className="text-blue-400">
                  {col.visible ? (
                    <CheckSquare className="w-4 h-4 text-blue-400" />
                  ) : (
                    <Square className="w-4 h-4 text-slate-600" />
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between p-4 bg-slate-950/50 border-t border-slate-800">
          <button
            onClick={handleReset}
            className="flex items-center space-x-1 px-3 py-1.5 text-xs text-slate-400 hover:text-white hover:bg-slate-800 rounded-lg transition-colors"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>Сбросить</span>
          </button>

          <button
            onClick={onClose}
            className="px-4 py-2 text-xs font-semibold text-white bg-blue-600 hover:bg-blue-500 rounded-xl shadow-md shadow-blue-600/20 transition-all"
          >
            Готово
          </button>
        </div>

      </div>
    </div>
  );
}