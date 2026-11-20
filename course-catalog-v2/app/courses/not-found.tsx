import Link from "next/link";

export default function CourseNotFound() {
  return (
    <section className="mx-auto max-w-xl space-y-5 py-16 text-center">
      <p className="font-serif text-7xl font-black text-sky-500">404</p>
      <h1 className="font-serif text-3xl font-black tracking-tight text-emerald-950">Course not found</h1>
      <p className="text-muted-foreground">
        The course you requested does not exist.
      </p>
      <Link
        className="inline-block rounded-full bg-emerald-700 px-5 py-3 font-semibold text-white transition hover:bg-emerald-600"
        href="/courses"
      >
        Back to courses
      </Link>
    </section>
  );
}
