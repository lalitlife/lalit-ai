import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("MODEL", "gpt-4")

# Finance API Keys
ALPHA_VANTAGE_KEY = os.getenv("ALPHA_VANTAGE_KEY")

# Agent Configuration
AGENT_TEMPERATURE = 0.7
MAX_TOKENS = 2000
TIMEOUT = 30

# Financial Thresholds
STRONG_BUY_THRESHOLD = 0.75
BUY_THRESHOLD = 0.60
HOLD_THRESHOLD = 0.40
SELL_THRESHOLD = 0.25

# Data Configuration
CACHE_DURATION = 3600  # 1 hour in seconds
