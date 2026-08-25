"""
Accounting Module - Financial calculations and analysis
"""
from typing import Dict, List
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Transaction:
    """Represent a financial transaction"""
    date: str
    description: str
    amount: float
    category: str
    transaction_type: str  # "income" or "expense"


class AccountingCalculator:
    """Handle accounting calculations and financial analysis"""
    
    def __init__(self):
        self.transactions: List[Transaction] = []
    
    def add_transaction(self, date: str, description: str, amount: float, 
                       category: str, transaction_type: str) -> Dict:
        """Add a transaction to the ledger"""
        try:
            transaction = Transaction(
                date=date,
                description=description,
                amount=amount,
                category=category,
                transaction_type=transaction_type.lower()
            )
            self.transactions.append(transaction)
            return {
                "status": "success",
                "message": f"Transaction added: {description}",
                "transaction": transaction.__dict__
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def calculate_profit_loss(self) -> Dict:
        """Calculate profit and loss"""
        total_income = sum(
            t.amount for t in self.transactions 
            if t.transaction_type == "income"
        )
        total_expense = sum(
            t.amount for t in self.transactions 
            if t.transaction_type == "expense"
        )
        net_profit = total_income - total_expense
        profit_margin = (net_profit / total_income * 100) if total_income > 0 else 0
        
        return {
            "total_income": round(total_income, 2),
            "total_expense": round(total_expense, 2),
            "net_profit": round(net_profit, 2),
            "profit_margin": round(profit_margin, 2)
        }
    
    def calculate_expenses_by_category(self) -> Dict:
        """Calculate total expenses by category"""
        expenses = {}
        for t in self.transactions:
            if t.transaction_type == "expense":
                expenses[t.category] = expenses.get(t.category, 0) + t.amount
        
        return {
            category: round(amount, 2) 
            for category, amount in sorted(expenses.items(), 
                                          key=lambda x: x[1], reverse=True)
        }
    
    def calculate_income_by_category(self) -> Dict:
        """Calculate total income by category"""
        income = {}
        for t in self.transactions:
            if t.transaction_type == "income":
                income[t.category] = income.get(t.category, 0) + t.amount
        
        return {
            category: round(amount, 2) 
            for category, amount in sorted(income.items(), 
                                          key=lambda x: x[1], reverse=True)
        }
    
    def calculate_financial_ratios(self, assets: float, liabilities: float, 
                                   equity: float) -> Dict:
        """Calculate key financial ratios"""
        try:
            debt_to_equity = liabilities / equity if equity > 0 else 0
            debt_to_assets = liabilities / assets if assets > 0 else 0
            equity_multiplier = assets / equity if equity > 0 else 0
            
            return {
                "debt_to_equity_ratio": round(debt_to_equity, 2),
                "debt_to_assets_ratio": round(debt_to_assets, 2),
                "equity_multiplier": round(equity_multiplier, 2),
                "financial_health": self._assess_financial_health(debt_to_equity)
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _assess_financial_health(self, debt_to_equity: float) -> str:
        """Assess financial health based on debt-to-equity ratio"""
        if debt_to_equity < 0.5:
            return "Excellent"
        elif debt_to_equity < 1.0:
            return "Good"
        elif debt_to_equity < 2.0:
            return "Moderate"
        else:
            return "Risky"
    
    def calculate_tax_estimate(self, income: float, tax_rate: float = 0.30) -> Dict:
        """Estimate tax liability"""
        tax_amount = income * tax_rate
        after_tax_income = income - tax_amount
        
        return {
            "gross_income": round(income, 2),
            "tax_rate": f"{tax_rate * 100}%",
            "estimated_tax": round(tax_amount, 2),
            "after_tax_income": round(after_tax_income, 2)
        }
    
    def get_financial_summary(self) -> Dict:
        """Get comprehensive financial summary"""
        return {
            "profit_loss": self.calculate_profit_loss(),
            "expenses_by_category": self.calculate_expenses_by_category(),
            "income_by_category": self.calculate_income_by_category(),
            "total_transactions": len(self.transactions)
        }
