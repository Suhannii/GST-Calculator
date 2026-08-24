// CRITICAL NOTE: This app requires the Python Flask server (server.py) to be running 
// in your terminal on port 5000 before the categories and calculations will work.

// --- Configuration ---
const API_BASE_URL = 'http://127.0.0.1:5000'; 

// --- App State ---
let invoiceItems = [];
let invoiceIdCounter = 0;
let invoiceId = 'INV-0000';

// --- Utility Functions ---
const $ = (id) => document.getElementById(id);
const formatCurrency = (amount) => `₹${parseFloat(amount).toFixed(2)}`;
const generateId = () => crypto.randomUUID();
