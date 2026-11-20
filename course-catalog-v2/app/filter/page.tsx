import { ElectiveFilter } from "@/components/ElectiveFilter";

export default function FilterPage() {
  return (
    <section className="mx-auto max-w-2xl space-y-6">
      <div className="space-y-2">
        <p className="text-xs font-bold uppercase tracking-[0.2em] text-sky-700">
          Browser request
        </p>
        <h1 className="font-serif text-4xl font-black tracking-tight text-emerald-950">
          Course filter
        </h1>
        <p className="leading-7 text-muted-foreground">
          Toggle the elective view to request a filtered catalog directly from the API.
        </p>
      </div>
      <ElectiveFilter />
    </section>
  );
}
