from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()


class Product(BaseModel):
    id: int
    best_deal: bool


class Products(BaseModel):
    groups: list[list[Product]]
    group_names: list[str]


def group_and_sort(products_json: str, query: str):
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You will be given json of grocery products, including a field with their IDs. Please group products that are the same but are "
                    "from different brands or in different sizes. Create one group which is most relevant to the user's search query. "
                    "Only add the best deal from each supermarket. Do not include bundles in the groups. e.g carrots & parsnips are a separate group to just carrots"
                    "The user has searched for: " + query
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
    return sorted_grouped_products
