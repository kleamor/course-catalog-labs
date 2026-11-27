type StudentOption = { id: string; name: string };

export function StudentPicker({ students, selectedId }: { students: StudentOption[]; selectedId?: string }) {
  return (
    <form method="get" className="flex flex-wrap items-end gap-3 rounded-2xl border border-emerald-900/10 bg-white p-5">
      <label htmlFor="studentId" className="grid gap-2 text-sm font-semibold text-emerald-950">
        Student
        <select
          id="studentId"
          name="studentId"
          defaultValue={selectedId ?? ""}
          className="min-w-56 rounded-lg border border-emerald-900/20 bg-white px-3 py-2 font-normal"
        >
          <option value="" disabled>Choose a student</option>
          {students.map((student) => <option key={student.id} value={student.id}>{student.name}</option>)}
        </select>
      </label>
      <button type="submit" className="rounded-full bg-emerald-700 px-5 py-2 text-sm font-semibold text-white hover:bg-emerald-800">
        Show courses
      </button>
    </form>
  );
}
