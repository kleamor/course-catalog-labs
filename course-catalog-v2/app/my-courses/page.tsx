import Link from "next/link";
import { StudentPicker } from "@/components/StudentPicker";
import { gql } from "@/lib/graphql";

type StudentOption = { id: string; name: string };
type Student = {
  name: string;
  enrollments: { id: string; course: { title: string; credits: number; level: string } }[];
};

export default async function MyCoursesPage({
  searchParams,
}: {
  searchParams: Promise<{ studentId?: string }>;
}) {
  const { studentId } = await searchParams;
  const selectedId = studentId && /^\d+$/.test(studentId) ? studentId : undefined;
  const data = selectedId
    ? await gql<{ students: StudentOption[]; student: Student | null }>(
        "query MyCourses($id: ID!) { students(limit: 100) { id name } student(id: $id) { name enrollments { id course { title credits level } } } }",
        { id: selectedId },
      )
    : await gql<{ students: StudentOption[]; student?: Student | null }>(
        "{ students(limit: 100) { id name } }",
        {},
      );
  const student = data.students.some(({ id }) => id === selectedId) ? data.student : null;

  return (
    <section className="space-y-6">
      <h1 className="font-serif text-4xl font-bold text-emerald-950">My courses · GraphQL</h1>
      <StudentPicker students={data.students} selectedId={student ? selectedId : undefined} />
      {student ? (
        <>
          <h2 className="text-xl font-semibold text-emerald-950">{student.name}</h2>
          {student.enrollments.length ? (
            <ul className="space-y-3">
              {student.enrollments.map(({ id, course }) => (
                <li key={id} className="rounded-2xl border border-emerald-900/10 bg-white p-5">
                  <strong>{course.title}</strong>
                  <p>{course.credits} credits · {course.level}</p>
                </li>
              ))}
            </ul>
          ) : <p>This student has no courses yet.</p>}
        </>
      ) : <p>{selectedId ? "Student not found. Choose another student." : "Choose a student to see their courses."}</p>}
      <Link className="text-sky-700 underline" href={selectedId ? `/my-courses-rest?studentId=${selectedId}` : "/my-courses-rest"}>
        Compare REST version
      </Link>
    </section>
  );
}
