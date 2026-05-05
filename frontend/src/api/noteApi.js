import apiClient from "./client";

export const fetchMonthNotes = (year, month) => apiClient.get(`/notes/?year=${year}&month=${month}`);
export const fetchNoteByDate = (date) => apiClient.get(`/notes/by-date/?date=${date}`);
export const saveNote = (payload) => apiClient.post("/notes/", payload);
export const updateNote = (id, payload) => apiClient.put(`/notes/${id}/`, payload);
export const deleteNote = (id) => apiClient.delete(`/notes/${id}/`);
