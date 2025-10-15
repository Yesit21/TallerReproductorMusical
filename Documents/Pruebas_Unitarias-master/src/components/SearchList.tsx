// src/components/SearchList.tsx
import { useState } from "react";

const initialNames = ["Ana", "Carlos", "Beatriz", "Daniel", "Elena", "Fernando", "Gabriela"];

export default function SearchList() {
  const [query, setQuery] = useState("");

  const filteredNames = initialNames.filter((name) =>
    name.toLowerCase().includes(query.toLowerCase())
  );

  return (
    <div className="p-4 border rounded-lg shadow-md bg-white dark:bg-slate-800">
      <h2 className="text-lg font-bold mb-2">Buscador en Lista</h2>
      <input
        type="text"
        placeholder="Buscar..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="border p-2 rounded w-full"
      />

      <ul className="mt-4 space-y-1">
        {filteredNames.length > 0 ? (
          filteredNames.map((name, index) => (
            <li key={index} className="p-1 border-b">
              {name}
            </li>
          ))
        ) : (
          <li className="text-red-500">No encontrado</li>
        )}
      </ul>
    </div>
  );
}
