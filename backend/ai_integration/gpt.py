from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()


class Products(BaseModel):
    groups: list[str]
    products: list[list[int]]


def group_and_sort(products_json: str):
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You will be given json of grocery products, including a field with their IDs. Please group products that are the same but are "
                    "from different brands or in different sizes. Make the cheapest product from each group have the best_deal boolean set to true. "
                    "When grouping products, group them by use e.g Tomatoes are not same as Tomatoe Puree or Ketchup or Tomato Soup. "
                    "Please return the groups and the products sorted by price within each group."
                ),
            },
            {
                "role": "user",
                "content": products_json,
            },
        ],
        response_format=Products,
    )

    sorted_grouped_products = completion.choices[0].message.parsed
    return sorted_grouped_products.groups, sorted_grouped_products.products
