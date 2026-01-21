# AI-102 Study Guide: Chatbot with Memory

This guide covers certification-relevant concepts for multi-turn conversations and conversation state management.

---

## Part 1: Key Concepts

### 1. The Fundamental Truth: Models Have No Memory

Azure OpenAI models are **stateless**. Each API call is completely independent. The model doesn't remember:
- Previous questions you asked
- Answers it gave before
- Any context from earlier in the conversation

**Memory is YOUR responsibility.** You create the illusion of memory by sending the conversation history with each request.

---

### 2. How Conversation Memory Works

#### The Pattern

```python
# Request 1
messages = [system, user1]           → Response: assistant1

# Request 2 (includes previous exchange)
messages = [system, user1, assistant1, user2]    → Response: assistant2

# Request 3 (includes all previous exchanges)
messages = [system, user1, assistant1, user2, assistant2, user3] → Response: assistant3
```

#### The Code Pattern

```python
# Initialize
conversation = [{"role": "system", "content": "..."}]

# Loop
while True:
    # 1. Get user input
    user_input = input()

    # 2. Add to history
    conversation.append({"role": "user", "content": user_input})

    # 3. Send FULL history
    response = client.chat.completions.create(
        model=deployment,
        messages=conversation  # Everything!
    )

    # 4. Add response to history
    conversation.append({
        "role": "assistant",
        "content": response.choices[0].message.content
    })
```

---

### 3. Context Window Management

#### The Problem

Every model has a maximum context window (total tokens it can process):

| Model | Context Window |
|-------|----------------|
| GPT-3.5-turbo | 4K - 16K |
| GPT-4 | 8K - 128K |
| GPT-4o-mini | 128K |

As conversations grow, you'll hit this limit.

#### The Formula

```
context_window >= prompt_tokens + max_completion_tokens
```

Where `prompt_tokens` = system message + all conversation history

#### The Solution: Trimming

```python
# Remove oldest messages (keep system at index 0)
while token_count > limit:
    del conversation[1]  # Remove oldest user/assistant pair
```

---

### 4. Token Counting

Use the `tiktoken` library to count tokens:

```python
import tiktoken

# GPT-4 and GPT-3.5-turbo use cl100k_base encoding
encoding = tiktoken.get_encoding("cl100k_base")

def count_tokens(text):
    return len(encoding.encode(text))

def count_message_tokens(messages):
    total = 0
    for message in messages:
        total += 4  # Message overhead
        total += count_tokens(message["content"])
    total += 2  # Priming tokens
    return total
```

---

### 5. System Message Best Practices

The system message should:
- **Always be first** in the messages array
- **Never be removed** during trimming
- **Define consistent behavior** for the entire conversation
- **Include persona, constraints, and guidelines**

Example:
```python
SYSTEM_PROMPT = """You are a customer service agent for TechCorp.
- Be professional and helpful
- Only discuss TechCorp products
- If you don't know something, offer to connect to human support
- Never share pricing without confirming customer's region"""
```

---

### 6. Context Degradation

**Warning:** Trimming old messages causes information loss.

**Symptoms:**
- Bot forgets user preferences mentioned early
- Inconsistent responses
- Loss of important context

**Mitigation strategies:**
1. **Summarization**: Periodically summarize older conversation into a condensed message
2. **Key facts extraction**: Store important details separately and inject into system prompt
3. **Session limits**: Start new conversations after reaching certain length
4. **Sliding window with summary**: Keep recent N messages + summary of older ones

---

## Part 2: Certification Q&A

### Conversation Memory Fundamentals

**Q: Do Azure OpenAI models remember previous conversations?**
> A: No. Azure OpenAI models are stateless and have no built-in memory. Each API call is independent. To maintain conversation context, the application must store and resend the entire conversation history with each request.

**Q: How do you implement conversation memory in a chatbot?**
> A: Maintain a messages array that accumulates the conversation:
> 1. Start with a system message
> 2. Append each user message with role="user"
> 3. Send the entire array with each API call
> 4. Append the assistant's response with role="assistant"
> 5. Repeat for each turn
>
> The model "remembers" because you tell it everything that happened.

**Q: Why must you include the assistant's previous responses in the conversation history?**
> A: Without the assistant's responses, the model wouldn't know what it said previously. This would cause:
> - Inconsistent or contradictory responses
> - Loss of conversation flow
> - Inability to reference its own previous statements

**Q: What is the correct order of messages in a conversation array?**
> A: Messages should be in chronological order:
> 1. System message (first, defines behavior)
> 2. User message 1
> 3. Assistant message 1
> 4. User message 2
> 5. Assistant message 2
> ... and so on

---

### Context Window Management

**Q: What is a context window?**
> A: The context window is the maximum number of tokens a model can process in a single request. It includes both input (prompt) and output (completion) tokens. Different models have different limits (e.g., 4K, 8K, 128K tokens).

**Q: What happens if your conversation exceeds the context window?**
> A: You'll receive an error. The API cannot process requests that exceed the model's context window. You must manage conversation length to stay within limits.

**Q: How do you handle long conversations that approach the context limit?**
> A: Common strategies:
> - **Trimming**: Remove oldest messages (keeping system message)
> - **Summarization**: Replace old messages with a summary
> - **Session restart**: Start new conversations periodically
> - **Sliding window**: Keep only the most recent N messages

**Q: When trimming conversation history, which message should you never remove?**
> A: The system message (always at index 0). It defines the assistant's behavior and should persist throughout the conversation. Remove oldest user/assistant pairs instead.

**Q: How do you calculate if a conversation fits within the context window?**
> A: Ensure: `prompt_tokens + max_completion_tokens <= context_window`
>
> Where prompt_tokens includes the system message plus all conversation history.

---

### Token Management

**Q: What library is commonly used to count tokens for Azure OpenAI?**
> A: `tiktoken` - OpenAI's tokenizer library. GPT-4 and GPT-3.5-turbo models use the `cl100k_base` encoding.

**Q: Why is it important to count tokens before sending a request?**
> A: Token counting helps you:
> - Stay within context window limits
> - Estimate costs (billing is per token)
> - Decide when to trim conversation history
> - Reserve space for the response

**Q: Approximately how many tokens are in 1000 words of English text?**
> A: Roughly 1300-1500 tokens. A common estimate is ~0.75 words per token, or ~4 characters per token.

**Q: Does the system message count toward the token limit?**
> A: Yes. The system message is included in every request and counts toward your prompt tokens. A lengthy system prompt reduces space available for conversation history.

---

### System Messages and Personas

**Q: What should a chatbot's system message include?**
> A: A well-designed system message includes:
> - Persona/role definition ("You are a travel assistant")
> - Knowledge domain ("Your expertise includes destinations, budgets...")
> - Behavioral guidelines ("Be professional", "Ask clarifying questions")
> - Constraints ("Only discuss company products", "Never provide medical advice")
> - Output format preferences if needed

**Q: How does the system message affect conversation memory?**
> A: The system message:
> - Is sent with EVERY request (counts toward tokens each time)
> - Should remain constant throughout the conversation
> - Is never removed during history trimming
> - Provides consistent behavioral context even as messages are trimmed

**Q: Can you change the system message mid-conversation?**
> A: Technically yes, but it's not recommended. Changing the system message can cause:
> - Inconsistent assistant behavior
> - Confusion if the persona changes
> - Potential contradiction with earlier responses
>
> If behavior needs to change, consider starting a new conversation.

---

### Practical Implementation

**Q: A user complains the chatbot forgot something they mentioned 20 messages ago. What's the likely cause?**
> A: The conversation history was likely trimmed to stay within token limits, removing the message containing that information. Solutions:
> - Increase context window (use model with larger limit)
> - Implement summarization to preserve key facts
> - Extract and store important details separately

**Q: How would you implement a chatbot that remembers user preferences across sessions?**
> A: Store user preferences in a database or user profile. Inject these preferences into the system message or as an initial context message at the start of each new session:
> ```python
> system_prompt = f"""You are a travel assistant.
> User preferences from previous sessions:
> - Prefers budget travel
> - Interested in hiking
> - Vegetarian dietary requirements
> """
> ```

**Q: What is context degradation and how do you mitigate it?**
> A: Context degradation occurs when trimming old messages causes loss of important information, leading to:
> - Forgotten user preferences
> - Inconsistent responses
> - Lost conversation context
>
> Mitigation strategies:
> - Summarize older messages instead of deleting
> - Extract key facts into persistent storage
> - Set reasonable session lengths
> - Include important context in system message

**Q: You're building a customer service chatbot. How do you ensure it remembers the customer's issue throughout a long conversation?**
> A: Multiple approaches:
> 1. **Topic tracking**: Extract and store the main issue in a variable, inject into prompts
> 2. **Summarization**: Periodically summarize conversation, include summary with new messages
> 3. **Key-value extraction**: Pull out important details (order number, issue type) and persist separately
> 4. **Prioritized trimming**: When trimming, keep messages that mention the core issue

---

### Token Limits and Billing

**Q: How does conversation length affect Azure OpenAI costs?**
> A: Costs increase with conversation length because:
> - You send MORE tokens with each request (full history)
> - Request 1: ~100 tokens
> - Request 10: ~1000 tokens (accumulated history)
> - Request 20: ~2000 tokens
>
> Long conversations multiply costs significantly.

**Q: What's more cost-effective: many short conversations or fewer long ones?**
> A: Many short conversations are typically more cost-effective because you're not repeatedly sending the same historical context. However, this must be balanced against user experience and the need for continuity.

---

### Error Handling

**Q: What error occurs when you exceed the context window?**
> A: You'll receive an error indicating the request exceeds the maximum context length. The exact message varies but typically mentions "maximum context length" or "token limit exceeded."

**Q: How should you handle a context window error in production?**
> A: Gracefully recover by:
> 1. Trimming old messages from conversation history
> 2. Retrying the request
> 3. If still failing, inform the user and offer to start a new conversation
> 4. Log the error for monitoring

---

## Part 3: Quick Reference

### Conversation Memory Pattern
```python
conversation = [{"role": "system", "content": PROMPT}]

while chatting:
    conversation.append({"role": "user", "content": input()})
    response = client.chat.completions.create(model=NAME, messages=conversation)
    conversation.append({"role": "assistant", "content": response.choices[0].message.content})
```

### Token Counting
```python
import tiktoken
encoding = tiktoken.get_encoding("cl100k_base")
tokens = len(encoding.encode(text))
```

### Trimming Strategy
```python
while count_tokens(conversation) > LIMIT:
    del conversation[1]  # Keep system message at [0]
```

### Context Window Sizes
| Model | Window |
|-------|--------|
| GPT-3.5-turbo | 4K-16K |
| GPT-4 | 8K-128K |
| GPT-4o-mini | 128K |

### Key Rules
1. Models have NO memory - you must send full history
2. System message = always first, never trimmed
3. Token count grows with each exchange
4. Trim oldest messages when approaching limit
5. Trimming causes information loss - mitigate with summarization
