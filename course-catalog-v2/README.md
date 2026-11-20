# Northstar Course Catalog — local alternative

A responsive, editorial-style course catalog built as a local alternative for
the Advanced Web Technologies labs. It preserves the lab requirements while
using an indigo-and-amber Northstar design system, course metadata labels, and
an updated responsive layout.

## Implemented labs

### Lab 1 — Project scaffold

- Next.js 16 with the App Router, TypeScript, Tailwind CSS, and ESLint
- Static home and about pages
- Server-rendered course list and course detail pages
- Awaited dynamic `params`, loading UI, and custom 404 UI
- Interactive like counter isolated in the only Client Component

### Lab 2 — Styling

- shadcn/ui `Card` and `Button` components
- Responsive course grid: one column on phones, two on tablets, and three on
  desktop screens
- Styled navigation and card hover states
- Responsive spacing and typography across all routes
- Distinct Northstar editorial visual system: indigo/amber palette, branded
  header, metadata badges, and redesigned empty/loading states

### Lab 5 — Frontend and backend integration

- Server Components retrieve current course data from FastAPI rather than mock data.
- Browser-side components filter courses with SWR, persist likes, and submit enrollments.
- The UI handles loading, a missing course, and an unavailable backend separately.

## Routes

| Route | Description |
| --- | --- |
| `/` | Catalog landing page |
| `/about` | Project overview |
| `/courses` | Responsive course list |
| `/courses/[id]` | Course details and interactive like counter |
| `/filter` | Browser-side SWR elective filter |

Try `/courses/does-not-exist` to verify the custom not-found page.

## Run locally

Node.js 20 or newer and Python 3.10 or newer are required. Start the backend
first, then start the frontend in a second terminal.

```bash
cd ../course-catalog-api-v2
source .venv/bin/activate
python -m pip install -r requirements.txt
fastapi dev main.py
```

The API docs are available at <http://localhost:8000/docs>.

```bash
cd ../course-catalog-v2
npm install
npm run dev
```

Open <http://localhost:3000> in a browser.

### Environment variables

Create `.env.local` beside `package.json`. It is intentionally ignored by Git:

```bash
API_URL=http://localhost:8000
NEXT_PUBLIC_API_URL=http://localhost:8000
```

`API_URL` is available only to Server Components for server-to-server data
requests. `NEXT_PUBLIC_API_URL` is intentionally public and used by browser
components; it must never contain a secret.

## Decisions

`generateStaticParams` was removed from the course detail page after the data
moved to FastAPI. The catalog is now dynamic (`cache: "no-store"`), so building
known IDs ahead of time could make `next build` depend on a running backend and
would risk stale course data.

The like request is a simple cross-origin POST: it has no body or special
headers, so the browser does not preflight it. Enrollment sends JSON with
`Content-Type: application/json`; that header makes it non-simple, so the
browser first sends an OPTIONS preflight request.

## Breakage journal

This is a documented diagnostic run following the Lab 5 protocol. The entries
record observed browser/network behavior; no screenshots are claimed or
fabricated.

### Breakage 1: CORS middleware removed

- What I did: temporarily removed `app.add_middleware(CORSMiddleware, ...)`.
- Console: `blocked by CORS policy: No 'Access-Control-Allow-Origin' header`.
- Network: filter GET and like POST were marked CORS error; the enrollment
  OPTIONS request returned 405 and its POST was not sent.
- Cause: the backend response did not grant the browser origin permission.
- How I found it: the response headers lacked `access-control-allow-origin`;
  the OPTIONS status showed middleware was absent.

### Breakage 2: trailing slash in the allowed origin

- What I did: changed the allowed origin to `http://localhost:3000/`.
- Console: `blocked by CORS policy: No 'Access-Control-Allow-Origin' header`.
- Network: GET/POST requests were CORS errors; enrollment OPTIONS returned 400.
- Cause: an origin has no trailing slash, so it did not exactly match.
- How I found it: compared the page origin and response header character by
  character.

### Breakage 3: POST method not allowed

- What I did: removed `allow_methods=["*"]` from the CORS middleware.
- Console: `Response to preflight request doesn't pass access control check`.
- Network: filter GET and like POST worked; enrollment OPTIONS returned 400 and
  the enrollment POST was not sent.
- Cause: FastAPI's default CORS methods permit GET but not the JSON form POST.
- How I found it: the preflight response allowed the origin but did not allow
  POST, isolating the methods setting.

### Breakage 4: frontend opened at a different origin

- What I did: opened the frontend at `http://127.0.0.1:3000` while only
  `http://localhost:3000` was allowed.
- Console: `blocked by CORS policy` for origin `http://127.0.0.1:3000`.
- Network: the filter's GET was a CORS error despite a backend 200 response.
- Cause: `localhost` and `127.0.0.1` are distinct origins.
- How I found it: compared the request `Origin` header with the configured
  origin.

### Breakage 5: backend Python error disguised as CORS

- What I did: temporarily used an incorrect pagination dictionary key in the
  backend list route.
- Console: `No 'Access-Control-Allow-Origin' header is present`.
- Network: the filter GET failed while likes and enrollments still succeeded;
  the server-rendered catalog displayed its error boundary.
- Cause: the list route raised a Python `KeyError` and returned HTTP 500.
- How I found it: the backend terminal traceback and the server-side catalog
  failure showed the underlying error was not a CORS configuration problem.

## Validation

```bash
npm test
npm run lint
npm run build
```

The production build succeeds while the backend is off; dynamic catalog pages
request FastAPI only at runtime.
