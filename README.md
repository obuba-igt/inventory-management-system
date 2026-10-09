# Inventory Management System

Summative Lab: Python API Consumption and CRUD

## Setup
pip install -r requirements.txt

## Run API
python app.py
Runs on http://127.0.0.1:5000 with debug mode

## Run CLI (in second terminal)
python cli.py

## API Endpoints
- GET /inventory - Fetch all items
- GET /inventory/<id> - Fetch single item
- POST /inventory - Add item (auto-enhances with OpenFoodFacts if barcode or product_name given)
- PATCH /inventory/<id> - Update item
- DELETE /inventory/<id> - Delete item

## OpenFoodFacts Integration
- Barcode: https://world.openfoodfacts.org/api/v0/product/{barcode}.json
- Search: https://world.openfoodfacts.org/cgi/search.pl?search_terms={name}&json=true

Example barcode to test: 737628064502 (Nutella)

## Testing
pytest -v