# AI-102 Study Guide: Azure OpenAI Chat Completions

This guide covers certification-relevant concepts from the 01-basic-chat exercise.

---

## Part 1: Key Concepts

### 1. Azure OpenAI Resource Architecture

```
Azure Subscription
    └── Resource Group
            └── Azure OpenAI Resource (has endpoint + keys)
                    └── Deployments (you can have multiple)
                            └── gpt-4o-mini, gpt-4, etc.
```

**Exam tip:** One resource can have multiple model deployments. Each deployment has its own name and rate limits.

---

### 2. Key Identifiers (Know the Difference!)

| Term | What it is | Example |
|------|------------|---------|
| **Endpoint** | Your resource's base URL | `https://xxx.cognitiveservices.azure.com/` |
| **Deployment name** | What YOU named the deployment | `gpt-4o-mini` |
| **Model name** | The actual model | `gpt-4o-mini` (can match, but doesn't have to) |
| **API version** | REST API protocol version | `2025-01-01-preview` |
| **Model version** | Training snapshot date | `2024-07-18` |

---

### 3. Authentication Methods

| Method | Header | When to use |
|--------|--------|-------------|
| **API Key** | `api-key: <key>` | Development, simple apps |
| **Azure AD / Entra ID** | `Authorization: Bearer <token>` | Production, enterprise, Managed Identity |

**Exam tip:** Managed Identity is the recommended approach for production (no keys to manage).

---

### 4. Chat Completions API

#### Message Roles

```python
messages = [
    {"role": "system", "content": "..."},    # Sets behavior (first)
    {"role": "user", "content": "..."},      # Human input
    {"role": "assistant", "content": "..."}  # AI responses (for context)
]
```

| Role | Purpose | Exam notes |
|------|---------|------------|
| `system` | Defines AI persona, constraints, output format | Processed first, counts toward tokens |
| `user` | Human input | Required |
| `assistant` | Previous AI responses | Used for multi-turn conversations |

#### The API Call (SDK)

```python
response = client.chat.completions.create(
    model=DEPLOYMENT_NAME,      # Your deployment name, NOT model name
    messages=[...],             # Conversation history
    temperature=0.7,            # Randomness
    max_tokens=150,             # Response length limit
    top_p=1.0                   # Nucleus sampling
)
```

#### The API Call (REST)

```
POST https://{endpoint}/openai/deployments/{deployment}/chat/completions?api-version={version}

Headers:
  api-key: {your-key}
  Content-Type: application/json

Body:
{
  "messages": [...],
  "temperature": 0.7,
  "max_tokens": 150
}
```

**Exam tip:** Know both SDK and REST approaches.

---

### 5. Key Parameters

#### Temperature
| Value | Behavior | Use case |
|-------|----------|----------|
| 0.0 | Deterministic, same output every time | Code generation, factual Q&A, data extraction |
| 0.5-0.7 | Balanced | General conversation |
| 1.0+ | Creative, varied | Brainstorming, creative writing |
| 1.5+ | Very random | Experimental (may be incoherent) |

#### Top_p (Nucleus Sampling)
| Value | Behavior |
|-------|----------|
| 0.1 | Only top 10% probable tokens (focused) |
| 0.5 | Top 50% (moderate) |
| 0.95 | Top 95% (diverse vocabulary) |

**Exam tip:** Don't use temperature AND top_p together. Pick one.

#### Max_tokens
- Limits **response** length (not prompt)
- If exceeded: `finish_reason = "length"` (response truncated)
- Must fit within: `context_window - prompt_tokens`

---

### 6. Response Structure

```python
response.choices[0].message.content    # The text response
response.choices[0].finish_reason      # Why it stopped
response.usage.prompt_tokens           # Input tokens (billed)
response.usage.completion_tokens       # Output tokens (billed)
response.usage.total_tokens            # Total tokens
```

#### Finish Reasons

| Value | Meaning |
|-------|---------|
| `stop` | Natural completion |
| `length` | Hit max_tokens limit (truncated!) |
| `content_filter` | Blocked by Azure content filtering |

---

### 7. Token Basics

- ~4 characters = 1 token (English)
- ~75 words = 100 tokens
- You pay for **prompt_tokens + completion_tokens**
- Each model has a **context window** (e.g., 8K, 32K, 128K tokens)

**Exam tip:** Know that billing is per 1,000 tokens, varies by model.

---

### 8. Prompt Engineering (System Messages)

System prompts control AI behavior without fine-tuning:

| Use case | Example system prompt |
|----------|----------------------|
| Persona | "You are a professional legal assistant." |
| Constraints | "Only answer questions about cooking." |
| Output format | "Respond in JSON format with keys: answer, confidence." |
| Safety | "Never provide medical diagnoses." |

**Exam tip:** System prompts are the primary tool for customizing behavior.

---

### 9. Content Filtering

Azure OpenAI has **built-in content filtering** (cannot be fully disabled):
- Hate speech
- Violence
- Sexual content
- Self-harm

If triggered: `finish_reason = "content_filter"`

---

### 10. Security Best Practices

| Practice | Why |
|----------|-----|
| Never commit API keys | Use `.env` files, Key Vault |
| Use Managed Identity in production | No keys to rotate/leak |
| Regenerate exposed keys immediately | Prevent unauthorized use |
| Use `.gitignore` for `.env` | Keep secrets out of repos |

---

### 11. URL Structure (REST API)

```
https://{resource}.cognitiveservices.azure.com/openai/deployments/{deployment}/chat/completions?api-version={version}
        └─────────────── endpoint ───────────────┘                 └─deployment─┘                           └─api version─┘
```

---

## Part 2: Certification Q&A

### Azure OpenAI Fundamentals

**Q: What is the relationship between an Azure OpenAI resource and deployments?**
> A: An Azure OpenAI resource is a container that can hold multiple model deployments. Each deployment is an instance of a specific model (like GPT-4 or GPT-3.5-turbo) with its own name and rate limits. You need one resource but can create many deployments within it.

**Q: What's the difference between the endpoint, deployment name, and model name?**
> A:
> - Endpoint: The base URL of your Azure OpenAI resource (e.g., `https://myresource.cognitiveservices.azure.com/`)
> - Deployment name: The name YOU give when deploying a model (e.g., "my-gpt4-deployment")
> - Model name: The actual model being deployed (e.g., "gpt-4", "gpt-35-turbo")
>
> The deployment name and model name can be different - you choose the deployment name.

**Q: What's the difference between API version and model version?**
> A:
> - API version: The version of the REST API protocol (e.g., `2025-01-01-preview`). Determines available features and request/response format.
> - Model version: The training snapshot date of the model (e.g., `2024-07-18`). Determines the model's knowledge and capabilities.
>
> They are independent - you can call the same model through different API versions.

**Q: Where do you find the API version for your deployment?**
> A: In Azure AI Foundry, click on your deployment to see the endpoint URL. The API version is in the query parameter: `?api-version=2025-01-01-preview`

---

### Authentication

**Q: How does Azure OpenAI API key authentication work?**
> A: Azure OpenAI uses the `api-key` header (not `Authorization: Bearer`). You include your API key directly in the request header:
> ```
> api-key: your-api-key-here
> ```

**Q: What authentication method is recommended for production Azure OpenAI applications?**
> A: Azure AD (Entra ID) with Managed Identity. This eliminates the need to manage API keys, provides automatic credential rotation, and integrates with Azure's identity management.

**Q: How does Azure OpenAI authentication differ from standard OpenAI?**
> A:
> - Azure OpenAI: Uses `api-key` header or Azure AD tokens
> - Standard OpenAI: Uses `Authorization: Bearer {token}` header
>
> Azure also supports Managed Identity for keyless authentication.

---

### Chat Completions API

**Q: What are the three message roles in the Chat Completions API?**
> A:
> - `system`: Sets the AI's behavior, personality, and constraints. Processed first.
> - `user`: Represents human input/questions.
> - `assistant`: Represents the AI's previous responses. Used for multi-turn context.

**Q: What is the purpose of the system message?**
> A: The system message defines the AI's behavior, persona, constraints, and output format. It's processed first and influences all subsequent responses. This is the primary tool for prompt engineering without fine-tuning the model.

**Q: In a multi-turn conversation, how do you maintain context?**
> A: Include previous messages in the messages array with appropriate roles. The conversation history is passed with each request:
> ```python
> messages = [
>     {"role": "system", "content": "You are a helpful assistant."},
>     {"role": "user", "content": "What is Python?"},
>     {"role": "assistant", "content": "Python is a programming language..."},
>     {"role": "user", "content": "What are its main uses?"}  # New question
> ]
> ```

**Q: When using the SDK, what do you pass to the `model` parameter?**
> A: The deployment name, NOT the model name. For example, if you named your deployment "my-gpt4", you use:
> ```python
> model="my-gpt4"
> ```
> Not `model="gpt-4"`.

---

### Parameters

**Q: What does the temperature parameter control?**
> A: Temperature controls randomness/creativity in responses:
> - 0.0: Deterministic, focused, consistent outputs
> - 0.5-0.7: Balanced
> - 1.0+: More creative and varied
> - 1.5+: Very random (may be incoherent)

**Q: When should you use temperature=0?**
> A: For tasks requiring deterministic, consistent outputs:
> - Code generation
> - Factual Q&A
> - Data extraction
> - Classification tasks
> - Any scenario where you want the same output for the same input

**Q: What is top_p (nucleus sampling)?**
> A: Top_p controls vocabulary diversity by limiting token selection to those within a cumulative probability:
> - 0.1: Only considers top 10% most likely tokens (very focused)
> - 0.5: Considers top 50% probability mass
> - 0.95: Considers nearly all tokens (diverse)

**Q: Can you use temperature and top_p together?**
> A: Microsoft recommends changing EITHER temperature OR top_p, not both. They are alternative approaches to controlling randomness. Using both can produce unpredictable results.

**Q: What does max_tokens control?**
> A: max_tokens limits the maximum length of the response (completion), not the prompt. If the response would exceed this limit, it gets truncated and `finish_reason` will be "length".

**Q: How do you know if a response was truncated due to max_tokens?**
> A: Check `response.choices[0].finish_reason`. If it equals `"length"`, the response was cut off because it hit the max_tokens limit.

---

### Response Handling

**Q: What are the possible values for finish_reason?**
> A:
> - `stop`: The model completed naturally
> - `length`: Response was truncated due to max_tokens limit
> - `content_filter`: Response was blocked by Azure's content filtering

**Q: What information is in the usage object of a response?**
> A:
> - `prompt_tokens`: Number of tokens in the input (billed)
> - `completion_tokens`: Number of tokens in the response (billed)
> - `total_tokens`: Sum of both (total billed tokens)

**Q: How is Azure OpenAI billed?**
> A: Per 1,000 tokens, with separate rates for input (prompt) and output (completion) tokens. Rates vary by model - GPT-4 is more expensive than GPT-3.5-turbo.

---

### Tokens

**Q: Approximately how many tokens is 100 words of English text?**
> A: Roughly 130-150 tokens. A common estimate is ~75 words per 100 tokens, or ~4 characters per token.

**Q: What is a context window?**
> A: The maximum total tokens (prompt + completion) a model can handle in one request. Different models have different limits:
> - GPT-3.5-turbo: 4K-16K tokens
> - GPT-4: 8K-128K tokens depending on version

**Q: What happens if your prompt plus max_tokens exceeds the context window?**
> A: You'll get an error. You must ensure: `prompt_tokens + max_tokens <= context_window`

---

### Content Filtering

**Q: What types of content does Azure OpenAI filter?**
> A: Azure OpenAI has built-in filters for:
> - Hate speech
> - Violence
> - Sexual content
> - Self-harm
>
> These filters cannot be fully disabled.

**Q: How do you know if content filtering blocked a response?**
> A: The `finish_reason` will be `"content_filter"` instead of `"stop"`.

---

### SDK vs REST

**Q: What are the advantages of using the OpenAI SDK over REST API?**
> A:
> - Easier to use (handles HTTP details)
> - Built-in error handling and retries
> - Type hints and IDE support
> - Automatic request/response serialization

**Q: When would you use REST API instead of the SDK?**
> A:
> - Debugging HTTP-level issues
> - Languages without SDK support
> - Custom scenarios (special headers, proxies)
> - Learning what happens under the hood

**Q: What is the REST endpoint URL structure for chat completions?**
> A:
> ```
> POST https://{endpoint}/openai/deployments/{deployment}/chat/completions?api-version={version}
> ```
> Example:
> ```
> POST https://myresource.cognitiveservices.azure.com/openai/deployments/gpt-4o-mini/chat/completions?api-version=2025-01-01-preview
> ```

---

### Security

**Q: What is the recommended way to store Azure OpenAI API keys in an application?**
> A:
> - Development: Environment variables or `.env` files (excluded from git via `.gitignore`)
> - Production: Azure Key Vault or Managed Identity (preferred - no keys at all)

**Q: What should you do if an API key is accidentally exposed?**
> A: Immediately regenerate the key in Azure Portal (Keys and Endpoint section) to invalidate the exposed key.

---

### Prompt Engineering

**Q: What are common uses for system prompts?**
> A:
> - Setting persona/role: "You are a professional legal assistant."
> - Defining constraints: "Only answer questions about cooking."
> - Specifying output format: "Respond in JSON format."
> - Adding safety guidelines: "Never provide medical diagnoses."
> - Setting tone: "Be concise and use bullet points."

**Q: How do system prompts differ from fine-tuning?**
> A: System prompts customize behavior at runtime without modifying the model. Fine-tuning permanently adjusts model weights with training data. System prompts are:
> - Faster to implement
> - No training required
> - Can be changed per request
> - Don't require additional data

---

### Practical Scenarios

**Q: A user complains that your chatbot gives different answers to the same question. How do you fix this?**
> A: Set `temperature=0` for deterministic responses. This ensures the same input produces the same output.

**Q: Your application needs to generate creative marketing copy. What temperature would you use?**
> A: Higher temperature (0.8-1.2) for more creative and varied outputs.

**Q: You're building a code generation tool. What parameter settings would you use?**
> A: `temperature=0` (or very low like 0.1) for consistent, accurate code. You might also use a system prompt like "You are a coding assistant. Provide only code without explanations unless asked."

**Q: Your responses are being cut off mid-sentence. What's the likely cause?**
> A: The `max_tokens` limit is too low. Check `finish_reason` - if it's "length", increase `max_tokens`.

**Q: You need to ensure your chatbot only discusses company products. How do you implement this?**
> A: Use a system prompt with constraints:
> ```
> You are a customer service assistant for XYZ Company.
> Only answer questions about our products and services.
> If asked about anything else, politely redirect to our product offerings.
> ```

---

## Part 3: Quick Reference Card

### Essential Code Pattern
```python
from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint="https://xxx.cognitiveservices.azure.com/",
    api_key="your-key",
    api_version="2025-01-01-preview"
)

response = client.chat.completions.create(
    model="your-deployment-name",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ],
    temperature=0.7,
    max_tokens=150
)

print(response.choices[0].message.content)
print(response.choices[0].finish_reason)
print(response.usage.total_tokens)
```

### Parameter Quick Guide
| Parameter | Low Value | High Value | Default |
|-----------|-----------|------------|---------|
| temperature | Deterministic | Creative | 1.0 |
| top_p | Focused vocabulary | Diverse vocabulary | 1.0 |
| max_tokens | Short responses | Long responses | Model default |

### Finish Reasons
| Value | Meaning | Action |
|-------|---------|--------|
| `stop` | Normal completion | None |
| `length` | Truncated | Increase max_tokens |
| `content_filter` | Blocked | Rephrase request |
