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
