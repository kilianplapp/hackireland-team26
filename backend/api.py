from flask import Flask, request, jsonify
from scraping import tesco, supervalu, dunnes
from ai_integration import group_and_sort
import json
app = Flask(__name__)

id = 0


@app.route("/api/products")
def search_products():
    global id
    query = request.args.get("q", "").lower()

    tesco_products = tesco(query)
    for product in tesco_products:
        product["store"] = "Tesco"
        product["ID"] = id
        id += 1

    dunnes_products = dunnes(jsonify(query))
    for product in dunnes_products:
        product["store"] = "Dunnes"
        product["ID"] = id
        id += 1

    supervalu_products = supervalu(query)
    for product in supervalu_products:
        product["store"] = "SuperValu"
        product["ID"] = id
        id += 1

    all_products = tesco_products + supervalu_products + dunnes_products
    all_products_short = all_products.copy()
    # remove images from all products
    for product in all_products_short:
        product.pop("image", None)
    
    response = dict(group_and_sort(str(json.dumps(all_products_short)), query))
    group_names = response["group_names"]
    groups = response["groups"]

    result = dict()
    for i in range(len(group_names)):
        group_name = group_names[i]
        group = groups[i]
        result[group_name] = []
        for p in group:
            all_products[p.id]["best_deal"] = p.best_deal
            result[group_name] += [all_products[p.id]]

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
