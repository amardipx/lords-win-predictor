export async function predictScore(score) {
  const res = await fetch("https://lords-backend-production.up.railway.app/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ score: Number(score) })
  });

  if (!res.ok) {
    throw new Error("Failed to fetch prediction");
  }

  return res.json();
}
