import assert from "node:assert/strict";
import { readFileSync, readdirSync } from "node:fs";
import { relative, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const projectRoot = fileURLToPath(new URL("..", import.meta.url));

function readProjectFile(path: string) {
  return readFileSync(resolve(projectRoot, path), "utf8");
}

function sourceFiles(directory: string): string[] {
  const absoluteDirectory = resolve(projectRoot, directory);

  return readdirSync(absoluteDirectory, { withFileTypes: true }).flatMap(
    (entry) => {
      const absolutePath = resolve(absoluteDirectory, entry.name);

      if (entry.isDirectory()) {
        return sourceFiles(relative(projectRoot, absolutePath));
      }

      return /\.tsx?$/.test(entry.name) ? [absolutePath] : [];
    },
  );
}

test("CourseCard uses only the required shadcn card primitives", () => {
  const courseCard = readProjectFile("components/CourseCard.tsx");

  assert.doesNotMatch(courseCard, /<\/?(?:div|button)\b/);
  assert.match(
    courseCard,
    /import\s*\{[^}]*\bButton\b[^}]*\}\s*from\s*["']@\/components\/ui\/button["']/,
  );
  assert.match(
    courseCard,
    /import\s*\{[^}]*\bCard\b[^}]*\bCardContent\b[^}]*\bCardHeader\b[^}]*\bCardTitle\b[^}]*\}\s*from\s*["']@\/components\/ui\/card["']/,
  );

  for (const component of [
    "Card",
    "CardHeader",
    "CardTitle",
    "CardContent",
    "Button",
  ]) {
    assert.match(courseCard, new RegExp(`<${component}\\b`));
  }

  assert.match(courseCard, /<Link\b[\s\S]*<Card\b[\s\S]*<Button\b[\s\S]*<\/Link>/);
});

test("interactive API components are client components", () => {
  const clientComponents = ["app", "components", "lib"]
    .flatMap(sourceFiles)
    .filter((path) => /^\s*["']use client["'];?/m.test(readFileSync(path, "utf8")))
    .map((path) => relative(projectRoot, path))
    .sort();

  assert.deepEqual(clientComponents, [
    "app/courses/error.tsx",
    "components/ElectiveFilter.tsx",
    "components/EnrollForm.tsx",
    "components/LikeButton.tsx",
  ]);
});

test("course routes retain responsive grid and dynamic API setup", () => {
  const coursesPage = readProjectFile("app/courses/page.tsx");
  const coursePage = readProjectFile("app/courses/[id]/page.tsx");

  assert.match(coursesPage, /grid-cols-1/);
  assert.match(coursesPage, /sm:grid-cols-2/);
  assert.match(coursesPage, /lg:grid-cols-3/);
  assert.match(coursePage, /params:\s*Promise<\{\s*id:\s*string\s*\}>/);
  assert.match(coursePage, /const\s*\{\s*id\s*\}\s*=\s*await\s+params/);
  assert.doesNotMatch(coursePage, /generateStaticParams/);
  assert.match(coursePage, /<LikeButton\s+courseId=\{course\.id\}/);
  assert.match(coursePage, /<EnrollForm\s+courseId=\{course\.id\}/);
});

test("Lab 5 frontend files use the API contract", () => {
  const courses = readProjectFile("lib/courses.ts");
  const filter = readProjectFile("components/ElectiveFilter.tsx");
  const likeButton = readProjectFile("components/LikeButton.tsx");
  const enrollForm = readProjectFile("components/EnrollForm.tsx");
  const errorPage = readProjectFile("app/courses/error.tsx");

  assert.match(courses, /process\.env\.API_URL/);
  assert.match(courses, /cache:\s*["']no-store["']/);
  assert.match(courses, /response\.status\s*===\s*404/);
  assert.match(filter, /useSWR/);
  assert.match(filter, /is_elective=true/);
  assert.match(likeButton, /method:\s*["']POST["']/);
  assert.match(likeButton, /courses\/\$\{courseId\}\/like/);
  assert.match(enrollForm, /Content-Type.*application\/json/);
  assert.match(enrollForm, /response\.status\s*===\s*422/);
  assert.match(errorPage, /retry/);
});
