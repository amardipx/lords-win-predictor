import { useState } from "react";
import InputForm from "../components/InputForm";
import ResultCard from "../components/ResultCard";

export default function Home() {
  const [result, setResult] = useState(null);

  return (
    <div className="min-h-screen bg-zinc-950 text-white flex flex-col items-center p-10">
      <h1 className="text-4xl font-bold mb-10 tracking-wide">
        Lords Win Probability
      </h1>

      <InputForm onResult={setResult} />

      {result && <ResultCard data={result} />}
    </div>
  );
}
