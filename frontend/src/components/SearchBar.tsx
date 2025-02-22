"use client";

import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useState } from "react";
import { motion } from "framer-motion";
import { Search } from "lucide-react";
import { useRouter } from "next/navigation";

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const router = useRouter();

  const onSearch = () => {
    router.push(`/search?q=${query}`);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="w-full max-w-lg p-4"
    >
      <div className="relative">
        <Input
          type="text"
          placeholder="Search..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="w-full p-3 text-xl border rounded-2xl shadow-md pr-12"
        />

        <Button
          onClick={onSearch}
          className="absolute right-2 top-1/2 transform -translate-y-1/2 p-2"
        >
          <Search className="w-5 h-5" />
        </Button>
      </div>
    </motion.div>
  );
}
