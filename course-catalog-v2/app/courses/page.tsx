import { CourseCard } from "@/components/CourseCard";
import { getCourses } from "@/lib/courses";

export default async function CoursesPage() {
  const courses = await getCourses();

  return (
    <section className="space-y-8">
      <div className="grid gap-3 border-b border-emerald-950/15 pb-7 sm:grid-cols-[1fr_auto] sm:items-end">
        <div className="space-y-2">
          <p className="text-xs font-bold uppercase tracking-[0.2em] text-sky-700">
            Curriculum · 06 courses
          </p>
          <h1 className="font-serif text-4xl font-black tracking-tight text-emerald-950 sm:text-5xl">
            Course index
          </h1>
        </div>
        <p className="max-w-xs text-sm leading-6 text-muted-foreground sm:text-right">
          Select a course for its outline, credits, and a quick show of support.
        </p>
      </div>
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
        {courses.map((course) => (
          <CourseCard key={course.id} {...course} />
        ))}
      </div>
    </section>
  );
}
