import { notFound } from "next/navigation";

import { EnrollForm } from "@/components/EnrollForm";
import { LikeButton } from "@/components/LikeButton";
import { getCourse } from "@/lib/courses";

type CoursePageProps = {
  params: Promise<{ id: string }>;
};

export default async function CoursePage({ params }: CoursePageProps) {
  const { id } = await params;
  const course = await getCourse(id);

  if (!course) {
    notFound();
  }

  return (
    <article className="mx-auto max-w-3xl overflow-hidden rounded-[2rem] border border-emerald-950/10 bg-card/90 shadow-xl shadow-emerald-950/10">
      <div className="bg-emerald-950 px-6 py-8 text-sky-50 sm:px-10 sm:py-11">
        <p className="text-xs font-bold uppercase tracking-[0.2em] text-sky-300">
          {course.isElective ? "Elective studio" : "Core course"}
        </p>
        <h1 className="mt-4 font-serif text-4xl font-black tracking-tight sm:text-5xl">
          {course.title}
        </h1>
      </div>
      <div className="space-y-8 px-6 py-8 sm:px-10 sm:py-10">
        <p className="text-lg leading-8 text-muted-foreground">
          {course.description}
        </p>
        <div className="flex flex-wrap items-center justify-between gap-4 border-t border-emerald-950/10 pt-6">
          <p className="rounded-full bg-sky-100 px-4 py-2 text-sm font-bold text-sky-900">
            {course.credits} credits
          </p>
          <LikeButton courseId={course.id} initialLikes={course.likes} />
        </div>
        <section className="space-y-4 border-t border-emerald-950/10 pt-6">
          <h2 className="font-serif text-2xl font-black text-emerald-950">
            Enroll in this course
          </h2>
          <EnrollForm courseId={course.id} />
        </section>
      </div>
    </article>
  );
}
