// src/views/SearchListView.tsx
import SearchList from "../components/SearchList";

export default function SearchListView() {
  return (
    <div className="space-y-8">
      <section className="bg-slate-50 dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800">
        <div className="container mx-auto px-4 py-6">
          <h1 className="text-2xl font-bold mb-4">Vista: Buscador en Lista</h1>
          <SearchList />
        </div>
      </section>
    </div>
  );
}
