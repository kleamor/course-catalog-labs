"use client";

import { useEffect } from "react";

export default function CoursesError({
  error,
  retry,
}: {
  error: Error & { digest?: string };
  retry: () => void;
}) {
  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <section className="mx-auto max-w-xl space-y-5 py-16 text-center">
      <p className="font-serif text-6xl font-black text-sky-500">!</p>
      <h1 className="font-serif text-3xl font-black tracking-tight text-emerald-950">
        Could not load courses
      </h1>
      <p className="text-muted-foreground">
        The backend may not be running. Start it and try the request again.
      </p>
      <button
        type="button"
        onClick={retry}
        className="rounded-full bg-emerald-700 px-5 py-3 font-semibold text-white transition hover:bg-emerald-600"
      >
        Try again
      </button>
    </section>
  );
}
