// src/components/DigitalClock.tsx
import { useEffect, useState } from "react";

export default function DigitalClock() {
  const [time, setTime] = useState<string>(() => {
    const now = new Date();
    return now.toLocaleTimeString("es-CO", { hour12: false });
  });

  useEffect(() => {
    const interval = setInterval(() => {
      const now = new Date();
      setTime(now.toLocaleTimeString("es-CO", { hour12: false }));
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="p-6 text-center">
      <h1 className="text-2xl font-bold mb-4">Reloj Digital</h1>
      <div className="bg-gray-900 text-green-400 font-mono text-4xl p-4 rounded-lg shadow-lg">
        {time}
      </div>
    </div>
  );
}
