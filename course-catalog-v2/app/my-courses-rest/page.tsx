import Link from "next/link";
import { StudentPicker } from "@/components/StudentPicker";
import { api } from "@/lib/api";

type Student = { id: number; name: string };
type Enrollment = { id: number; studentId: number; courseId: string };
type Course = { title: string; credits: number; level: string };

export default async function MyCoursesRestPage({
  searchParams,
}: {
  searchParams: Promise<{ studentId?: string }>;
}) {
  const { studentId } = await searchParams;
  const selectedId = studentId && /^\d+$/.test(studentId) ? studentId : undefined;
  const students = await api<Student[]>("/students");
  const student = students.find(({ id }) => String(id) === selectedId);
  const mine = student
    ? (await api<Enrollment[]>("/enrollments")).filter(({ studentId }) => studentId === student.id)
    : [];
  const courses = await Promise.all(mine.map(({ courseId }) => api<Course>(`/courses/${courseId}`)));

  return (
    <section className="space-y-6">
      <h1 className="font-serif text-4xl font-bold text-emerald-950">My courses · REST</h1>
      <StudentPicker students={students.map(({ id, name }) => ({ id: String(id), name }))} selectedId={student ? selectedId : undefined} />
      {student ? (
        <>
          <h2 className="text-xl font-semibold text-emerald-950">{student.name}</h2>
          {mine.length ? (
            <ul className="space-y-3">
              {mine.map(({ id }, index) => (
                <li key={id} className="rounded-2xl border border-emerald-900/10 bg-white p-5">
                  <strong>{courses[index].title}</strong>
                  <p>{courses[index].credits} credits · {courses[index].level}</p>
                </li>
              ))}
            </ul>
          ) : <p>This student has no courses yet.</p>}
        </>
      ) : <p>{selectedId ? "Student not found. Choose another student." : "Choose a student to see their courses."}</p>}
      <Link className="text-sky-700 underline" href={selectedId ? `/my-courses?studentId=${selectedId}` : "/my-courses"}>
        Compare GraphQL version
      </Link>
    </section>
  );
}
