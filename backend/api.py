from flask import Flask, request, jsonify
from scraping import tesco, supervalu, dunnes
from ai_integration import group_and_sort

app = Flask(__name__)


@app.route("/api/products")
def search_products():
    query = request.args.get("q", "").lower()

    tesco_products = tesco(query)
    for i, product in enumerate(tesco_products):
        product["store"] = "Tesco"
        product["ID"] = i

    # dunnes_products = dunnes(jsonify(query))
    # for i, product in enumerate(dunnes_products):
    #     product["store"] = "Dunnes"
    #     product["ID"] = i

    # supervalu_products = supervalu(query)
    # for product in supervalu_products:
    #     product["store"] = "SuperValu"

    response = dict(group_and_sort(str(tesco_products)))
    group_names = response["group_names"]
    groups = response["groups"]

    result = dict()
    for i in range(len(group_names)):
        group_name = group_names[i]
        group = groups[i]
        result[group_name] = []
        for p in group:
            tesco_products[p.id]["best_deal"] = p.best_deal
            result[group_name] += [tesco_products[p.id]]

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
