// Tab Navigation
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        
        // Remove active class from all links
        document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
        link.classList.add('active');
        
        // Hide all tab contents
        document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
        
        // Show selected tab
        const tabId = link.dataset.tab;
        document.getElementById(tabId).classList.add('active');
    });
});

// Chat Functionality
const chatMessages = document.getElementById('chatMessages');
const chatForm = document.getElementById('chatForm');
const chatInput = document.getElementById('chatInput');

function handleChatSubmit(event) {
    event.preventDefault();
    
    const message = chatInput.value.trim();
    if (!message) return;
    
    // Add user message to chat
    addMessage(message, 'user');
    chatInput.value = '';
    
    // Send to backend
    sendMessage(message);
}

function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = text;
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function sendMessage(message) {
    // Add loading indicator
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'message assistant';
    loadingDiv.innerHTML = '<div class="message-content"><span class="loading"></span></div>';
    chatMessages.appendChild(loadingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    // Send to backend
    fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        // Remove loading indicator
        loadingDiv.remove();
        
        // Add assistant response
        if (data.success) {
            addMessage(data.response, 'assistant');
        } else {
            addMessage('Sorry, I encountered an error. Please try again.', 'assistant');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        loadingDiv.remove();
        addMessage('Connection error. Please check your internet and try again.', 'assistant');
    });
}

// Stock Analysis
function analyzeStock() {
    const symbol = document.getElementById('stockSymbol').value.trim().toUpperCase();
    
    if (!symbol) {
        alert('Please enter a stock symbol');
        return;
    }
    
    const resultsContainer = document.getElementById('stockResults');
    resultsContainer.innerHTML = '<div class="loading"></div>';
    
    fetch('/api/analyze-stock', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ symbol: symbol })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            displayStockResults(data.data);
        } else {
            resultsContainer.innerHTML = `<p style="color: var(--danger-color);">Error: ${data.message}</p>`;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        resultsContainer.innerHTML = '<p style="color: var(--danger-color);">Failed to fetch stock data</p>';
    });
}

function displayStockResults(data) {
    const resultsContainer = document.getElementById('stockResults');
    
    let html = `
        <div class="card">
            <h4>${data.symbol} - ${data.name}</h4>
            <p><strong>Current Price:</strong> $${data.price}</p>
            <p><strong>Change:</strong> ${data.change}%</p>
            <p><strong>Market Cap:</strong> ${data.market_cap}</p>
            <p><strong>Recommendation:</strong> <span style="color: ${data.recommendation === 'Buy' ? 'var(--success-color)' : data.recommendation === 'Sell' ? 'var(--danger-color)' : 'var(--warning-color)'}">${data.recommendation}</span></p>
            <p><strong>Analysis:</strong> ${data.analysis}</p>
        </div>
    `;
    
    resultsContainer.innerHTML = html;
}

// Transaction Form
document.getElementById('transactionForm').addEventListener('submit', (e) => {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    
    fetch('/api/add-transaction', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            description: formData.get('description'),
            amount: parseFloat(formData.get('amount')),
            type: formData.get('type')
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            e.target.reset();
            updateFinancialSummary();
        }
    });
});

function updateFinancialSummary() {
    fetch('/api/financial-summary')
        .then(response => response.json())
        .then(data => {
            const summary = document.getElementById('financialSummary');
            summary.innerHTML = `
                <p>Total Income: $${data.income.toFixed(2)}</p>
                <p>Total Expenses: $${data.expenses.toFixed(2)}</p>
                <p>Net Profit/Loss: $${(data.income - data.expenses).toFixed(2)}</p>
            `;
        });
}

// Portfolio Form
document.getElementById('portfolioForm').addEventListener('submit', (e) => {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    
    fetch('/api/add-portfolio-item', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            symbol: formData.get('symbol'),
            quantity: parseInt(formData.get('quantity')),
            purchase_price: parseFloat(formData.get('purchase_price'))
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            e.target.reset();
            updatePortfolioList();
        }
    });
});

function updatePortfolioList() {
    fetch('/api/portfolio-list')
        .then(response => response.json())
        .then(data => {
            const portfolioList = document.getElementById('portfolioList');
            
            if (data.holdings.length === 0) {
                portfolioList.innerHTML = '<p>No holdings yet</p>';
                return;
            }
            
            let html = '<table style="width: 100%; border-collapse: collapse;">';
            html += '<tr style="border-bottom: 1px solid var(--border-color);"><th style="text-align: left; padding: 8px;">Symbol</th><th style="text-align: left; padding: 8px;">Qty</th><th style="text-align: left; padding: 8px;">Current Price</th><th style="text-align: left; padding: 8px;">Gain/Loss</th></tr>';
            
            data.holdings.forEach(holding => {
                const gainLoss = ((holding.current_price - holding.purchase_price) * holding.quantity).toFixed(2);
                const gainLossPercent = (((holding.current_price - holding.purchase_price) / holding.purchase_price) * 100).toFixed(2);
                const color = gainLoss >= 0 ? 'var(--success-color)' : 'var(--danger-color)';
                
                html += `<tr style="border-bottom: 1px solid var(--border-color);">
                    <td style="padding: 8px; font-weight: 600;">${holding.symbol}</td>
                    <td style="padding: 8px;">${holding.quantity}</td>
                    <td style="padding: 8px;">$${holding.current_price.toFixed(2)}</td>
                    <td style="padding: 8px; color: ${color};">$${gainLoss} (${gainLossPercent}%)</td>
                </tr>`;
            });
            
            html += '</table>';
            portfolioList.innerHTML = html;
        });
}

// Clear Chat History
document.querySelector('.clear-history').addEventListener('click', (e) => {
    e.preventDefault();
    
    if (confirm('Are you sure you want to clear chat history?')) {
        chatMessages.innerHTML = `
            <div class="welcome-message">
                <h3>Welcome to Lalit AI</h3>
                <p>Your AI-powered financial analyst is ready to help!</p>
                <div class="quick-prompts">
                    <button class="quick-prompt" onclick="sendMessage('What are today\\'s top stock movers?')">
                        📊 Top Movers
                    </button>
                    <button class="quick-prompt" onclick="sendMessage('Analyze Apple (AAPL) stock')">
                        🍎 AAPL Analysis
                    </button>
                    <button class="quick-prompt" onclick="sendMessage('What\\'s the market sentiment today?')">
                        📈 Market Sentiment
                    </button>
                </div>
            </div>
        `;
    }
});

// Settings
document.getElementById('modelSelect').addEventListener('change', (e) => {
    // Save settings
    localStorage.setItem('model', e.target.value);
});

document.getElementById('themeSelect').addEventListener('change', (e) => {
    const theme = e.target.value.toLowerCase();
    localStorage.setItem('theme', theme);
    applyTheme(theme);
});

document.querySelectorAll('.setting-item input[type="range"]').forEach(slider => {
    slider.addEventListener('input', (e) => {
        const value = e.target.value;
        document.getElementById('tempValue').textContent = value;
        localStorage.setItem('temperature', value);
    });
});

function applyTheme(theme) {
    if (theme === 'light') {
        document.documentElement.style.colorScheme = 'light';
    } else {
        document.documentElement.style.colorScheme = 'dark';
    }
}

// Load settings on page load
document.addEventListener('DOMContentLoaded', () => {
    const savedModel = localStorage.getItem('model');
    const savedTheme = localStorage.getItem('theme');
    const savedTemp = localStorage.getItem('temperature');
    
    if (savedModel) document.getElementById('modelSelect').value = savedModel;
    if (savedTheme) {
        document.getElementById('themeSelect').value = savedTheme.charAt(0).toUpperCase() + savedTheme.slice(1);
        applyTheme(savedTheme);
    }
    if (savedTemp) {
        document.querySelectorAll('.setting-item input[type="range"]')[0].value = savedTemp;
        document.getElementById('tempValue').textContent = savedTemp;
    }
    
    // Load initial data
    updateFinancialSummary();
    updatePortfolioList();
});

// Mobile Sidebar Toggle
const toggleBtn = document.querySelector('.toggle-sidebar');
if (toggleBtn) {
    toggleBtn.addEventListener('click', () => {
        document.querySelector('.sidebar').classList.toggle('open');
    });
    
    // Close sidebar when a link is clicked
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => {
            document.querySelector('.sidebar').classList.remove('open');
        });
    });
}
