from flask import Flask, request, jsonify
from scraping import tesco, supervalu, dunnes

app = Flask(__name__)


@app.route("/api/products")
def search_products():
    query = request.args.get("q", "").lower()

    products = dict()

    products["tesco"] = tesco(query)

    products["dunnes"] = dunnes(query)

    products["supervalu"] = supervalu(query)

    return jsonify(products)


if __name__ == "__main__":
    app.run(debug=True)
