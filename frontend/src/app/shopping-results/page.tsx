"use client";

import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import { motion } from "framer-motion";
import Image from "next/image";

export default function ShoppingResults() {
  const searchParams = useSearchParams();
  const items = searchParams.get("items")?.split(",") || [];
  const [results, setResults] = useState<{ [key: string]: any[] }>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (items.length === 0) return;

    const fetchShoppingList = async () => {
      setLoading(true);

      try {
        const response = await fetch("http://127.0.0.1:5000/api/shopping-list", {
          method: "POST", 
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ items })
        });

        if (!response.ok) {
          throw new Error("Failed to fetch shopping list");
        }

        const data = await response.json();
        setResults(data);
      } catch (error) {
        console.error("Error fetching shopping list:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchShoppingList();
  }, [items]);

  return (
    <div className="max-w-5xl mx-auto p-6">
      <h1 className="text-3xl font-bold text-center mb-6">Best Prices Found</h1>

      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {items.map((item, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0.5 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 1, repeat: Infinity, repeatType: "reverse" }}
              className="p-4 border rounded-lg shadow-md bg-gray-100 animate-pulse"
            >
              <div className="h-6 bg-gray-300 w-2/3 mb-2 rounded"></div>
              <div className="h-4 bg-gray-300 w-1/2 rounded"></div>
            </motion.div>
          ))}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {Object.entries(results).map(([item, products]) => (
            <div key={item} className="border p-4 rounded-lg shadow-md">
              <h2 className="text-xl font-bold mb-3">{item}</h2>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {products.map((product) => (
                  <div key={product.store} className="text-center">
                    <Image
                      src={product.image || "/placeholder.png"}
                      alt={product.title}
                      width={100}
                      height={100}
                      className="rounded-lg"
                    />
                    <div className="font-semibold">{product.store}</div>
                    <div className="text-green-600 font-bold">€{product.price}</div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
