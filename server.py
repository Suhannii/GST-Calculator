from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

# ----------------------------------------------------
# 1. Core GST Calculation Logic (From your main.py)
# ----------------------------------------------------

class GSTCategory:
    default_rates = {
        "essential goods": 0,
        "clothing & footwear": 10,
        "food items": 5,
        "electronics": 18,
        "luxury goods": 28,
        "education": 0,
        "healthcare": 5,
        "automobile": 28,
        "entertainment services": 22,
        "personal care products": 5
        
    }

    def __init__(self, name, tax_rate=None):
        self.name = name
        # Ensures rate is pulled from defaults if not specified
        self.tax_rate = tax_rate if tax_rate is not None else self.default_rates.get(name.lower(), 0)
        
    @classmethod
    def get_category_data(cls, name):
        """Returns category name and rate for the API."""
        rate = cls.default_rates.get(name.lower())
        if rate is not None:
            return {"name": name.capitalize(), "rate": rate}
        return None

    @classmethod
    def get_all_categories(cls):
        """Returns a list of all category names and rates."""
        # We sort this so the list is always predictable
        sorted_items = sorted(cls.default_rates.items())
        return [{"name": name.capitalize(), "rate": rate} for name, rate in sorted_items]

class InvoiceItem:
    # --- ADDED 'item_id' ---
    def __init__(self, name, category, price, qty, item_id):
        self.name = name
        self.category = category  # Dictionary: {"name": str, "rate": int}
        self.price = float(price) # Unit price (Excl. GST)
        self.qty = int(qty)
        self.id = item_id # Store the unique ID from the frontend

    @property
    def subtotal(self):
        """Total price of this item (Excl. GST)"""
        return self.price * self.qty

    @property
    def total_gst(self):
        """Total GST amount for this item"""
        return self.subtotal * (self.category['rate'] / 100)

    @property
    def total_incl_gst(self):
        """Total price of this item (Incl. GST)"""
        return self.subtotal + self.total_gst

    def to_dict(self):
        return {
            'id': self.id, # --- PASS THE ID BACK ---
            'name': self.name,
            'category': self.category,
            'qty': self.qty,
            'subtotal': round(self.subtotal, 2),
            'totalInclGST': round(self.total_incl_gst, 2)
        }

class Invoice:
    def __init__(self, items_data):
        self.items = []
        for item_data in items_data:
            category_data = GSTCategory.get_category_data(item_data['categoryName'])
            if category_data:
                # Ensure 'id' is passed; default to None if not present
                item_id = item_data.get('id', None) 
                item = InvoiceItem(
                    item_data['itemName'],
                    category_data,
                    item_data['itemPrice'],
                    item_data['itemQty'],
                    item_id # --- PASS THE ID ---
                )
                self.items.append(item)

    @property
    def totals(self):
        subtotal = sum(item.subtotal for item in self.items)
        total_gst = sum(item.total_gst for item in self.items)
        grand_total = sum(item.total_incl_gst for item in self.items)

        return {
            "subtotal": round(subtotal, 2),
            "totalGST": round(total_gst, 2),
            "grandTotal": round(grand_total, 2),
            "taxableValue": round(subtotal, 2) # Same as subtotal in this context
        }

# ----------------------------------------------------
# 2. Flask API Setup
# ----------------------------------------------------

app = Flask(__name__)
# Enable CORS for development so the frontend can talk to the backend
CORS(app)

@app.route('/')
def index():
    """Serve the frontend."""
    return send_from_directory(os.path.dirname(__file__), 'index.html')

@app.route('/categories', methods=['GET'])
def get_categories():
    """Endpoint to fetch all GST categories and rates for the dropdown."""
    return jsonify(GSTCategory.get_all_categories())

# === NEW FEATURE: Add Category Endpoint ===
@app.route('/add-category', methods=['POST'])
def add_category():
    """Endpoint to add a new dynamic category."""
    data = request.get_json()
    name = data.get('name')
    rate = data.get('rate')

    if name and rate is not None:
        try:
            # Add to the *in-memory* dictionary
            GSTCategory.default_rates[name.lower()] = int(rate)
            return jsonify({"message": "Category added successfully"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400
            
    return jsonify({"error": "Invalid data, 'name' and 'rate' are required."}), 400
# === END OF NEW FEATURE ===


