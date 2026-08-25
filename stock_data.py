"""
Stock Data Module - Fetch and process financial data
"""
import yfinance as yf
import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json

class StockDataFetcher:
    """Fetch and analyze stock market data"""
    
    def __init__(self):
        self.cache = {}
    
    def get_stock_info(self, symbol: str) -> Dict:
        """Get current stock information"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            return {
                "symbol": symbol,
                "current_price": info.get("currentPrice", "N/A"),
                "market_cap": info.get("marketCap", "N/A"),
                "pe_ratio": info.get("trailingPE", "N/A"),
                "dividend_yield": info.get("dividendYield", "N/A"),
                "52_week_high": info.get("fiftyTwoWeekHigh", "N/A"),
                "52_week_low": info.get("fiftyTwoWeekLow", "N/A"),
                "average_volume": info.get("averageVolume", "N/A"),
                "company_name": info.get("longName", "N/A"),
                "sector": info.get("sector", "N/A"),
                "industry": info.get("industry", "N/A"),
            }
        except Exception as e:
            return {"error": f"Failed to fetch data for {symbol}: {str(e)}"}
    
    def get_historical_data(self, symbol: str, period: str = "1y") -> pd.DataFrame:
        """Get historical stock data"""
        try:
            ticker = yf.Ticker(symbol)
            return ticker.history(period=period)
        except Exception as e:
            print(f"Error fetching historical data: {e}")
            return pd.DataFrame()
    
    def calculate_technical_indicators(self, symbol: str) -> Dict:
        """Calculate technical indicators"""
        try:
            data = self.get_historical_data(symbol, period="3mo")
            
            if data.empty:
                return {"error": "No data available"}
            
            # Simple Moving Averages
            data['SMA_20'] = data['Close'].rolling(window=20).mean()
            data['SMA_50'] = data['Close'].rolling(window=50).mean()
            
            # RSI (Relative Strength Index)
            delta = data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            current_price = data['Close'].iloc[-1]
            sma_20 = data['SMA_20'].iloc[-1]
            sma_50 = data['SMA_50'].iloc[-1]
            current_rsi = rsi.iloc[-1]
            
            return {
                "symbol": symbol,
                "current_price": round(current_price, 2),
                "sma_20": round(sma_20, 2),
                "sma_50": round(sma_50, 2),
                "rsi": round(current_rsi, 2),
                "trend": "Bullish" if sma_20 > sma_50 else "Bearish",
                "momentum": "Strong" if current_rsi > 70 else "Weak" if current_rsi < 30 else "Neutral"
            }
        except Exception as e:
            return {"error": f"Error calculating indicators: {str(e)}"}
    
    def get_stock_recommendation(self, symbol: str) -> Dict:
        """Generate stock recommendation based on technical analysis"""
        try:
            info = self.get_stock_info(symbol)
            indicators = self.calculate_technical_indicators(symbol)
            
            if "error" in info or "error" in indicators:
                return {"error": "Could not generate recommendation"}
            
            # Simple scoring system
            score = 0.5  # Start at neutral
            
            # PE Ratio analysis
            pe_ratio = info.get("pe_ratio", 0)
            if isinstance(pe_ratio, (int, float)):
                if pe_ratio < 15:
                    score += 0.15
                elif pe_ratio > 25:
                    score -= 0.15
            
            # Technical indicators
            if indicators.get("trend") == "Bullish":
                score += 0.2
            else:
                score -= 0.2
            
            rsi = indicators.get("rsi", 50)
            if 30 < rsi < 70:
                score += 0.1
            elif rsi >= 70:
                score -= 0.1
            
            # Generate recommendation
            if score >= 0.75:
                recommendation = "STRONG BUY"
            elif score >= 0.60:
                recommendation = "BUY"
            elif score >= 0.40:
                recommendation = "HOLD"
            elif score >= 0.25:
                recommendation = "SELL"
            else:
                recommendation = "STRONG SELL"
            
            return {
                "symbol": symbol,
                "recommendation": recommendation,
                "confidence_score": round(score * 100, 2),
                "technical_analysis": indicators,
                "fundamental_data": info
            }
        except Exception as e:
            return {"error": f"Error generating recommendation: {str(e)}"}


def get_stock_data_tools():
    """Return tools for ChatGPT to use"""
    fetcher = StockDataFetcher()
    
    return [
        {
            "type": "function",
            "function": {
                "name": "get_stock_info",
                "description": "Get current stock information including price, market cap, PE ratio, etc.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "symbol": {
                            "type": "string",
                            "description": "Stock ticker symbol (e.g., AAPL, GOOGL)"
                        }
                    },
                    "required": ["symbol"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_technical_indicators",
                "description": "Calculate and return technical indicators for a stock",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "symbol": {
                            "type": "string",
                            "description": "Stock ticker symbol"
                        }
                    },
                    "required": ["symbol"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_stock_recommendation",
                "description": "Get stock recommendation based on technical and fundamental analysis",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "symbol": {
                            "type": "string",
                            "description": "Stock ticker symbol"
                        }
                    },
                    "required": ["symbol"]
                }
            }
        }
    ]
