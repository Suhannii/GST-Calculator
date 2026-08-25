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

// --- Core API Interaction ---

// 1. Fetch Categories
async function fetchCategories() {
    showMessage('Attempting to connect to Python server...', 'loading');
    try {
        let response = null;
        const maxRetries = 3;
        let delay = 1000; 
        for (let i = 0; i < maxRetries; i++) {
            try {
                response = await fetch(`${API_BASE_URL}/categories`);
                if (response.ok) break;
            } catch (e) {
                if (i < maxRetries - 1) {
                    await new Promise(resolve => setTimeout(resolve, delay));
                    delay *= 2; 
                } else {
                    throw e; 
                }
            }
        }
        if (!response || !response.ok) throw new Error('Failed to fetch categories after multiple retries.');
        const categories = await response.json();
        const categorySelect = $('itemCategory');
        const currentVal = categorySelect.value; // Save current selection
        
        categorySelect.innerHTML = categories.map(cat => 
            `<option value="${cat.name}">${cat.name} (${cat.rate}%)</option>`
        ).join('');
        
        // Try to restore previous selection, or default to first
        const matchingOption = categories.find(cat => cat.name === currentVal);
        if (matchingOption) {
            categorySelect.value = currentVal;
        } else {
            categorySelect.value = categories.length > 0 ? categories[0].name : '';
        }
        showMessage('Server connected! Categories loaded.', 'success');
        
    } catch (error) {
        showMessage(`CRITICAL ERROR: Could not connect to Python backend at ${API_BASE_URL}. Please ensure 'server.py' is running.`, 'error');
    }
}
