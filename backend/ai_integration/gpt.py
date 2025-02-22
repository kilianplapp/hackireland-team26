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
                    "You will be given json of products, icluding a field with their IDs. Come up with a maximum of five"
                    "categories for the products and respond with a dictionary where the key is the name of the category"
                    "and the value is a list of IDs belonging to it, sorted by the best value product. If there is no data,"
                    "do not make up groups. Do not make up IDs."
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
