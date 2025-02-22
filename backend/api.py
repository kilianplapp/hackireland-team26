from flask import Flask, request, jsonify
from scraping import tesco, supervalu, dunnes
from ai_integration import group_and_sort

app = Flask(__name__)


@app.route("/api/products")
def search_products():
    query = request.args.get("q", "").lower()

    tesco_products = tesco(query)
    for product in tesco_products:
        product["store"] = "Tesco"

    # dunnes_products = dunnes(jsonify(query))
    # for i, product in enumerate(dunnes_products):
    #     product["store"] = "Dunnes"
    #     product["ID"] = i

    # supervalu_products = supervalu(query)
    # for product in supervalu_products:
    #     product["store"] = "SuperValu"

    groups, products = group_and_sort(str(tesco_products))

    result = dict()
    for group, product in zip(groups, products):
        result[group] = [
            tesco_products[i] for i in product if (0 <= i and i < len(tesco_products))
        ]

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
