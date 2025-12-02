import { useState } from "react";
import lordsImg from "./assets/lords.jpg";
import { predictFirstInnings, predictSecondInnings } from "./api/predict";

export default function App() {
  const [inningsType, setInningsType] = useState("first");

  const [score1, setScore1] = useState("");
  const [score2, setScore2] = useState("");

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setResult(null);

    try {
      let data;

      if (inningsType === "first") {
        data = await predictFirstInnings(score1);
      } else {
        data = await predictSecondInnings(score1, score2);
      }

      setResult(data);
    } catch (err) {
      console.error(err);
    }

    setLoading(false);
  }

  return (
    <div className="min-h-screen bg-zinc-950 text-white flex flex-col items-center">

      <img 
        src={lordsImg} 
        alt="Lords Cricket Ground"
        className="w-full max-h-72 object-cover shadow-lg"
      />

      <h1 className="text-4xl font-bold mt-8 mb-6 tracking-wide">
        Lord’s Win Probability
      </h1>

      {/* FORM */}
      <form 
        onSubmit={handleSubmit}
        className="bg-zinc-900 p-6 rounded-xl w-full max-w-md shadow-xl space-y-4"
      >

        {/* INNINGS SWITCH */}
        <div className="flex justify-center space-x-6 mb-4">
          <label>
            <input 
              type="radio" 
              value="first"
              checked={inningsType === "first"}
              onChange={() => setInningsType("first")}
            />
            <span className="ml-2">1st Innings</span>
          </label>

          <label>
            <input 
              type="radio" 
              value="second"
              checked={inningsType === "second"}
              onChange={() => setInningsType("second")}
            />
            <span className="ml-2">2nd Innings</span>
          </label>
        </div>

        {/* FIRST INNINGS INPUT */}
        <label className="block text-sm text-zinc-400 mb-1">
          First Innings Score
        </label>
        <input
          type="number"
          value={score1}
          onChange={(e) => setScore1(e.target.value)}
          placeholder="e.g., 320"
          className="w-full p-2 rounded bg-zinc-800 outline-none"
        />

        {/* SECOND INNINGS INPUT IF NEEDED */}
        {inningsType === "second" && (
          <>
            <label className="block text-sm text-zinc-400 mb-1">
              Second Innings Score
            </label>
            <input
              type="number"
              value={score2}
              onChange={(e) => setScore2(e.target.value)}
              placeholder="e.g., 280"
              className="w-full p-2 rounded bg-zinc-800 outline-none"
            />
          </>
        )}

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

          {/* TEAM A */}
          <h3 className="text-lg font-bold text-green-400 mb-2">Team A (Batting First)</h3>
          
          <p>Win:  <span className="font-bold text-green-400">{result.team_a.win.toFixed(2)}%</span></p>
          <p>Draw: <span className="font-bold text-blue-400">{result.team_a.draw.toFixed(2)}%</span></p>
          <p>Loss: <span className="font-bold text-red-400">{result.team_a.loss.toFixed(2)}%</span></p>

          {/* TEAM B */}
          <h3 className="text-lg font-bold text-red-400 mt-4 mb-2">Team B (Opponent)</h3>
          
          <p>Win:  <span className="font-bold text-green-400">{result.team_b.win.toFixed(2)}%</span></p>
          <p>Draw: <span className="font-bold text-blue-400">{result.team_b.draw.toFixed(2)}%</span></p>
          <p>Loss: <span className="font-bold text-red-400">{result.team_b.loss.toFixed(2)}%</span></p>

        </div>
      )}

    </div>
  );
}
