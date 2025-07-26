// JavaScript for Linq-AcmeCRM Integration Demo

const API_BASE_URL = 'http://127.0.0.1:8200';

// Handle create contact form submission
document.getElementById('createContactForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const contactData = {
        firstName: formData.get('firstName'),
        lastName: formData.get('lastName'),
        email: formData.get('email'),
        phone: formData.get('phone') || null,
        company: formData.get('company') || null,
        notes: formData.get('notes') || null
    };
    
    const token = formData.get('token');
    
    try {
        const response = await fetch(`${API_BASE_URL}/contacts`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(contactData)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            displayResult('createResult', 'success', JSON.stringify(result, null, 2));
            e.target.reset();
        } else {
            displayResult('createResult', 'error', `Error: ${response.status}\n${JSON.stringify(result, null, 2)}`);
        }
    } catch (error) {
        displayResult('createResult', 'error', `Network Error: ${error.message}`);
    }
});

// Get all contacts
async function getContacts() {
    const token = document.getElementById('getToken').value;
    
    if (!token) {
        displayResult('contactsResult', 'error', 'Please select a JWT token');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/contacts`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        const result = await response.json();
        
        if (response.ok) {
            displayResult('contactsResult', 'success', JSON.stringify(result, null, 2));
        } else {
            displayResult('contactsResult', 'error', `Error: ${response.status}\n${JSON.stringify(result, null, 2)}`);
        }
    } catch (error) {
        displayResult('contactsResult', 'error', `Network Error: ${error.message}`);
    }
}

// Display result in formatted JSON
function displayResult(elementId, type, message) {
    const element = document.getElementById(elementId);
    element.textContent = message;
    element.className = `result ${type}`;
}

// Auto-populate tokens for convenience
document.addEventListener('DOMContentLoaded', () => {
    const tokenSelects = document.querySelectorAll('select[name="token"], select[name="getToken"]');
    tokenSelects.forEach(select => {
        select.value = 'linq-demo-token';
    });
});
