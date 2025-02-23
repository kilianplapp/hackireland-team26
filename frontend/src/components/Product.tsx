// export default function Product() {
//   return (
//     <div>
//       <img
//         className="mb-3 border border-gray-100 shadow-sm rounded-xl"
//         src="https://digitalcontent.api.tesco.com/v2/media/ghs/a17ee4c9-ea9e-477a-b5f5-63850050e5ea/dec2b422-963a-4e99-a579-9417b1b47765_968650595.jpeg?h=960&w=960"
//         alt=""
//       />
//       <div className="text-lg font-semibold">Tesco Carrot Bag 500G</div>
//       <div>Tesco</div>
//       <div>€0.79</div>
//     </div>
//   );
// }

import React from "react";

interface ProductProps {
  query: string;
  shop: string;
  price: string;
  image: string;
}

/*

To-do:
- connect with backend (lol)
*/

export default function Product({ query, shop, price, image }: ProductProps) {
  return (
    <div>
      <img
        className="mb-3 border border-gray-100 shadow-sm rounded-xl"
        src={image}
        alt={query}
      />
      {/* This should be the name of the product in the queried store */}
      <div className="text-lg font-semibold">{query}</div>
      <div>{shop}</div>
      <div>{price}</div>
    </div>
  );
}
