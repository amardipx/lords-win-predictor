import { useState } from "react";
import lordsImg from "./assets/lords.jpg";
import { predictScore } from "./api/predict";

export default function App() {
  const [score, setScore] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setResult(null);

    try {
      const data = await predictScore(score);
      setResult(data);
    } catch (err) {
      console.error(err);
    }

    setLoading(false);
  }

  return (
    <div className="min-h-screen bg-zinc-950 text-white flex flex-col items-center">

      {/* TOP IMAGE */}
      <img 
        src={lordsImg} 
        alt="Lords Cricket Ground"
        className="w-full max-h-72 object-cover shadow-lg"
      />

      {/* TITLE */}
      <h1 className="text-4xl font-bold mt-8 mb-6 tracking-wide">
        Lord’s Win Probability
      </h1>

      {/* FORM */}
      <form 
        onSubmit={handleSubmit}
        className="bg-zinc-900 p-6 rounded-xl w-full max-w-md shadow-xl space-y-4"
      >
        <label className="block text-sm text-zinc-400 mb-1">
          First Innings Score
        </label>

        <input
          type="number"
          value={score}
          onChange={(e) => setScore(e.target.value)}
          placeholder="e.g., 320"
          className="w-full p-2 rounded bg-zinc-800 outline-none"
        />

        <button
          type="submit"
          className="w-full bg-green-600 py-2 rounded-lg font-semibold hover:bg-green-700 transition disabled:opacity-50"
          disabled={loading}
        >
          {loading ? "Predicting..." : "Get Prediction"}
        </button>
      </form>

      {/* RESULT */}
      {result && (
        <div className="mt-10 bg-zinc-900 p-8 rounded-2xl w-full max-w-md text-center border border-zinc-800 space-y-2">
          <h2 className="text-2xl font-semibold mb-3">Probabilities</h2>

          <p className="text-lg">
            Win: <span className="text-green-400 font-bold">
              {result.win_probability.toFixed(2)}%
            </span>
          </p>

          <p className="text-lg">
            Draw: <span className="text-blue-400 font-bold">
              {result.draw_probability.toFixed(2)}%
            </span>
          </p>

          <p className="text-lg">
            Loss: <span className="text-red-400 font-bold">
              {result.loss_probability.toFixed(2)}%
            </span>
          </p>
        </div>
      )}

    </div>
  );
}
