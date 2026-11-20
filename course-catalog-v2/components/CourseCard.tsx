import Link from "next/link";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

type CourseCardProps = {
  id: string;
  title: string;
  description: string;
  credits: number;
  isElective: boolean;
  likes: number;
};

export function CourseCard({
  id,
  title,
  description,
  credits,
  isElective,
  likes,
}: CourseCardProps) {
  return (
    <Link className="block h-full" href={`/courses/${id}`}>
      <Card className="h-full border border-emerald-950/10 bg-card/90 shadow-sm transition duration-300 hover:-translate-y-1 hover:border-sky-400/80 hover:shadow-xl hover:shadow-emerald-950/10">
        <CardHeader className="gap-3">
          <p className="text-xs font-bold uppercase tracking-[0.16em] text-sky-700">
            {isElective ? "Elective" : "Core course"}
          </p>
          <CardTitle className="font-serif text-xl font-black leading-tight text-emerald-950">
            {title}
          </CardTitle>
        </CardHeader>
        <CardContent className="flex flex-1 flex-col gap-5">
          <p className="flex-1 leading-6 text-muted-foreground">{description}</p>
          <footer className="flex items-center justify-between border-t border-emerald-950/10 pt-4">
            <span className="text-sm font-bold text-emerald-950">{credits} credits</span>
            <Button
              aria-label={`${likes} likes`}
              className="pointer-events-none rounded-full text-sky-700"
              variant="ghost"
              size="sm"
            >
              ♥ {likes}
            </Button>
          </footer>
        </CardContent>
      </Card>
    </Link>
  );
}
