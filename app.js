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

// 2. Send Items and Fetch Totals
async function fetchInvoiceTotals() {
    const printBtn = $('printInvoiceBtn');
    if (invoiceItems.length === 0) {
        renderTotals({ subtotal: 0, totalGST: 0, grandTotal: 0, taxableValue: 0 });
        renderItems([]);
        printBtn.disabled = true;
        return;
    }
    printBtn.disabled = false;
    showMessage('Calculating totals...', 'loading');
    const payload = { 
        items: invoiceItems.map(item => ({
            itemName: item.name,
            categoryName: item.categoryName,
            itemPrice: item.price,
            itemQty: item.qty,
            id: item.id
        }))
    };
    try {
        const response = await fetch(`${API_BASE_URL}/calculate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const result = await response.json();
        if (!response.ok) {
            throw new Error(result.error || 'Server error during calculation.');
        }
        renderTotals(result.totals);
        renderItems(result.processedItems); 
        showMessage('Calculation successful!', 'success');
    } catch (error) {
        renderTotals({ subtotal: 0, totalGST: 0, grandTotal: 0, taxableValue: 0 });
        showMessage(`Calculation Error: Could not get totals. Details: ${error.message}`, 'error');
    }
}

// --- Rendering & UI Management ---

const renderTotals = (totals) => {
    $('subtotalDisplay').textContent = formatCurrency(totals.subtotal);
    $('totalGSTDisplay').textContent = formatCurrency(totals.totalGST);
    $('taxableValueDisplay').textContent = formatCurrency(totals.taxableValue);
    $('grandTotalDisplay').textContent = formatCurrency(totals.grandTotal);
};

// RenderItems function (with delete button)
const renderItems = (processedItems) => {
     const invoiceItemsTableBody = $('invoiceItemsTableBody');
     
     if (processedItems.length === 0) {
        invoiceItemsTableBody.innerHTML = '<tr><td colspan="7" style="text-align: center; color: var(--text-medium); padding: 2rem 0;">No items added yet.</td></tr>';
        return;
    }

    invoiceItemsTableBody.innerHTML = processedItems.map((item) => {
        const itemId = item.id;
        const gstRate = (item.category && item.category.rate !== undefined) ? item.category.rate : 'N/A';
        
        return `
            <tr data-id="${itemId}">
                <td style="font-weight: 600;">${item.name}</td>
                <td>${item.category ? item.category.name : 'Unknown'}</td>
                <td style="text-align: center;">${item.qty}</td>
                <td>${formatCurrency(item.subtotal)}</td>
                <td style="text-align: center;">${gstRate}%</td>
                <td style="font-weight: 600;">${formatCurrency(item.totalInclGST)}</td>
                <td style="text-align: right;"><button class="btn-delete" data-id="${itemId}">&#10005;</button></td>
            </tr>
        `;
    }).join('');
};

// --- Event Handlers ---

// handleAddItem (FIXED TYPO)
const handleAddItem = () => {
    const name = $('itemName').value.trim();
    const price = parseFloat($('itemPrice').value); 
    const qty = parseInt($('itemQty').value);
    const categorySelect = $('itemCategory');
    
    // === THIS IS THE FIX ===
    const categoryName = categorySelect.options.length > 0 ? categorySelect.options[categorySelect.selectedIndex].value : '';

    if (!name || isNaN(price) || price <= 0 || isNaN(qty) || qty <= 0 || !categoryName) {
        showMessage('Please ensure Item Name, Price (> 0), Quantity (> 0), and Category are selected.', 'error');
        return;
    }

    const newItem = {
        id: generateId(), // <-- Generate a unique ID
        name: name,
        categoryName: categoryName,
        price: price,
        qty: qty
    };
