import requests
import json

BASE_URL = "http://127.0.0.1:5000"


def cli():
    print("=== Inventory Management CLI ===")
    print("Make sure Flask API is running: python app.py in another terminal")
    while True:
        print("\n1. View all items [GET /inventory]")
        print("2. View single item [GET /inventory/<id>]")
        print("3. Add new item [POST /inventory]")
        print("4. Update item [PATCH /inventory/<id>]")
        print("5. Delete item [DELETE /inventory/<id>]")
        print("6. Exit")
        choice = input("Enter choice 1-6: ").strip()

        try:
            if choice == "1":
                r = requests.get(f"{BASE_URL}/inventory")
                print(json.dumps(r.json(), indent=2))

            elif choice == "2":
                iid = input("Enter ID: ").strip()
                r = requests.get(f"{BASE_URL}/inventory/{iid}")
                print(json.dumps(r.json(), indent=2))

            elif choice == "3":
                print(
                    "Add item - if you enter barcode, it will auto-fetch from OpenFoodFacts")
                barcode = input(
                    "Barcode (e.g. 737628064502 for Nutella) or leave blank: ").strip()
                product_name = input("Product name (if no barcode): ").strip()
                quantity = input("Quantity [1]: ").strip() or "1"
                price = input("Price [0.0]: ").strip() or "0.0"
                payload = {
                    "product_name": product_name,
                    "barcode": barcode,
                    "quantity": int(quantity),
                    "price": float(price)
                }
                r = requests.post(f"{BASE_URL}/inventory", json=payload)
                print(f"Status {r.status_code}:")
                print(json.dumps(r.json(), indent=2))

            elif choice == "4":
                iid = input("ID to update: ").strip()
                field = input(
                    "Field to update (quantity, price, product_name, brands): ").strip()
                value = input(f"New value for {field}: ").strip()
                if field == "quantity":
                    value = int(value)
                if field == "price":
                    value = float(value)
                r = requests.patch(
                    f"{BASE_URL}/inventory/{iid}", json={field: value})
                print(json.dumps(r.json(), indent=2))

            elif choice == "5":
                iid = input("ID to delete: ").strip()
                r = requests.delete(f"{BASE_URL}/inventory/{iid}")
                print(json.dumps(r.json(), indent=2))

            elif choice == "6":
                print("Bye!")
                break
            else:
                print("Invalid choice")

        except requests.exceptions.ConnectionError:
            print(
                "ERROR: Flask API not running. Run 'python app.py' first in another terminal!")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    cli()
