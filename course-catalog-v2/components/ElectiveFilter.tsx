"use client";

import { useState } from "react";
import useSWR from "swr";

import type { Course } from "@/lib/courses";

const API = process.env.NEXT_PUBLIC_API_URL;

async function fetcher(url: string): Promise<Course[]> {
  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return response.json();
}

export function ElectiveFilter() {
  const [onlyElective, setOnlyElective] = useState(false);
  const query = onlyElective ? "?is_elective=true" : "";
  const { data, error, isLoading } = useSWR(`${API}/courses${query}`, fetcher);

  return (
    <section className="space-y-5 rounded-[1.5rem] border border-emerald-950/10 bg-card/90 p-6 shadow-sm">
      <label className="flex cursor-pointer items-center gap-3 font-semibold text-emerald-950">
        <input
          type="checkbox"
          checked={onlyElective}
          onChange={(event) => setOnlyElective(event.target.checked)}
          className="size-4 accent-sky-600"
        />
        Electives only
      </label>

      {error && (
        <p className="font-medium text-red-700" role="alert">
          Failed to load courses.
        </p>
      )}
      {isLoading && <p className="text-muted-foreground">Loading courses…</p>}
      {data && (
        <ul className="space-y-3">
          {data.map((course) => (
            <li
              key={course.id}
              className="border-b border-emerald-950/10 pb-3 last:border-0 last:pb-0"
            >
              <span className="font-bold text-emerald-950">{course.title}</span>
              <span className="text-muted-foreground"> — {course.credits} cr.</span>
              {course.isElective && (
                <span className="font-semibold text-sky-700"> · elective</span>
              )}
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
