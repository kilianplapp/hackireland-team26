"use client"

import { useRouter } from "next/navigation";
import SearchBar from "@/components/SearchBar";
import { Button } from "@/components/ui/button";

export default function HomePage() {
  const router = useRouter();

  return (
    <div className="flex flex-col gap-6 items-center justify-center h-screen max-w-5xl mx-auto">
      <div className="text-3xl font-bold">SmartCart</div>

      <SearchBar />

      <Button
        variant="default"
        size="lg"
        className="mt-6 px-6 py-3 text-lg"
        onClick={() => router.push("/shopping-list")}
      >
        Create Shopping List
      </Button>
    </div>
  );
}
