export default function LoadingCourse() {
  return (
    <section className="mx-auto max-w-3xl animate-pulse overflow-hidden rounded-[2rem] border border-emerald-950/10 bg-card" role="status">
      <div className="h-44 bg-emerald-950/90" />
      <div className="space-y-4 p-8">
        <p className="h-5 w-2/3 rounded-full bg-emerald-950/10" />
        <p className="h-5 w-full rounded-full bg-emerald-950/10" />
        <p className="h-5 w-4/5 rounded-full bg-emerald-950/10" />
      </div>
      <span className="sr-only">Loading course…</span>
    </section>
  );
}
