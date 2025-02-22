from flask import Flask, request, jsonify
from scraping import tesco, supervalu, dunnes

app = Flask(__name__)


@app.route("/api/products")
def search_products():
    query = request.args.get("q", "").lower()

    tesco_products = tesco(query)
    for product in tesco_products:
        product["store"] = "Tesco"

    dunnes_products = dunnes(query)
    for product in dunnes_products:
        product["store"] = "Dunnes"

    supervalu_products = supervalu(query)
    for product in supervalu_products:
        product["store"] = "SuperValu"

    return jsonify(tesco_products + dunnes_products + supervalu_products)


if __name__ == "__main__":
    app.run(debug=True)
