import Link from "next/link";
import { api } from "@/lib/api";

type Student = { id: number; name: string };
type Enrollment = { id: number; studentId: number; courseId: string };
type Course = { title: string; credits: number; level: string };

export default async function MyCoursesRestPage() {
  const students = await api<Student[]>("/students");
  const student = students.find(({ id }) => id === 2);
  const enrollments = await api<Enrollment[]>("/enrollments");
  const mine = enrollments.filter(({ studentId }) => studentId === 2);
  const courses = await Promise.all(mine.map(({ courseId }) => api<Course>(`/courses/${courseId}`)));
  return <section className="space-y-6"><h1 className="font-serif text-4xl font-bold text-emerald-950">My courses · REST</h1><p>{student?.name ?? "Student not found"}</p><ul className="space-y-3">{mine.map(({ id }, index) => <li key={id} className="rounded-2xl border border-emerald-900/10 bg-white p-5"><strong>{courses[index].title}</strong><p>{courses[index].credits} credits · {courses[index].level}</p></li>)}</ul><Link className="text-sky-700 underline" href="/my-courses">Compare GraphQL version</Link></section>;
}
