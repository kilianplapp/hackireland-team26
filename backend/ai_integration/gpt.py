from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()


class Products(BaseModel):
    groups: list[list[str]]
    group_names: list[str]


def group_and_sort(products_json: str, query: str):
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You will be given json of grocery products, a result of a search for "
                    f"a users query, which was {query}. Please group products that could be considered alternatives "
                    "but are possibly from different brands and/or different sizes."
                    "Output human-readable names for the groups and the groups, "
                    "which should include exact names of the items as elements."
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
