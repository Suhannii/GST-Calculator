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

/**
 * UPDATED: showMessage now supports 'success', 'error', or 'loading'
 * type: 'success', 'error', 'loading'
 */
function showMessage(message, type = 'loading') {
    const box = $('messageBox');
    box.textContent = message;
    box.style.display = 'block';
    
    box.classList.remove('msg-loading', 'msg-error', 'msg-success');

    if (type === 'success') {
        box.classList.add('msg-success');
    } else if (type === 'error') {
        box.classList.add('msg-error');
    } else {
        box.classList.add('msg-loading');
    }

    // Auto-hide success and loading messages, but not errors
    if (type !== 'error') {
        setTimeout(() => {
            box.style.display = 'none';
        }, 3000);
    }
}
