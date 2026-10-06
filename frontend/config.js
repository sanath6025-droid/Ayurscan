/**
 * AyurScan - Central Frontend Deployment Configuration
 * 
 * HOW TO CONNECT TO A DEPLOYED BACKEND:
 * 1. If your backend is deployed on Render (e.g., https://ayurscan-api.onrender.com)
 *    and frontend is hosted separately (Vercel, Netlify, GitHub Pages, Render Static):
 *    Set AYURSCAN_BACKEND_URL below to your Render URL.
 * 
 * 2. If your backend and frontend are deployed together as a full-stack Web Service:
 *    Leave AYURSCAN_BACKEND_URL as "" (empty string). All requests will use clean relative paths.
 * 
 * 3. During local development or local Wi-Fi:
 *    Leave AYURSCAN_BACKEND_URL as "" (empty string). It automatically connects to port 8000.
 */
window.AYURSCAN_BACKEND_URL = "https://ayurscan-vd1q.onrender.com";

/**
 * Returns the active API base URL without trailing slash.
 */
window.getAyurScanApiBase = function () {
  if (window.AYURSCAN_BACKEND_URL && window.AYURSCAN_BACKEND_URL.trim() !== "") {
    return window.AYURSCAN_BACKEND_URL.trim().replace(/\/+$/, "");
  }

  // Local development fallback for file:// or alternative dev ports (e.g., Live Server 5500)
  if (window.location.protocol === "file:" || (window.location.port && window.location.port !== "8000")) {
    const host = window.location.hostname || "127.0.0.1";
    return `http://${host}:8000`;
  }

  // Relative path for same-origin production or standard dev
  return "";
};
