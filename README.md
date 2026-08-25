# 🏦 Lalit's AI Stock Analyst Agent

An AI-powered financial analyst agent built with ChatGPT that provides stock recommendations, market analysis, and accounting assistance.

## Features

✨ **Stock Analysis**
- Real-time stock data and pricing
- Technical indicators (SMA, RSI)
- Stock recommendations (Buy/Sell/Hold)
- Market trend analysis
- Company fundamental data

💰 **Accounting & Finance**
- Transaction tracking
- Profit & loss calculations
- Expense categorization
- Financial ratio analysis
- Tax estimation

🤖 **AI Agent**
- Powered by ChatGPT (GPT-4)
- Natural language conversation
- Multi-turn dialogue
- Tool integration for real data

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/lalitlife/lalit-ai.git
cd lalit-ai
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Setup environment variables**
```bash
cp .env.example .env
# Edit .env and add your API keys
```

4. **Add your API keys to .env**
```
OPENAI_API_KEY=your_openai_key_here
ALPHA_VANTAGE_KEY=your_alpha_vantage_key_here
MODEL=gpt-4
```

## Usage

### Command Line Interface

```bash
python finance_agent.py
```

Then type your questions:
```
📊 You: What's your recommendation for Apple stock (AAPL)?
💡 Agent: Based on technical analysis...
```

### Web Interface

```bash
python app.py
```

Open your browser to `http://localhost:5000`

### Python API

```python
from finance_agent import FinanceAIAgent

agent = FinanceAIAgent()
response = agent.chat("What's your recommendation for TESLA?")
print(response)
```

## Example Queries

### Stock Analysis
- "What's the current price of Apple stock?"
- "Should I buy Tesla stock now?"
- "Analyze the technical indicators for Microsoft"
- "Compare Amazon and Google stocks"

### Accounting
- "Calculate my profit and loss"
- "What are my expenses by category?"
- "Estimate my tax liability for $100,000 income"

## API Keys Required

1. **OpenAI API Key** (Required)
   - Get it from: https://platform.openai.com/api-keys
   - Required for ChatGPT integration

2. **Alpha Vantage API Key** (Optional)
   - Get it from: https://www.alphavantage.co/api/
   - For advanced stock data features

## Project Structure

```
lalit-ai/
├── finance_agent.py      # Main AI agent
├── stock_data.py         # Stock data fetcher & analysis
├── accounting.py         # Accounting calculations
├── app.py               # Flask web application
├── config.py            # Configuration settings
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
└── README.md           # This file
```

## Configuration

Edit `config.py` to customize:
- Model (gpt-4, gpt-3.5-turbo)
- Temperature (0.0-1.0)
- Max tokens
- Financial thresholds

## Disclaimer

⚠️ **Important**: This AI agent provides analysis for informational purposes only. It should NOT be used as a substitute for professional financial advice. Always consult with a qualified financial advisor before making investment decisions.

## Technologies Used

- **AI Model**: OpenAI GPT-4
- **Data**: yfinance, Alpha Vantage
- **Web Framework**: Flask
- **Data Processing**: Pandas, NumPy
- **Technical Analysis**: TA-Lib

## Future Enhancements

- [ ] Portfolio management
- [ ] Real-time alerts
- [ ] Machine learning predictions
- [ ] Options trading analysis
- [ ] Cryptocurrency support
- [ ] Database integration
- [ ] Mobile app

## License

MIT License - see LICENSE file for details

## Support

For issues or feature requests, please open an issue on GitHub.

## Author

Lalit - AI Financial Analyst Agent

---

⭐ If you find this project helpful, please give it a star!
