// Base API URL loaded from environment variables.
// In development → http://127.0.0.1:8000
// In production → your Railway backend URL
const API_BASE = import.meta.env.VITE_API_URL;

export async function predictFirstInnings(score) {
  const res = await fetch(`${API_BASE}/predict`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ score: Number(score) })
  });

  if (!res.ok) throw new Error("Failed first-innings prediction");

  return res.json();
}

export async function predictSecondInnings(score1, score2) {
  const res = await fetch(`${API_BASE}/predict/second`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      score_1: Number(score1),
      score_2: Number(score2)
    })
  });

  if (!res.ok) throw new Error("Failed second-innings prediction");

  return res.json();
}
