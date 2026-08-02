# -----------------------------
# Classes
# -----------------------------

class GSTCategory:
    # Class variable (shared by all instances)
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
        # If tax_rate not given, pick from default_rates
        self.name = name
        self.tax_rate = tax_rate if tax_rate is not None else self.default_rates.get(name.lower(), 0)

    @classmethod
    def update_rate(cls, category, new_rate):
        """Update the default tax rate for a category"""
        if category.lower() in cls.default_rates:
            cls.default_rates[category.lower()] = new_rate
            print(f"Updated GST rate for '{category}' to {new_rate}%")
        else:
            print(f"Category '{category}' not found in defaults!")

    @classmethod
    def show_default_rates(cls):
        """Display all current GST default rates"""
        print("\n Current GST Rates:")
        for cat, rate in cls.default_rates.items():
            print(f"- {cat.capitalize()}: {rate}%")

class InvoiceItem:
    def __init__(self, name, category, price, qty):
        self.name = name
        self.category = category
        self.price = price
        self.qty = qty

    def get_total(self):
        subtotal = self.price * self.qty
        tax = subtotal * (self.category.tax_rate / 100)
        return subtotal + tax

