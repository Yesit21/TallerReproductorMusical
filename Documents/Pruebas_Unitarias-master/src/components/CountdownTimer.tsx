import { useState, useRef, useEffect } from "react";

export default function CountdownTimer() {
  const [seconds, setSeconds] = useState<number>(0);
  const [timeLeft, setTimeLeft] = useState<number | null>(null);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  const handleStart = () => {
    if (seconds > 0) {
      setTimeLeft(seconds);
    }
  };

  useEffect(() => {
    if (timeLeft === null) return;

    if (timeLeft <= 0) {
      if (intervalRef.current) clearInterval(intervalRef.current);
      return;
    }

    intervalRef.current = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev !== null) {
          return prev > 0 ? prev - 1 : 0;
        }
        return 0;
      });
    }, 1000);

    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, [timeLeft]);

  return (
    <div className="p-4 border rounded-lg shadow-md bg-white dark:bg-slate-800">
      <h2 className="text-lg font-bold mb-2">Contador Regresivo</h2>
      <input
        type="number"
        value={seconds}
        onChange={(e) => setSeconds(Number(e.target.value))}
        className="border p-2 mr-2 rounded"
        placeholder="Segundos"
      />
      <button
        onClick={handleStart}
        className="bg-emerald-600 text-white px-4 py-2 rounded hover:bg-emerald-700"
      >
        Iniciar
      </button>

      <div className="mt-4 text-xl font-mono">
        {timeLeft !== null ? timeLeft : "Listo"}
      </div>
    </div>
  );
}
