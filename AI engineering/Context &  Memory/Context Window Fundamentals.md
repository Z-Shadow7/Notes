# Context Window Fundamentals

> **Roadmap:** Context & Memory → Topic 1 of 8
> **Status:** ✅ Completed

---

## What is the context window?

The context window is the **total amount of text the model can see at one time**. Everything — your system prompt, the full conversation history, any documents you feed it, and its own replies — all has to fit inside this one window.

Whatever falls outside it, the model simply cannot see. It's not forgotten — it never existed as far as the model is concerned.

Think of it like a desk. You can only work with what's physically on the desk right now. Older papers that slid off the edge are gone from your view — even if they're still in the room somewhere.

![Context Window Diagram](./context_window_fundamentals.svg)

---

## What is a token?

The model doesn't count words — it counts **tokens**. A token is roughly 3/4 of a word.

| Rule of thumb | Tokens |
|---|---|
| 1 word | ≈ 1.3 tokens |
| 100 words | ≈ 130 tokens |
| 1 page of text | ≈ 500 tokens |
| 1000 tokens | ≈ 750 words |

A 128k token window holds roughly 96,000 words — about the length of a novel. But it fills up fast when you have long conversations, big documents, and a detailed system prompt all competing for space.

---

## Context limits for popular models

| Model | Context Window |
|---|---|
| `llama-3.3-70b-versatile` (Groq) | 128k tokens |
| `llama-3.1-8b-instant` (Groq) | 128k tokens |
| `gpt-4o` | 128k tokens |
| `claude-sonnet-4-6` | 200k tokens |
| `gemini-1.5-pro` | 1M tokens |

---

## Tracking token usage in code

Every Groq API response tells you exactly how many tokens were used. Always track this in production.

```python
from groq import Groq

client = Groq(api_key="your-groq-api-key")

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    max_tokens=300,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user",   "content": "Explain what a neural network is in simple terms."}
    ]
)

print(response.choices[0].message.content)

# Token usage — always check this
usage = response.usage
print(f"\nPrompt tokens:     {usage.prompt_tokens}")
print(f"Completion tokens: {usage.completion_tokens}")
print(f"Total tokens:      {usage.total_tokens}")
```

---

## What happens when you run out of context?

When a conversation grows too long, one of three things happens:

- **API throws an error** — if you send more tokens than the model's limit, the call fails outright
- **Old messages get silently cut** — if you truncate naively, the model loses the system prompt or early context it needs
- **The model "forgets"** — if managed imperfectly, it simply won't know things it was told earlier

---

## Detecting when you're close to the limit

```python
from groq import Groq

client = Groq(api_key="your-groq-api-key")

MODEL_CONTEXT_LIMIT = 128_000  # tokens
WARNING_THRESHOLD   = 0.80     # warn at 80% full

def chat_with_limit_check(conversation: list, system: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=500,
        messages=[
            {"role": "system", "content": system},
            *conversation
        ]
    )

    used = response.usage.total_tokens
    pct  = used / MODEL_CONTEXT_LIMIT

    print(f"Tokens used: {used} / {MODEL_CONTEXT_LIMIT} ({pct:.0%})")

    if pct >= WARNING_THRESHOLD:
        print("⚠️  WARNING: Context window 80% full. Consider summarising history.")

    return response.choices[0].message.content


# Simulate a growing conversation
system       = "You are a helpful coding assistant."
conversation = []

questions = [
    "What is a Python list?",
    "What is the difference between a list and a tuple?",
    "When should I use a dictionary instead?",
]

for q in questions:
    conversation.append({"role": "user", "content": q})
    reply = chat_with_limit_check(conversation, system)
    conversation.append({"role": "assistant", "content": reply})
    print(f"Q: {q}\nA: {reply}\n")
```

---

## Key Insight

> The context window is not infinite memory — it's a sliding spotlight. Everything the model knows about your conversation exists only inside that spotlight.

Managing what goes in, what stays in, and what gets summarised or removed is one of the core skills of AI engineering. The next topics in this section are all about doing that well.

---

➡️ **Next: Tokens & Token Counting**
