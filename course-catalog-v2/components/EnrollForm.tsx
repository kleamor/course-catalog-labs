"use client";

import { useState, type FormEvent } from "react";

import type { Enrollment } from "@/lib/courses";
import { Button } from "@/components/ui/button";

const API = process.env.NEXT_PUBLIC_API_URL;

type EnrollFormProps = {
  courseId: string;
};

type Status = "idle" | "sending" | "done" | "rejected" | "error";

type ValidationError = {
  detail?: Array<{ msg?: string }>;
};

export function EnrollForm({ courseId }: EnrollFormProps) {
  const [studentName, setStudentName] = useState("");
  const [status, setStatus] = useState<Status>("idle");
  const [message, setMessage] = useState("");

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setStatus("sending");
    setMessage("");

    try {
      const response = await fetch(`${API}/enrollments`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ courseId, studentName }),
      });

      if (response.status === 422) {
        const body: ValidationError = await response.json();
        setMessage(body.detail?.[0]?.msg ?? "The submitted data is invalid.");
        setStatus("rejected");
        return;
      }

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const enrollment: Enrollment = await response.json();
      setMessage(`Enrollment number: ${enrollment.id}`);
      setStatus("done");
    } catch {
      setStatus("error");
    }
  }

  return (
    <form onSubmit={handleSubmit} className="flex max-w-sm flex-col gap-3">
      <label htmlFor="studentName" className="font-semibold text-emerald-950">
        Your name
      </label>
      <input
        id="studentName"
        value={studentName}
        onChange={(event) => setStudentName(event.target.value)}
        className="rounded-xl border border-emerald-950/20 bg-white px-3 py-2 text-emerald-950 outline-none transition focus:border-sky-500 focus:ring-2 focus:ring-sky-200"
      />
      <Button
        type="submit"
        disabled={status === "sending"}
        className="w-fit rounded-full bg-emerald-700 px-5 hover:bg-emerald-600"
      >
        {status === "sending" ? "Sending…" : "Enroll"}
      </Button>
      {status === "done" && (
        <p className="font-medium text-emerald-700" role="status">
          You are enrolled. {message}
        </p>
      )}
      {status === "rejected" && (
        <p className="font-medium text-red-700" role="alert">
          The server rejected the data: {message}
        </p>
      )}
      {status === "error" && (
        <p className="font-medium text-red-700" role="alert">
          Could not submit the enrollment.
        </p>
      )}
    </form>
  );
}
