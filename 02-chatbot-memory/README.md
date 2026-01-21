# 02 - Chatbot with Memory: Multi-Turn Conversations

## AI-102 Certification Topics Covered

| Exam Objective | What You'll Learn |
|----------------|-------------------|
| Implement multi-turn conversations | Managing conversation history |
| Manage context and state | Token counting and context window limits |
| Prompt engineering | System prompts for chatbot personas |
| Build conversational AI | Practical chatbot implementation |

---

## The Key Concept: Models Have No Memory

**This is crucial to understand:**

Azure OpenAI models have **NO built-in memory**. Each API call is independent. To create the illusion of memory, YOU must:

1. Store the conversation history
2. Send the ENTIRE history with each request
3. Manage the history to stay within token limits

```
Request 1: [system, user1]                    → assistant1
Request 2: [system, user1, assistant1, user2] → assistant2
Request 3: [system, user1, assistant1, user2, assistant2, user3] → assistant3
```

The model "remembers" because you're telling it everything that happened before.

---

## How Memory Works

### The Conversation Array

```python
conversation = [
    {"role": "system", "content": "You are a travel assistant..."},
    {"role": "user", "content": "I want to visit Japan"},
    {"role": "assistant", "content": "Japan is wonderful! When are you planning to go?"},
    {"role": "user", "content": "Next spring"},
    {"role": "assistant", "content": "Spring is perfect for cherry blossoms..."}
]
```

### The Pattern

```python
# 1. Initialize with system message
conversation = [{"role": "system", "content": SYSTEM_PROMPT}]

# 2. Add user input
conversation.append({"role": "user", "content": user_input})

# 3. Send FULL history to API
response = client.chat.completions.create(
    model=DEPLOYMENT_NAME,
    messages=conversation  # Everything sent each time!
)

# 4. Add assistant response to history
conversation.append({"role": "assistant", "content": response.choices[0].message.content})

# 5. Repeat from step 2
```

---

## Project Setup

### 1. Navigate to the project folder
```bash
cd 02-chatbot-memory
```

### 2. Create and activate virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
cp .env.example .env
```

Edit `.env` with your Azure credentials (same as 01-basic-chat).

### 5. Run the chatbot
```bash
python chatbot.py
```

### Commands
- Type messages to chat
- `stats` - Show conversation statistics (tokens, message count)
- `clear` - Reset conversation memory
- `quit` - Exit

---

## Key Concepts

### 1. Token Management

Every conversation has a **context window limit** (e.g., 4K, 8K, 128K tokens).

```
context_window >= prompt_tokens + completion_tokens
```

As conversations grow, you must manage tokens:

```python
# Remove oldest messages when approaching limit
while token_count > limit:
    del conversation[1]  # Keep system message at [0]
```

### 2. Token Counting

Use `tiktoken` library to count tokens before sending:

```python
import tiktoken

encoding = tiktoken.get_encoding("cl100k_base")  # GPT-4/3.5 encoding
token_count = len(encoding.encode(text))
```

### 3. System Prompt Persistence

The system message should:
- Always be first in the array
- Never be removed during trimming
- Define consistent behavior throughout the conversation

### 4. Context Degradation

**Warning:** As conversations get longer and you trim old messages, the model loses earlier context. This can cause:
- Forgetting user preferences mentioned early
- Inconsistent responses
- Loss of important details

**Solution:** For long interactions, consider:
- Summarizing earlier conversation
- Storing key facts separately
- Starting new conversation sessions

---

## Troubleshooting

### Bot "forgets" things I said earlier
- Check if messages were trimmed due to token limits
- Use `stats` command to see token count
- Consider increasing MAX_CONTEXT_TOKENS

### Responses seem disconnected
- Ensure you're adding BOTH user AND assistant messages to history
- Check that the conversation array is being passed correctly

### Token limit errors
- Reduce MAX_RESPONSE_TOKENS
- Implement conversation trimming
- Start a new conversation with `clear`

---

## Files in This Project

| File | Purpose |
|------|---------|
| `chatbot.py` | Travel assistant chatbot with memory management |
| `requirements.txt` | Python dependencies (includes tiktoken) |
| `.env.example` | Environment variable template |

---

## Try These Conversations

### Test Memory Persistence
```
You: I'm planning a trip to Japan with my wife
Bot: [responds about Japan trip for two]

You: What's a good budget?
Bot: [should remember it's for Japan, for two people]

You: We love hiking
Bot: [should remember Japan + couple + now knows hiking preference]

You: Suggest an itinerary
Bot: [should incorporate ALL previous context]
```

### Test Context Building
```
You: I have $3000 budget
You: I like beaches
You: I prefer quiet places
You: I'm traveling in December
You: Suggest a destination
Bot: [should consider budget + beaches + quiet + December]
```

---

## Microsoft Learn Resources

- [Conversation loop documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/chatgpt)
- [Managing conversation history](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/prompt-engineering)
- [Token limits and context](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models)
