// src/views/ColorPickerView.tsx
import ColorPicker from "../components/ColorPicker";

export default function ColorPickerView() {
  return (
    <div className="space-y-8">
      <section className="bg-slate-50 dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800">
        <div className="container mx-auto px-4 py-6">
          <h1 className="text-2xl font-bold mb-4">Vista: Selector de Colores</h1>
          <ColorPicker />
        </div>
      </section>
    </div>
  );
}
