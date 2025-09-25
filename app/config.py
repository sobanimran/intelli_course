import os
from dotenv import load_dotenv

# Load .env file from project root
load_dotenv()

# Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Debug print (will only show on startup)
print("🔑 Config loaded:")
print(f"   GROQ_API_KEY set: {bool(GROQ_API_KEY)}")
print(f"   TAVILY_API_KEY set: {bool(TAVILY_API_KEY)}")
