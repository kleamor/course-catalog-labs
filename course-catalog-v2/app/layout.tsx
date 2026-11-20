import type { Metadata } from "next";
import type { ReactNode } from "react";
import { Geist, Geist_Mono } from "next/font/google";
import Link from "next/link";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Northstar Course Catalog",
  description: "An editorial course catalog for Advanced Web Technologies",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col">
        <nav className="border-b border-emerald-950/10 bg-background/80 px-4 py-4 backdrop-blur sm:px-6">
          <div className="mx-auto flex max-w-6xl items-center justify-between gap-4">
            <Link href="/" className="font-serif text-xl font-black tracking-tight text-emerald-950">
              NORTHSTAR<span className="text-sky-600">.</span>
            </Link>
            <div className="flex items-center gap-1 sm:gap-2">
              <Link
                href="/"
                className="rounded-full px-3 py-2 text-sm font-semibold text-emerald-950 transition-colors hover:bg-sky-100"
              >
                Home
              </Link>
              <Link
                href="/courses"
                className="rounded-full px-3 py-2 text-sm font-semibold text-emerald-950 transition-colors hover:bg-sky-100"
              >
                Courses
              </Link>
              <Link
                href="/filter"
                className="rounded-full px-3 py-2 text-sm font-semibold text-emerald-950 transition-colors hover:bg-sky-100"
              >
                Filter
              </Link>
              <Link
                href="/about"
                className="rounded-full px-3 py-2 text-sm font-semibold text-emerald-950 transition-colors hover:bg-sky-100"
              >
                About
              </Link>
            </div>
          </div>
        </nav>
        <main className="mx-auto w-full max-w-6xl flex-1 px-4 py-10 sm:px-6 sm:py-14">
          {children}
        </main>
      </body>
    </html>
  );
}
