/**
 * Converts a price string (e.g., "€1.59") into a numeric value.
 * Supports different currency formats.
 *
 * @param {string} priceStr - The price string to convert.
 * @returns {number} The numeric value of the price.
 * @throws {Error} If the input string cannot be converted to a number.
 */
export const convertPrice = (priceStr: string): number => {
    // Extract the numeric part using regex
    const numericValue = priceStr.replace(/[^\d.,]/g, "").replace(",", ".");
  
    // Convert to float
    const result = parseFloat(numericValue);
  
    if (isNaN(result)) {
      throw new Error("Invalid price string");
    }
  
    return result;
  };