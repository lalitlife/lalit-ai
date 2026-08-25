"""
Updated Flask application with web interface and API endpoints
"""
from flask import Flask, render_template, request, jsonify
from finance_agent import FinanceAIAgent
from stock_data import StockAnalyzer
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder='templates', static_folder='static')
agent = FinanceAIAgent()
stock_analyzer = StockAnalyzer()

# In-memory storage for demo purposes
transactions = []
portfolio = {}

# ============ Web Interface Routes ============

@app.route('/')
def index():
    """Render main web interface"""
    return render_template('index.html')

# ============ Chat API Endpoints ============

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.json
        message = data.get('message', '')
        
        if not message:
            return jsonify({'success': False, 'message': 'Empty message'}), 400
        
        # Get response from AI agent
        response = agent.chat(message)
        
        return jsonify({
            'success': True,
            'response': response,
            'message': message
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# ============ Stock Analysis API ============

@app.route('/api/analyze-stock', methods=['POST'])
def analyze_stock():
    """Analyze a stock and return results"""
    try:
        data = request.json
        symbol = data.get('symbol', '').upper()
        
        if not symbol:
            return jsonify({'success': False, 'message': 'Symbol required'}), 400
        
        # Get stock data
        stock_data = stock_analyzer.get_stock_data(symbol)
        
        if not stock_data:
            return jsonify({'success': False, 'message': 'Stock not found'}), 404
        
        # Get AI analysis
        analysis = agent.analyze_stock(symbol)
        
        return jsonify({
            'success': True,
            'data': {
                'symbol': symbol,
                'name': stock_data.get('name', symbol),
                'price': stock_data.get('price', 0),
                'change': stock_data.get('change', 0),
                'market_cap': stock_data.get('market_cap', 'N/A'),
                'recommendation': analysis.get('recommendation', 'Hold'),
                'analysis': analysis.get('analysis', 'No analysis available')
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# ============ Accounting API ============

@app.route('/api/add-transaction', methods=['POST'])
def add_transaction():
    """Add a financial transaction"""
    try:
        data = request.json
        transaction = {
            'description': data.get('description', ''),
            'amount': float(data.get('amount', 0)),
            'type': data.get('type', 'expense')
        }
        
        transactions.append(transaction)
        
        return jsonify({'success': True, 'message': 'Transaction added'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/financial-summary', methods=['GET'])
def financial_summary():
    """Get financial summary"""
    income = sum(t['amount'] for t in transactions if t['type'] == 'income')
    expenses = sum(t['amount'] for t in transactions if t['type'] == 'expense')
    
    return jsonify({
        'income': income,
        'expenses': expenses,
        'net': income - expenses,
        'transaction_count': len(transactions)
    })

# ============ Portfolio API ============

@app.route('/api/add-portfolio-item', methods=['POST'])
def add_portfolio_item():
    """Add item to portfolio"""
    try:
        data = request.json
        symbol = data.get('symbol', '').upper()
        quantity = int(data.get('quantity', 0))
        purchase_price = float(data.get('purchase_price', 0))
        
        if symbol in portfolio:
            portfolio[symbol]['quantity'] += quantity
        else:
            portfolio[symbol] = {
                'quantity': quantity,
                'purchase_price': purchase_price
            }
        
        return jsonify({'success': True, 'message': 'Added to portfolio'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/portfolio-list', methods=['GET'])
def portfolio_list():
    """Get portfolio holdings"""
    holdings = []
    
    for symbol, data in portfolio.items():
        try:
            current_price = stock_analyzer.get_current_price(symbol)
            holdings.append({
                'symbol': symbol,
                'quantity': data['quantity'],
                'purchase_price': data['purchase_price'],
                'current_price': current_price,
                'total_value': current_price * data['quantity']
            })
        except:
            holdings.append({
                'symbol': symbol,
                'quantity': data['quantity'],
                'purchase_price': data['purchase_price'],
                'current_price': data['purchase_price'],
                'total_value': data['purchase_price'] * data['quantity']
            })
    
    return jsonify({'holdings': holdings})

# ============ Error Handlers ============

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'success': False, 'message': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({'success': False, 'message': 'Server error'}), 500

# ============ Development Server ============

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    print(f"""
    ╔══════════════════════════════════════╗
    ║  Lalit AI - Financial Analyst Agent  ║
    ║                                      ║
    ║  🌐 Web Interface: http://localhost:{port}
    ║  📊 Ready for stock analysis!        ║
    ╚══════════════════════════════════════╝
    """)
    
    app.run(host='0.0.0.0', port=port, debug=debug)
