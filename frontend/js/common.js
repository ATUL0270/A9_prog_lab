// Shared helpers used by both pages.

async function apiGet(path) {
  const res = await fetch(path);
  let body = null;
  try { body = await res.json(); } catch (_) { /* non-JSON response */ }
  if (!res.ok) {
    const msg = (body && body.error) || `Request failed (${res.status})`;
    const err = new Error(msg);
    err.status = res.status;
    throw err;
  }
  return body;
}

function formatPrice(value) {
  return new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR" }).format(value);
}

// Escape text before inserting into HTML (prevents XSS).
function esc(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

function setStatus(message, isError = false) {
  const el = document.getElementById("status");
  el.textContent = message;
  el.classList.toggle("error", isError);
}
