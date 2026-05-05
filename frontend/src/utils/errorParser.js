/**
 * Parses a Django/DRF error response into a user-friendly string.
 * @param {any} errorResponse - The error.response.data from Axios
 * @returns {string} - A clean error message
 */
export const parseError = (errorResponse) => {
  if (!errorResponse) return "An unexpected error occurred.";

  // If it's a direct detail string
  if (typeof errorResponse === "string") return errorResponse;
  if (errorResponse.detail) return errorResponse.detail;

  // If it's a validation error object (e.g., { "password": ["error message"] })
  if (typeof errorResponse === "object") {
    const firstKey = Object.keys(errorResponse)[0];
    if (firstKey) {
      const error = errorResponse[firstKey];
      if (Array.isArray(error)) return error[0];
      if (typeof error === "string") return error;
      if (typeof error === "object") return parseError(error);
    }
  }

  return "An error occurred. Please try again.";
};
