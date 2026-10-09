import requests


def fetch_from_openfoodfacts(barcode=None, product_name=None):
    """
    Task 3 Step 3: Fetch Data
    Queries OpenFoodFacts API using barcode or product name
    """
    try:
        if barcode:
            url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            if data.get("status") == 1 and data.get("product"):
                p = data["product"]
                return {
                    "status": 1,
                    "product_name": p.get("product_name", ""),
                    "brands": p.get("brands", ""),
                    "ingredients_text": p.get("ingredients_text", ""),
                    "product": p
                }
            return {"status": 0, "product_name": "", "brands": "", "ingredients_text": "", "product": {}}

        if product_name:
            url = "https://world.openfoodfacts.org/cgi/search.pl"
            params = {"search_terms": product_name,
                      "json": True, "page_size": 1}
            resp = requests.get(url, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            products = data.get("products", [])
            if products:
                p = products[0]
                return {
                    "status": 1,
                    "product_name": p.get("product_name", product_name),
                    "brands": p.get("brands", ""),
                    "ingredients_text": p.get("ingredients_text", ""),
                    "product": p
                }
            return {"status": 0, "product_name": product_name, "brands": "", "ingredients_text": "", "product": {}}

    except requests.exceptions.RequestException as e:
        print(f"[OpenFoodFacts Error] {e}")
        return {"status": 0, "product_name": product_name or "", "brands": "", "ingredients_text": "", "product": {}, "error": str(e)}

    return {"status": 0, "product_name": "", "brands": "", "ingredients_text": "", "product": {}}
