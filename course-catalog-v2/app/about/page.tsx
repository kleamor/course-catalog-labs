export default function AboutPage() {
  return (
    <section className="mx-auto max-w-3xl space-y-6 py-4">
      <p className="text-xs font-bold uppercase tracking-[0.2em] text-sky-700">
        About Northstar
      </p>
      <h1 className="font-serif text-4xl font-black tracking-tight text-emerald-950 sm:text-5xl">
        A small catalog with a clear point of view.
      </h1>
      <p className="border-l-4 border-sky-400 pl-5 text-lg leading-8 text-muted-foreground">
        This catalog presents the Advanced Web Technologies program through an
        editorial interface. It was built with Next.js, React, TypeScript,
        Tailwind CSS, and shadcn/ui for the course labs.
      </p>
    </section>
  );
}
