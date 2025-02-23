interface ProductProps {
  query: string;
  shop: string;
  price: string;
  image: string;
  starred?: boolean;
}

const defaultImageStyle = "border border-gray-100 shadow-sm rounded-xl";
const starredImageStyle = "border-2 border-yellow-300 shadow-sm rounded-xl";

export default function Product({
  query,
  shop,
  price,
  image,
  starred = false,
}: ProductProps) {
  return (
    <div>
      <div className="mb-3 relative">
        <img
          className={starred ? starredImageStyle : defaultImageStyle}
          src={image}
          alt={query}
        />

        {starred && (
          <svg
            className="absolute -top-2.5 -right-2.5"
            xmlns="http://www.w3.org/2000/svg"
            width="34"
            height="34"
            viewBox="0 0 50 50"
            fill="#eab308"
          >
            <path d="M10.2,48.6c-0.2,0-0.4-0.1-0.6-0.2c-0.3-0.2-0.5-0.7-0.4-1.1l4.4-16.4L0.4,20.2C0,20-0.1,19.5,0,19.1 c0.1-0.4,0.5-0.7,0.9-0.7l17-0.9l6.1-15.9C24.2,1.3,24.6,1,25,1c0.4,0,0.8,0.3,0.9,0.6l6.1,15.9l17,0.9c0.4,0,0.8,0.3,0.9,0.7 c0.1,0.4,0,0.8-0.3,1.1L36.4,30.9l4.4,16.4c0.1,0.4,0,0.8-0.4,1.1c-0.3,0.2-0.8,0.3-1.1,0L25,39.2l-14.3,9.2 C10.5,48.6,10.4,48.6,10.2,48.6z"></path>
          </svg>
        )}
      </div>

      {/* This should be the name of the product in the queried store */}
      <div className="text-lg font-semibold">{query}</div>
      <div>{shop}</div>
      <div>{price}</div>
    </div>
  );
}