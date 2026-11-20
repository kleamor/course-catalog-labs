"use client";

import { useState } from "react";

import type { Course } from "@/lib/courses";
import { Button } from "@/components/ui/button";

const API = process.env.NEXT_PUBLIC_API_URL;

type LikeButtonProps = {
  courseId: string;
  initialLikes: number;
};

export function LikeButton({ courseId, initialLikes }: LikeButtonProps) {
  const [likes, setLikes] = useState(initialLikes);
  const [failed, setFailed] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleClick() {
    setFailed(false);
    setIsSubmitting(true);

    try {
      const response = await fetch(`${API}/courses/${courseId}/like`, {
        method: "POST",
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const course: Course = await response.json();
      setLikes(course.likes);
    } catch {
      setFailed(true);
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="space-y-2">
      <Button
        type="button"
        className="rounded-full border-emerald-950/15 bg-sky-100 px-4 text-sky-900 hover:bg-sky-200"
        variant="outline"
        disabled={isSubmitting}
        onClick={handleClick}
      >
        ♥ {likes}
      </Button>
      {failed && (
        <p className="text-sm font-medium text-red-700" role="alert">
          Failed to like the course.
        </p>
      )}
    </div>
  );
}
