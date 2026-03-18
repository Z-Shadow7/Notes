#code for groq
#pip install groq

from groq import Groq

client = Groq(api_key="your-groq-api-key")  # get it free at console.groq.com

# Context (dynamic — changes per user)
user_context = """
The user has a Pro plan. Purchase date: March 12, 2026.
Refund policy: refunds allowed within 30 days of purchase.
"""

# Instruction
instruction = """
Answer the user's question using the context above.
Keep your reply under 3 sentences. Be polite and direct.
"""

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",   # fast & capable — good default on Groq
    max_tokens=300,
    messages=[
        {
            "role": "system",                                  # ← System prompt
            "content": """You are a helpful customer support agent for TechCorp.
Never make up information. If unsure, say you'll check."""
        },
        {
            "role": "user",                                    # ← Context + Instruction + Input
            "content": f"{user_context}\n\n{instruction}\n\nUser question: Can I get a refund for my purchase last week?"
        }
    ]
)

print(response.choices[0].message.content)
