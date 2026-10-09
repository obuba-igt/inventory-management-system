from flask import Flask, request, jsonify
from external_api import fetch_from_openfoodfacts

app = Flask(__name__)


inventory = []
id_counter = 1


def find_item(item_id):
    return next((item for item in inventory if item["id"] == item_id), None)


@app.route('/')
def home():
    return jsonify({"message": "Inventory Management API", "endpoints": ["/inventory"]})


@app.route('/inventory', methods=['GET'])
def get_all():
    return jsonify(inventory), 200


@app.route('/inventory/<int:item_id>', methods=['GET'])
def get_one(item_id):
    item = find_item(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item), 200


@app.route('/inventory', methods=['POST'])
def add_item():
    global id_counter
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    enhanced = {}
    if data.get("barcode"):
        enhanced = fetch_from_openfoodfacts(barcode=data.get("barcode"))
    elif data.get("product_name"):
        enhanced = fetch_from_openfoodfacts(
            product_name=data.get("product_name"))

    new_item = {
        "id": id_counter,
        "product_name": data.get("product_name") or enhanced.get("product_name", "Unknown Product"),
        "brands": data.get("brands") or enhanced.get("brands", ""),
        "ingredients_text": data.get("ingredients_text") or enhanced.get("ingredients_text", ""),
        "quantity": data.get("quantity", 1),
        "price": data.get("price", 0.0),
        "barcode": data.get("barcode", ""),
        "status": enhanced.get("status", 1),
        "product": enhanced.get("product", {})
    }

    inventory.append(new_item)
    id_counter += 1
    return jsonify(new_item), 201


@app.route('/inventory/<int:item_id>', methods=['PATCH'])
def update_item(item_id):
    item = find_item(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    data = request.get_json()
    item.update(data)
    return jsonify(item), 200


@app.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global inventory
    item = find_item(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    inventory = [i for i in inventory if i["id"] != item_id]
    return jsonify({"message": f"Item {item_id} deleted"}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)
