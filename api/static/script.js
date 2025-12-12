const API_URL = '/predict';
const WINDOW_SIZE = 30;

// Initialize the UI
document.addEventListener('DOMContentLoaded', function() {
    initializeInputs();
    setupEventListeners();
});

function initializeInputs() {
    const container = document.getElementById('dataInputs');
    container.innerHTML = '';
    
    for (let i = 0; i < WINDOW_SIZE; i++) {
        const item = document.createElement('div');
        item.className = 'data-input-item';
        
        const label = document.createElement('label');
        label.textContent = `Day ${i + 1}`;
        
        const input = document.createElement('input');
        input.type = 'number';
        input.step = '0.01';
        input.min = '0';
        input.placeholder = '0';
        input.id = `input-${i}`;
        input.addEventListener('input', validateInputs);
        
        item.appendChild(label);
        item.appendChild(input);
        container.appendChild(item);
    }
    
    updateInputCount();
}

function setupEventListeners() {
    document.getElementById('predictBtn').addEventListener('click', makePrediction);
    document.getElementById('loadSampleBtn').addEventListener('click', loadSampleData);
    document.getElementById('clearBtn').addEventListener('click', clearAll);
    document.getElementById('csvFile').addEventListener('change', handleCSVUpload);
}

function validateInputs() {
    const inputs = document.querySelectorAll('#dataInputs input');
    let filledCount = 0;
    
    inputs.forEach(input => {
        if (input.value && input.value.trim() !== '') {
            filledCount++;
        }
    });
    
    updateInputCount(filledCount);
    
    const predictBtn = document.getElementById('predictBtn');
    predictBtn.disabled = filledCount !== WINDOW_SIZE;
}

function updateInputCount(count = null) {
    if (count === null) {
        const inputs = document.querySelectorAll('#dataInputs input');
        count = Array.from(inputs).filter(input => input.value && input.value.trim() !== '').length;
    }
    
    const countElement = document.getElementById('inputCount');
    countElement.textContent = count;
    countElement.style.color = count === WINDOW_SIZE ? '#28a745' : count > 0 ? '#ffc107' : '#666';
}

function getInputValues() {
    const inputs = document.querySelectorAll('#dataInputs input');
    const values = [];
    
    inputs.forEach(input => {
        const value = parseFloat(input.value);
        if (isNaN(value)) {
            throw new Error('Please fill all 30 fields with valid numbers');
        }
        values.push(value);
    });
    
    if (values.length !== WINDOW_SIZE) {
        throw new Error('Please fill all 30 fields');
    }
    
    return values;
}

async function makePrediction() {
    const predictBtn = document.getElementById('predictBtn');
    const predictBtnText = document.getElementById('predictBtnText');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const resultSection = document.getElementById('resultSection');
    const errorSection = document.getElementById('errorSection');
    
    // Hide previous results/errors
    resultSection.style.display = 'none';
    errorSection.style.display = 'none';
    
    try {
        // Get and validate input values
        const values = getInputValues();
        
        // Show loading state
        predictBtn.disabled = true;
        predictBtnText.textContent = 'Predicting...';
        loadingSpinner.style.display = 'inline-block';
        
        // Make API call
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                new_cases: values
            })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to get prediction');
        }
        
        const data = await response.json();
        
        // Display result
        document.getElementById('predictedValue').textContent = Math.round(data.predicted_cases).toLocaleString();
        document.getElementById('resultMessage').textContent = data.message;
        resultSection.style.display = 'block';
        
        // Scroll to result
        resultSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        
    } catch (error) {
        // Display error
        document.getElementById('errorMessage').textContent = error.message;
        errorSection.style.display = 'block';
        errorSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } finally {
        // Reset button state
        predictBtn.disabled = false;
        predictBtnText.textContent = 'Make Prediction';
        loadingSpinner.style.display = 'none';
    }
}

function loadSampleData() {
    // Generate sample data (trending upward)
    const inputs = document.querySelectorAll('#dataInputs input');
    let baseValue = 100;
    
    inputs.forEach((input, index) => {
        // Create a trend with some variation
        const value = baseValue + (index * 5) + Math.random() * 20;
        input.value = Math.round(value);
    });
    
    validateInputs();
}

function clearAll() {
    const inputs = document.querySelectorAll('#dataInputs input');
    inputs.forEach(input => {
        input.value = '';
    });
    validateInputs();
    
    document.getElementById('resultSection').style.display = 'none';
    document.getElementById('errorSection').style.display = 'none';
}

function handleCSVUpload(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    const reader = new FileReader();
    reader.onload = function(e) {
        try {
            const text = e.target.result;
            const lines = text.split('\n');
            
            // Try to find the new_cases column
            let newCasesIndex = -1;
            let dataStartIndex = 0;
            
            // Check if first line is header
            const header = lines[0].toLowerCase();
            if (header.includes('new_cases') || header.includes('new cases')) {
                const headers = lines[0].split(',');
                newCasesIndex = headers.findIndex(h => 
                    h.toLowerCase().includes('new') && h.toLowerCase().includes('case')
                );
                dataStartIndex = 1;
            }
            
            if (newCasesIndex === -1) {
                // Assume first column is new_cases
                newCasesIndex = 0;
            }
            
            const values = [];
            for (let i = dataStartIndex; i < lines.length && values.length < WINDOW_SIZE; i++) {
                if (lines[i].trim() === '') continue;
                const columns = lines[i].split(',');
                const value = parseFloat(columns[newCasesIndex]);
                if (!isNaN(value)) {
                    values.push(value);
                }
            }
            
            if (values.length < WINDOW_SIZE) {
                throw new Error(`CSV file must contain at least ${WINDOW_SIZE} valid values. Found ${values.length}.`);
            }
            
            // Take the last 30 values
            const last30Values = values.slice(-WINDOW_SIZE);
            
            // Fill inputs
            const inputs = document.querySelectorAll('#dataInputs input');
            last30Values.forEach((value, index) => {
                if (inputs[index]) {
                    inputs[index].value = value;
                }
            });
            
            validateInputs();
            
            // Show success message
            alert(`Successfully loaded ${WINDOW_SIZE} values from CSV file!`);
            
        } catch (error) {
            alert('Error reading CSV file: ' + error.message);
        }
    };
    
    reader.readAsText(file);
    
    // Reset file input
    event.target.value = '';
}

