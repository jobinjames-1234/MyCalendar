import axios from "axios";

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  withCredentials: true,
  headers: { "Content-Type": "application/json" },
  xsrfCookieName: "csrftoken",
  xsrfHeaderName: "X-CSRFToken",
});

// Function to get cookie value
const getCookie = (name) => {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
  return null;
};

// Automatic CSRF pre-fetching and header injection
apiClient.interceptors.request.use(async (config) => {
  let csrfToken = getCookie("csrftoken");

  // If missing and not already trying to get one, fetch it
  if (!csrfToken && !config.url.includes("/auth/csrf/")) {
    try {
      await axios.get(`${import.meta.env.VITE_API_BASE_URL}/auth/csrf/`, { withCredentials: true });
      csrfToken = getCookie("csrftoken");
    } catch (error) {
      console.error("Failed to pre-fetch CSRF token:", error);
    }
  }

  // Manually attach the token to the headers if we have it
  if (csrfToken) {
    config.headers["X-CSRFToken"] = csrfToken;
  }

  return config;
});

export default apiClient;
