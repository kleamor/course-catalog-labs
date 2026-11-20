import assert from "node:assert/strict";
import test from "node:test";

process.env.API_URL = "http://api.example.test";

function loadCoursesModule() {
  return import("../lib/courses");
}

const course = {
  id: "modern-frontend",
  title: "Modern Frontend: React & Next.js",
  description: "React 19, Server Components, and the App Router.",
  credits: 5,
  isElective: false,
  likes: 24,
};

test("getCourses reads the catalog from the API without a cache", async (t) => {
  const { getCourses } = await loadCoursesModule();
  const originalFetch = globalThis.fetch;
  let url = "";
  let cache: RequestCache | undefined;

  globalThis.fetch = (async (input, init) => {
    url = String(input);
    cache = init?.cache;
    return Response.json([course]);
  }) as typeof fetch;
  t.after(() => {
    globalThis.fetch = originalFetch;
  });

  const courses = await getCourses();

  assert.deepEqual(courses, [course]);
  assert.equal(url, "http://api.example.test/courses");
  assert.equal(cache, "no-store");
});

test("getCourse returns undefined for an API 404", async (t) => {
  const { getCourse } = await loadCoursesModule();
  const originalFetch = globalThis.fetch;
  globalThis.fetch = (async () => new Response(null, { status: 404 })) as typeof fetch;
  t.after(() => {
    globalThis.fetch = originalFetch;
  });

  assert.equal(await getCourse("does-not-exist"), undefined);
});

test("getCourse throws for an API failure other than 404", async (t) => {
  const { getCourse } = await loadCoursesModule();
  const originalFetch = globalThis.fetch;
  globalThis.fetch = (async () => new Response(null, { status: 500 })) as typeof fetch;
  t.after(() => {
    globalThis.fetch = originalFetch;
  });

  await assert.rejects(getCourse("modern-frontend"), /API error: 500/);
});
