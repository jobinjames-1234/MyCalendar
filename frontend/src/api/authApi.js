import apiClient from "./client";

export const registerUser = (payload) => apiClient.post("/auth/register/", payload);
export const fetchCsrf = () => apiClient.get("/auth/csrf/");
export const loginUser = (payload) => apiClient.post("/auth/login/", payload);
export const logoutUser = () => apiClient.post("/auth/logout/");
export const getCurrentUser = () => apiClient.get("/auth/me/");
export const updateCurrentUser = (payload) => apiClient.put("/auth/me/update/", payload);
export const forgotPasswordRequest = (payload) => apiClient.post("/auth/forgot-password/request/", payload);
export const forgotPasswordConfirm = (payload) => apiClient.post("/auth/forgot-password/confirm/", payload);
export const adminListUsers = (search = "") =>
  apiClient.get(`/auth/admin/users/${search ? `?search=${encodeURIComponent(search)}` : ""}`);
export const adminGetUser = (id) => apiClient.get(`/auth/admin/users/${id}/`);
export const adminUpdateUser = (id, payload) => apiClient.put(`/auth/admin/users/${id}/`, payload);
export const adminToggleUserActive = (id) => apiClient.patch(`/auth/admin/users/${id}/toggle-active/`);
