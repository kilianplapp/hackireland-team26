from flask import Flask, request, jsonify
from scraping import tesco

app = Flask(__name__)


@app.route("/api/products")
def search_products():
    query = request.args.get("q", "").lower()

    tesco_products = tesco.main(query)

    return jsonify(tesco_products)


if __name__ == "__main__":
    app.run(debug=True)
