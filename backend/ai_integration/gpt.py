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
                    f"a users query, which was {query}. Output only one group which is most relevant to the users query. "
                    "This group should contain JUST ONE PRODUCT FROM EACH SUPERMARKET."
                    "This allows the user to search and find only the most relevant and best deal from each supermarket."
                    "Output human-readable names for the groups and the groups, "
                    "which should include exact names of the items as elements."
                    "Your output will be interpreted by a computer so you must not deviate from this format."
                    "Only output a single group."
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
