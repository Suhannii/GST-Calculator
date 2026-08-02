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
        

class Invoice:
    invoice_counter = 1000  # class variable for unique IDs

    def __init__(self, customer_name, phone=None, email=None, address=None):
        self.customer_name = customer_name
        self.phone = phone or "Not Provided"
        self.email = email or "Not Provided"
        self.address = address or "Not Provided"
        self.items = []
        Invoice.invoice_counter += 1
        self.invoice_id = f"INV-{Invoice.invoice_counter}"

    def add_item(self, item):
        self.items.append(item)

    def show_invoice(self):
        import datetime
        print("\n" + "=" * 55)
        print(f"INVOICE — {self.invoice_id}")
        print("=" * 55)
        print(f"Customer Name : {self.customer_name}")
        print(f"Phone Number  : {self.phone}")
        print(f"Email         : {self.email}")
        print(f"Address       : {self.address}")
        print(f"Date          : {datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
        print("-" * 55)
        print(f"{'Item':20} {'Category':10} {'Qty':5} {'Total (₹)':>10}")
        print("-" * 55)

        total = 0
        for item in self.items:
            item_total = item.get_total()
            total += item_total
            print(f"{item.name:20} {item.category.name:10} {item.qty:<5} {item_total:>10.2f}")

        print("-" * 55)
        print(f"{'Grand Total':35} ₹{total:.2f}")
        print("=" * 55)class GSTSystem:
    def __init__(self):
        self.categories = {}

    def add_category(self, name, tax_rate=None):
        """Add a category — uses default rate if not provided"""
        self.categories[name.lower()] = GSTCategory(name, tax_rate)

    def show_categories(self):
        print("\nAvailable categories:")
        for name, cat in self.categories.items():
            print(f"- {cat.name} ({cat.tax_rate}% GST)")

    def get_category(self, name):
        return self.categories.get(name.lower(), None)
        

class GSTSystem:
    def __init__(self):
        self.categories = {}

    def add_category(self, name, tax_rate=None):
        """Add a category — uses default rate if not provided"""
        self.categories[name.lower()] = GSTCategory(name, tax_rate)

    def show_categories(self):
        print("\nAvailable categories:")
        for name, cat in self.categories.items():
            print(f"- {cat.name} ({cat.tax_rate}% GST)")

    def get_category(self, name):
        return self.categories.get(name.lower(), None)
        

if __name__ == "__main__":
    gst_system = GSTSystem()

    # Load default categories
    for cat in GSTCategory.default_rates.keys():
        gst_system.add_category(cat)

    print("Welcome to the Dynamic GST Billing System 💼")

    # Step 1: Customer Details (Optional Inputs)
    name = input("\nEnter customer name: ").strip()
    while not name:
        name = input("Customer name cannot be empty. Please enter again: ").strip()

    phone = input("Enter phone number (optional): ").strip() or None
    email = input("Enter email (optional): ").strip() or None
    address = input("Enter address (optional): ").strip() or None

    invoice = Invoice(name, phone, email, address)

    # Step 2: Item Input
    gst_system.show_categories()

    while True:
        item_name = input("\nEnter item name (or 'done' to finish): ").strip()
        if item_name.lower() == 'done':
            break
        if not item_name:
            print("⚠️ Item name cannot be empty!")
            continue

        category_name = input("Enter category: ").strip().lower()
        category = gst_system.get_category(category_name)
        if not category:
            print("⚠️ Invalid category. Try again.")
            continue

        try:
            price = float(input("Enter item price (₹): "))
            qty = int(input("Enter quantity: "))
        except ValueError:
            print("⚠️ Invalid input! Please enter numeric values for price and quantity.")
            continue

        invoice.add_item(InvoiceItem(item_name, category, price, qty))

    # Step 3: Display final invoice
    if invoice.items:
        invoice.show_invoice()
    else:
        print("\n⚠️ No items added. Invoice not generated.")
