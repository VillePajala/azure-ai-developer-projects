# 01 - Basic Chat: Azure OpenAI Chat Completions

## AI-102 Certification Topics Covered

| Exam Objective | What You'll Learn |
|----------------|-------------------|
| Implement Azure OpenAI Service | Creating and configuring Azure OpenAI resources |
| Generate chat completions | Using the Chat Completions API with SDK and REST |
| Prompt engineering | System prompts, message roles, shaping AI behavior |
| Configure parameters | Temperature, top_p, max_tokens and their effects |

---

## Prerequisites

Before running this code, you need an Azure OpenAI resource with a deployed model.

### Step 1: Create Azure OpenAI Resource

1. Go to [Azure Portal](https://portal.azure.com)
2. Click **Create a resource**
3. Search for **"Azure OpenAI"**
4. Click **Create**
5. Fill in:
   - **Subscription**: Your Azure subscription
   - **Resource group**: Create new or use existing
   - **Region**: Choose a region where Azure OpenAI is available (e.g., East US, West Europe)
   - **Name**: Unique name for your resource (this becomes part of your endpoint URL)
   - **Pricing tier**: Standard S0
6. Click **Review + create**, then **Create**
7. Wait for deployment to complete

### Step 2: Deploy a Model (Azure AI Foundry)

1. Once the resource is created, click **Go to resource**
2. Click **Go to Azure AI Foundry** (or navigate to [ai.azure.com](https://ai.azure.com))
3. Select your Azure OpenAI resource
4. Go to **Deployments** → **+ Create deployment**
5. Select a model:
   - **gpt-4** (recommended for best results)
   - **gpt-35-turbo** (faster, cheaper)
6. Give it a **Deployment name** (e.g., "my-gpt4") - **remember this name!**
7. Set tokens-per-minute rate limit (start with default)
8. Click **Create**

### Step 3: Get Your Credentials

1. In Azure Portal, go to your Azure OpenAI resource
2. Go to **Keys and Endpoint** (left menu)
3. Copy:
   - **Endpoint**: `https://your-resource-name.openai.azure.com/`
   - **KEY 1** or **KEY 2**: Your API key

---

## Project Setup

### 1. Navigate to the project folder
```bash
cd 01-basic-chat
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

Edit `.env` with your values:
```
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT=your-deployment-name
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

### 5. Run the application
```bash
# SDK version (recommended to start with)
python chat_app.py

# REST API version (to understand HTTP-level details)
python chat_app_rest.py
```

---

## Key Concepts

### Chat Completions API

The Chat Completions API uses a **messages array** to maintain conversation context:

```python
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is Python?"},
    {"role": "assistant", "content": "Python is a programming language..."},
    {"role": "user", "content": "What are its main uses?"}
]
```

**Message Roles:**
| Role | Purpose |
|------|---------|
| `system` | Sets AI behavior, personality, constraints (processed first) |
| `user` | Human input |
| `assistant` | AI's previous responses (for multi-turn context) |

### Key Parameters

| Parameter | Range | Default | Purpose |
|-----------|-------|---------|---------|
| `temperature` | 0.0 - 2.0 | 1.0 | Controls randomness. Lower = deterministic, higher = creative |
| `top_p` | 0.0 - 1.0 | 1.0 | Nucleus sampling. Controls vocabulary diversity |
| `max_tokens` | 1 - model max | varies | Maximum response length |

**Important:** Don't use `temperature` and `top_p` together. Pick one approach.

### Response Structure

```python
response.choices[0].message.content   # The actual text
response.choices[0].finish_reason     # "stop", "length", or "content_filter"
response.usage.prompt_tokens          # Input tokens (billed)
response.usage.completion_tokens      # Output tokens (billed)
response.usage.total_tokens           # Total (for cost tracking)
```

### SDK vs REST API

| Aspect | SDK (`openai` package) | REST API (`requests`) |
|--------|------------------------|------------------------|
| Ease of use | Easier, handles details | More verbose |
| Error handling | Built-in | Manual |
| Type hints | Yes | No |
| Debugging | Abstracted | See raw HTTP |
| Use case | Most applications | Custom scenarios, debugging |

---

## Troubleshooting

### "Missing configuration!" error
- Ensure `.env` file exists (copied from `.env.example`)
- Check all four variables are set correctly
- No quotes around values in `.env`

### "Resource not found" (404)
- Verify `AZURE_OPENAI_ENDPOINT` URL is correct
- Check `AZURE_OPENAI_DEPLOYMENT` matches your deployment name exactly
- Ensure the deployment is active in Azure AI Foundry

### "Access denied" (401)
- Check `AZURE_OPENAI_API_KEY` is correct
- Try regenerating the key in Azure Portal

### "Rate limit exceeded" (429)
- You've exceeded tokens-per-minute limit
- Wait and retry, or increase limit in Azure AI Foundry

### "Content filtered"
- Azure OpenAI has built-in content filtering
- Your prompt or response triggered safety filters
- Rephrase your request

---

## Review Questions (Self-Test)

1. **What's the difference between endpoint, deployment name, and model name?**
   <details>
   <summary>Answer</summary>
   - Endpoint: Your resource URL (https://xxx.openai.azure.com/)
   - Deployment name: What YOU named the deployment (e.g., "my-gpt4")
   - Model name: The actual model (e.g., "gpt-4", "gpt-35-turbo")
   </details>

2. **When should you use temperature=0?**
   <details>
   <summary>Answer</summary>
   For deterministic, consistent outputs: factual Q&A, code generation, data extraction where you want the same output for the same input.
   </details>

3. **What does finish_reason="length" indicate?**
   <details>
   <summary>Answer</summary>
   The response was cut off because it reached the max_tokens limit. The full response wasn't generated.
   </details>

4. **Why would you use the REST API instead of the SDK?**
   <details>
   <summary>Answer</summary>
   - Debugging HTTP-level issues
   - Languages without SDK support
   - Custom scenarios (proxies, special headers)
   - Understanding what happens under the hood
   </details>

5. **What's the purpose of the system message?**
   <details>
   <summary>Answer</summary>
   Sets the AI's behavior, personality, and constraints. It's processed first and influences all responses. Used for prompt engineering without fine-tuning.
   </details>

6. **How does Azure OpenAI authentication differ from standard OpenAI?**
   <details>
   <summary>Answer</summary>
   - Azure uses `api-key` header
   - Standard OpenAI uses `Authorization: Bearer {token}`
   - Azure also supports Azure AD/Entra ID authentication for production
   </details>

---

## Files in This Project

| File | Purpose |
|------|---------|
| `chat_app.py` | Main app using OpenAI SDK (heavily commented for learning) |
| `chat_app_rest.py` | Same functionality using direct REST API calls |
| `requirements.txt` | Python dependencies |
| `.env.example` | Template for environment variables |

---

## Microsoft Learn Resources

- [Azure OpenAI Service documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
- [Chat completions API reference](https://learn.microsoft.com/en-us/azure/ai-services/openai/reference#chat-completions)
- [Prompt engineering techniques](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/prompt-engineering)
- [AI-102 exam skills outline](https://learn.microsoft.com/en-us/credentials/certifications/azure-ai-engineer/)
