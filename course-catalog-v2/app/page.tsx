import Link from "next/link";

export default function HomePage() {
  return (
    <section className="grid min-h-[calc(100vh-13rem)] items-center gap-10 py-8 lg:grid-cols-[1.3fr_0.7fr] lg:py-16">
      <div className="space-y-7">
        <p className="inline-flex rounded-full border border-sky-500/30 bg-sky-100 px-4 py-1.5 text-xs font-bold uppercase tracking-[0.18em] text-sky-800">
          Advanced Web Technologies · 2026
        </p>
        <h1 className="max-w-3xl font-serif text-5xl font-black leading-[0.94] tracking-tight text-emerald-950 sm:text-7xl">
          Find your next
          <span className="block text-teal-600">bright idea.</span>
        </h1>
        <p className="max-w-xl text-lg leading-8 text-muted-foreground sm:text-xl">
          A focused collection of six practical courses for people building the
          modern web.
        </p>
        <Link
          className="inline-flex rounded-full bg-emerald-700 px-6 py-3.5 font-semibold text-white shadow-lg shadow-emerald-900/20 transition hover:-translate-y-0.5 hover:bg-emerald-600"
          href="/courses"
        >
          Explore the catalog →
        </Link>
      </div>
      <aside className="rounded-[2rem] border border-emerald-950/10 bg-emerald-950 p-7 text-sky-50 shadow-2xl shadow-emerald-950/20 sm:p-9">
        <p className="text-xs font-bold uppercase tracking-[0.2em] text-sky-300">
          Learning index
        </p>
        <p className="mt-8 font-serif text-6xl font-black">06</p>
        <p className="mt-2 text-emerald-100">courses in the current catalog</p>
        <p className="mt-10 border-t border-emerald-400/30 pt-5 text-sm leading-6 text-emerald-100">
          Frontend, backend, data, security, API design, and AI integration —
          mapped for a hands-on semester.
        </p>
      </aside>
    </section>
  );
}
