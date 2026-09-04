import axios from "axios";

const API_BASE = "/api";

export const api = {
  // Start parsing
  startParsing: async ({ query, limit = 20, search_type = "user", filter_type = "all", apify_token = "", is_mock = false }) => {
    const res = await axios.post(`${API_BASE}/parse`, {
      query,
      limit: Number(limit),
      search_type,
      filter_type,
      apify_token: apify_token || undefined,
      is_mock
    });
    return res.data;
  },

  // Get all saved sessions
  getSessions: async () => {
    const res = await axios.get(`${API_BASE}/sessions`);
    return res.data;
  },

  // Get single session with leads
  getSessionDetail: async (sessionId) => {
    const res = await axios.get(`${API_BASE}/sessions/${sessionId}`);
    return res.data;
  },

  // Delete session
  deleteSession: async (sessionId) => {
    const res = await axios.delete(`${API_BASE}/sessions/${sessionId}`);
    return res.data;
  },

  // Update lead
  updateLead: async (leadId, updates) => {
    const res = await axios.patch(`${API_BASE}/leads/${leadId}`, updates);
    return res.data;
  },

  // Delete lead
  deleteLead: async (leadId) => {
    const res = await axios.delete(`${API_BASE}/leads/${leadId}`);
    return res.data;
  },

  // Export Excel URL
  getExportUrl: (sessionId) => {
    return `${API_BASE}/sessions/${sessionId}/export`;
  },

  // Generate AI Offer (Template or ChatGPT B2B)
  generateOffer: async ({
    username,
    full_name,
    niche,
    link_type,
    link_label,
    biography,
    followers_count,
    tone = "friendly",
    mode = "template",
    openai_api_key
  }) => {
    const res = await axios.post(`${API_BASE}/generate-offer`, {
      username,
      full_name,
      niche,
      link_type,
      link_label,
      biography,
      followers_count,
      tone,
      mode,
      openai_api_key: openai_api_key || undefined
    });
    return res.data;
  }
};