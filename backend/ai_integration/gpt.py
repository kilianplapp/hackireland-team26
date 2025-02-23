from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()


class Products(BaseModel):
    best_deal_products: list[str]


def best_deal_from_each_store(products_json: str, query: str):
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You will be given json of grocery products, a result of a search for "
                    f"a users query, which was {query}. Output only one group which is most relevant to the users query. "
                    "This group should contain JUST ONE PRODUCT FROM EACH SUPERMARKET. The items in the group "
                    "should also represent the best VALUE FOR MONEY from THE SAME CATEGORY OF ITEM."
                    "This allows the user to search and find only the most relevant and best deal from each supermarket."
                    "Output the EXACT names of the products."
                    "Your output will be interpreted by a computer so you must not deviate from this format."
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
