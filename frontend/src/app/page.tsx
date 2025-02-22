"use client"

import { useState } from "react";
import SearchBar from "@/components/SearchBar";

export default function SearchPage() {
  const [query, setQuery] = useState("");

  return (
    <div className="flex flex-col gap-6 items-center justify-center h-screen max-w-5xl mx-auto">
      <div className="text-3xl font-bold">
        SmartCart
      </div>
      <SearchBar />
    </div>
  );
}
