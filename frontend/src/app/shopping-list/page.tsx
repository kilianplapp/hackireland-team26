"use client";

import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

export default function ShoppingListPage() {
  const [productInput, setProductInput] = useState("");
  const [shoppingList, setShoppingList] = useState<string[]>([]);
  const [results, setResults] = useState<any>({}); 


  const handleAddProduct = () => {
    if (productInput.trim() !== "") {
      setShoppingList((prev) => [...prev, productInput.trim()]);
      setProductInput("");
    }
  };


  const handleFetchData = async () => {
    try {
      const queryParams = shoppingList
        .map((item) => `items=${encodeURIComponent(item)}`)
        .join("&");

      const res = await fetch(`http://127.0.0.1:5000/api/shopping-list?${queryParams}`);
      const data = await res.json();
      setResults(data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  return (
    <div className="flex flex-col gap-6 items-center justify-center min-h-screen max-w-3xl mx-auto p-4">
      <h1 className="text-3xl font-bold">Shopping List</h1>

      {/* ---- Product Input Field ---- */}
      <div className="flex gap-2 w-full max-w-md">
        <Input
          type="text"
          placeholder="Enter a product..."
          value={productInput}
          onChange={(e) => setProductInput(e.target.value)}
        />
        <Button variant="default" onClick={handleAddProduct}>
          Add
        </Button>
      </div>

      {/* ---- Display Current Shopping List ---- */}
      <div className="w-full max-w-md">
        <h2 className="text-xl font-semibold mt-4 mb-2">Your Shopping List</h2>
        {shoppingList.length === 0 ? (
          <p className="text-gray-500">No items in the list yet.</p>
        ) : (
          <ul className="list-disc ml-5">
            {shoppingList.map((item, idx) => (
              <li key={idx} className="text-lg">
                {item}
              </li>
            ))}
          </ul>
        )}
      </div>

      {/* ---- Button to Trigger DB/Web Scrape ---- */}
      <Button variant="secondary" className="font-bold" onClick={handleFetchData}>
        Fetch from DB + Scrape
      </Button>

      {/* ---- Show Results from Flask ---- */}
      {Object.keys(results).length > 0 && (
        <div className="w-full max-w-md mt-6">
          <h2 className="text-xl font-semibold mb-2">Fetched/Scraped Results</h2>
          <pre className="bg-gray-100 rounded p-3 text-sm overflow-x-auto">
            {JSON.stringify(results, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}
