import Product from "@/components/Product";
import Link from "next/link";

export default function SearchPage({ searchParams }: { searchParams: { q?: string } }) {
  const query = searchParams.q || "";

  return (
    <div className="grid grid-cols-2">
      <div className="px-8 py-6">
        <Link href="/" className="text-3xl font-bold">
          SmartCart
        </Link>

        <div className="mb-8 text-sm text-slate-500">
          Showing 4 results for "{query}"
        </div>

        <div className="grid grid-cols-3 gap-8">
          <Product query={query} shop="Tesco" />
          <Product query={query} shop="Supervalu" />
          <Product query={query} shop="Dunnes" />
          <Product query={query} shop="Aldi" />
        </div>
      </div>

      {/* <Map /> */}
    </div>
  );
}
