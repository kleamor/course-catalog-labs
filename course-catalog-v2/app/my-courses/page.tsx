import Link from "next/link";
import { gql } from "@/lib/graphql";

type Student = { name: string; enrollments: { id: string; course: { title: string; credits: number; level: string } }[] };

export default async function MyCoursesPage() {
  const { student } = await gql<{ student: Student | null }>(
    "query MyCourses($id: ID!) { student(id: $id) { name enrollments { id course { title credits level } } } }",
    { id: "2" },
  );
  return <section className="space-y-6"><h1 className="font-serif text-4xl font-bold text-emerald-950">My courses · GraphQL</h1><p>{student?.name ?? "Student not found"}</p><ul className="space-y-3">{student?.enrollments.map(({ id, course }) => <li key={id} className="rounded-2xl border border-emerald-900/10 bg-white p-5"><strong>{course.title}</strong><p>{course.credits} credits · {course.level}</p></li>)}</ul><Link className="text-sky-700 underline" href="/my-courses-rest">Compare REST version</Link></section>;
}
