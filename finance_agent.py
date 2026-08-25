"""
Finance AI Agent - Main agent powered by ChatGPT
"""
import openai
from typing import Any, Dict, List, Optional
import json
from config import OPENAI_API_KEY, MODEL, MAX_TOKENS, AGENT_TEMPERATURE
from stock_data import StockDataFetcher, get_stock_data_tools
from accounting import AccountingCalculator

openai.api_key = OPENAI_API_KEY


class FinanceAIAgent:
    """AI-powered financial analyst and accounting assistant"""
    
    def __init__(self):
        self.stock_fetcher = StockDataFetcher()
        self.accounting = AccountingCalculator()
        self.conversation_history = []
        self.setup_tools()
    
    def setup_tools(self):
        """Setup tools for ChatGPT"""
        self.tools = get_stock_data_tools()
    
    def add_message(self, role: str, content: str):
        """Add message to conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content
        })
    
    def get_system_prompt(self) -> str:
        """Get system prompt for the agent"""
        return """You are an expert financial analyst and accounting assistant named Lalit's AI Agent.
        
You have access to:
1. Real-time stock data and technical analysis
2. Accounting and financial calculations
3. Portfolio analysis capabilities

Your responsibilities:
- Provide stock recommendations based on technical and fundamental analysis
- Analyze market trends and volatility
- Help with accounting calculations and financial planning
- Assess financial health and risk profiles
- Answer questions about investments and accounting

Always be professional, data-driven, and provide clear explanations for your recommendations.
When users ask about stocks, use the available tools to fetch real data and provide accurate analysis.
For accounting matters, help calculate and interpret financial metrics.

Remember: Always include disclaimer that recommendations are for informational purposes only."""
    
    def process_tool_call(self, tool_name: str, tool_input: Dict) -> Any:
        """Process tool calls from ChatGPT"""
        
        if tool_name == "get_stock_info":
            return self.stock_fetcher.get_stock_info(tool_input.get("symbol", ""))
        
        elif tool_name == "get_technical_indicators":
            return self.stock_fetcher.calculate_technical_indicators(tool_input.get("symbol", ""))
        
        elif tool_name == "get_stock_recommendation":
            return self.stock_fetcher.get_stock_recommendation(tool_input.get("symbol", ""))
        
        else:
            return {"error": f"Unknown tool: {tool_name}"}
    
    def chat(self, user_message: str) -> str:
        """Send a message and get response from ChatGPT"""
        self.add_message("user", user_message)
        
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=self.conversation_history,
            tools=self.tools,
            tool_choice="auto",
            temperature=AGENT_TEMPERATURE,
            max_tokens=MAX_TOKENS,
            system=self.get_system_prompt()
        )
        
        # Process response
        assistant_message = response.choices[0].message
        
        # Check if there are tool calls
        if hasattr(assistant_message, 'tool_calls') and assistant_message.tool_calls:
            # Add assistant message with tool calls
            self.add_message("assistant", str(assistant_message))
            
            # Process each tool call
            for tool_call in assistant_message.tool_calls:
                tool_name = tool_call.function.name
                tool_input = json.loads(tool_call.function.arguments)
                
                print(f"\n🔧 Calling tool: {tool_name}")
                print(f"   Input: {tool_input}")
                
                tool_result = self.process_tool_call(tool_name, tool_input)
                print(f"   Result: {tool_result}")
                
                # Add tool result to conversation
                self.conversation_history.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": json.dumps(tool_result)
                })
            
            # Get final response after tool calls
            response = openai.ChatCompletion.create(
                model=MODEL,
                messages=self.conversation_history,
                tools=self.tools,
                temperature=AGENT_TEMPERATURE,
                max_tokens=MAX_TOKENS,
                system=self.get_system_prompt()
            )
            
            final_response = response.choices[0].message.content
        else:
            final_response = assistant_message.content
        
        # Add assistant response to history
        self.add_message("assistant", final_response)
        
        return final_response
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def get_conversation_history(self) -> List[Dict]:
        """Get current conversation history"""
        return self.conversation_history


def main():
    """Main function to run the agent"""
    print("=" * 60)
    print("🏦 Lalit's AI Stock Analyst Agent")
    print("=" * 60)
    print("\nWelcome! I'm your AI-powered financial analyst.")
    print("Ask me about stocks, recommendations, or accounting help.")
    print("Type 'quit' to exit, 'clear' to clear history.\n")
    
    agent = FinanceAIAgent()
    
    while True:
        try:
            user_input = input("\n📊 You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == 'quit':
                print("\n✅ Goodbye! Happy investing! 📈")
                break
            
            if user_input.lower() == 'clear':
                agent.clear_history()
                print("✓ Conversation history cleared.")
                continue
            
            print("\n🤖 Agent is thinking...")
            response = agent.chat(user_input)
            print(f"\n💡 Agent: {response}")
        
        except KeyboardInterrupt:
            print("\n\n✅ Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
