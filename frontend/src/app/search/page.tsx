import Map from "@/components/Map";
import Product from "@/components/Product";
import Link from "next/link";

export default function SearchPage({ query }) {
  return (
    <div className="grid grid-cols-2">
      <div className="px-8 py-6">
        <Link href="/" className="text-3xl font-bold">
          SmartCart
        </Link>

        <div className="mb-8 text-sm text-slate-500">
          showing 4 results for "carrot"
        </div>

        <div className="grid grid-cols-3 gap-8">
          <Product />
          <Product />
          <Product />
          <Product />
        </div>
      </div>

      <Map />
    </div>
  );
}
