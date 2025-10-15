// src/components/ColorPicker.tsx
import { useState, useEffect } from "react";

export default function ColorPicker() {
  const [color, setColor] = useState<string>(() => {
    return localStorage.getItem("selectedColor") || "#ffffff";
  });

  useEffect(() => {
    localStorage.setItem("selectedColor", color);
  }, [color]);

  return (
    <div className="p-4 border rounded-lg shadow-md bg-white dark:bg-slate-800">
      <h2 className="text-lg font-bold mb-2">Selector de Colores</h2>
      <label htmlFor="color-input" className="block mb-2">Color</label>
      <input
        id="color-input"
        type="color"
        value={color}
        onChange={(e) => setColor(e.target.value)}
        className="w-16 h-10 border cursor-pointer"
      />
      <div
        data-testid="color-box"
        className="mt-4 w-32 h-32 border rounded-lg shadow"
        style={{ backgroundColor: color }}
      ></div>
    </div>
  );
}
