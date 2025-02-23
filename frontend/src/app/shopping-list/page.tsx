"use client";

import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import Product from "@/components/Product";
import { convertPrice } from "@/helpers/currency";

type Result = {
  ID: any;
  image: string;
  price: string;
  store: string;
  title: string;
  starred?: boolean;
  numericPrice?: number;
};

export default function ShoppingListPage() {
  const [productInput, setProductInput] = useState("");
  const [shoppingList, setShoppingList] = useState<string[]>([]);
  const [results, setResults] = useState<Record<string, Result[]>>({});

  const handleAddProduct = () => {
    if (productInput.trim() !== "") {
      setShoppingList((prev) => [...prev, productInput.trim()]);
      setProductInput("");
    }
  };

  const removeProductAtIndex = (index: number) => {
    const newList = [...shoppingList];
    newList.splice(index, 1);
    setShoppingList(newList);
  };

  const handleFetchData = async () => {
    try {
      for (const item of shoppingList) {
        const res = await fetch(
          `http://127.0.0.1:5000/api/products?q=${encodeURIComponent(item)}`
        );
        let data = await res.json();
        const prices = data.map((product: any) => convertPrice(product.price));
        const cheapestPrice = Math.min(...prices);

        data = data.map((product: any) => ({
          ...product,
          starred: convertPrice(product.price) === cheapestPrice,
          numericPrice: convertPrice(product.price),
        }));

        setResults((prevResults) => ({ ...prevResults, [item]: data }));
      }
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  return (
    <div className="py-24 flex flex-col gap-6 items-center justify-center min-h-screen max-w-3xl mx-auto p-4">
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
          <div className="flex flex-col gap-2">
            {shoppingList.map((item, idx) => (
              <div
                key={idx}
                className="text-lg bg-gray-100 py-2 px-3 rounded-lg flex justify-between"
              >
                {item}
                <button
                  onClick={() => removeProductAtIndex(idx)}
                  className="hover:text-red-500 text-slate-500 transition-colors duration-200"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    x="0px"
                    y="0px"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    className="fill-current"
                  >
                    <path d="M12,2C6.47,2,2,6.47,2,12c0,5.53,4.47,10,10,10s10-4.47,10-10C22,6.47,17.53,2,12,2z M16.707,15.293 c0.391,0.391,0.391,1.023,0,1.414C16.512,16.902,16.256,17,16,17s-0.512-0.098-0.707-0.293L12,13.414l-3.293,3.293 C8.512,16.902,8.256,17,8,17s-0.512-0.098-0.707-0.293c-0.391-0.391-0.391-1.023,0-1.414L10.586,12L7.293,8.707 c-0.391-0.391-0.391-1.023,0-1.414s1.023-0.391,1.414,0L12,10.586l3.293-3.293c0.391-0.391,1.023-0.391,1.414,0 s0.391,1.023,0,1.414L13.414,12L16.707,15.293z"></path>
                  </svg>
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* ---- Button to Trigger DB/Web Scrape ---- */}
      <Button
        variant="secondary"
        className="font-bold bg-sky-500 hover:bg-sky-600 text-white"
        onClick={handleFetchData}
      >
        Let's Go Shopping
      </Button>

      {/* ---- Show Results from Flask ---- */}
      {Object.keys(results).length > 0 && (
        <div className="w-full max-w-3xl mt-24">
          <h2 className="text-xl font-semibold mb-5">
            Fetched/Scraped Results
          </h2>

          <div className="flex flex-col gap-16">
            {Object.keys(results).map((key) => (
              <div key={key}>
                <div className="text-2xl text-center font-bold mb-6 capitalize">
                  {key}
                </div>

                <div className="grid grid-cols-4 gap-4">
                  {results[key].map((product, j) => (
                    <Product
                      key={j}
                      query={product.title}
                      shop={product.store}
                      price={product.price}
                      image={product.image}
                      starred={product.starred || false}
                    />
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
