"use client";

import Product from "@/components/Product";
import Link from "next/link";
import { useState, useEffect } from "react";
import { useSearchParams } from "next/navigation";

export default function SearchPage() {
  const searchParams = useSearchParams();
  const query = searchParams.get("q") || "";
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    const fetchData = async () => {
      if (query.trim() !== "") {
        setLoading(true);
        try {
          const res = await fetch(`http://127.0.0.1:5000/api/products?q=${encodeURIComponent(query)}`);
          const data = await res.json();
          setResults(data);
        } catch (error) {
          console.error("Error fetching data:", error);
        } finally {
          setLoading(false);
        }
      }
    };

    fetchData();
  }, [query]);

  return (
    <div className="grid grid-cols-2">
      <div className="px-8 py-6">
        <Link href="/" className="text-3xl font-bold">
          SmartCart
        </Link>
        <div className="mb-8 text-sm text-slate-500">
          Showing {results.length} results for "{query}"
        </div>

        {loading ? (
          <div className="flex justify-center items-center">
            <div className="text-xl font-semibold">Loading...</div>
            <img src="https://i.gifer.com/origin/b4/b4d657e7ef262b88eb5f7ac021edda87_w200.gif" height={50} width={50} alt="loading" />
            <div className="spinner"></div>
          </div>
        ) : (
          <div className="grid grid-cols-3 gap-8">
            {results.map((product, index) => (
              <Product key={index} query={product.title} shop={product.shop} price={product.price} image={product.image} />
            ))}
          </div>
        )}
      </div>

      {/* <Map /> */}
    </div>
  );
}
