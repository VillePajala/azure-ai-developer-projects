"""
Azure OpenAI Chat Application
Demonstrates system prompts and parameter tuning for chat completions.

=============================================================================
AI-102 CERTIFICATION TOPICS COVERED:
- Implement Azure OpenAI Service solutions
- Create chat completions using the SDK
- Configure chat completion parameters (temperature, top_p, max_tokens)
- Use system messages to guide model behavior (prompt engineering)
- Understand token usage and billing implications
=============================================================================
"""

import os
from dotenv import load_dotenv
from openai import AzureOpenAI

# =============================================================================
# CONFIGURATION
# =============================================================================
# load_dotenv() reads the .env file and loads variables into os.environ
# This is a common pattern to keep secrets out of code
#
# AI-102 NOTE: In production, use Azure Key Vault or Managed Identity instead
# of environment variables. API keys should never be committed to source control.
# =============================================================================
load_dotenv()

# =============================================================================
# AZURE OPENAI CLIENT INITIALIZATION
# =============================================================================
# The AzureOpenAI client differs from the standard OpenAI client:
# - Requires azure_endpoint (your resource URL)
# - Requires api_version (Azure-specific versioning)
# - Uses deployment names instead of model names
#
# AI-102 EXAM TIP: Know the difference between:
# - Endpoint: https://<resource-name>.openai.azure.com/
# - Deployment name: What YOU named the model deployment (e.g., "my-gpt4")
# - Model name: The actual model (e.g., "gpt-4", "gpt-35-turbo")
# =============================================================================
client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
)

# In Azure OpenAI, you call your DEPLOYMENT name, not the model name
# The deployment is created in Azure AI Foundry or Azure Portal
DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# =============================================================================
# SYSTEM PROMPTS (PROMPT ENGINEERING)
# =============================================================================
# System prompts set the AI's behavior, personality, and constraints.
#
# AI-102 EXAM TIP: System prompts are used for:
# - Setting persona/role ("You are a helpful assistant")
# - Defining constraints ("Only answer questions about cooking")
# - Output formatting ("Respond in JSON format")
# - Safety guidelines ("Never provide medical advice")
#
# The system message is processed FIRST and influences all responses.
# It counts toward your token limit but is powerful for controlling behavior.
# =============================================================================
SYSTEM_PROMPTS = {
    "professional": "You are a professional business assistant. Respond formally and concisely, focusing on actionable advice and clear communication.",
    "casual": "You are a friendly, casual helper. Use conversational language, be warm and approachable, and feel free to use informal expressions.",
    "technical": "You are a technical expert. Provide detailed, accurate technical explanations with relevant terminology. Include examples and best practices where appropriate.",
    "creative": "You are a creative storyteller. Use vivid imagery, metaphors, and engaging narratives. Let your imagination flow and make responses entertaining."
}

# Test prompts for parameter exploration
TEST_PROMPTS = [
    "Write a short poem about technology",
    "Create a plan for learning a new skill",
    "Describe the perfect morning routine"
]


def display_response_details(response):
    """
    Display the full response structure for learning purposes.

    AI-102 EXAM TIP: Understand the response object structure:
    - choices[]: Array of completions (usually 1 unless n>1)
    - choices[0].message.content: The actual text response
    - choices[0].finish_reason: Why generation stopped
        - "stop": Natural completion
        - "length": Hit max_tokens limit
        - "content_filter": Blocked by content filtering
    - usage: Token counts for billing
        - prompt_tokens: Input tokens (you pay for these)
        - completion_tokens: Output tokens (you pay for these)
        - total_tokens: Sum of both
    """
    print("\n" + "=" * 50)
    print("RESPONSE DETAILS:")
    print("=" * 50)

    choice = response.choices[0]
    print(f"\nMessage Content:\n{choice.message.content}")

    # finish_reason tells you WHY the model stopped generating
    # This is important for detecting truncated responses
    print(f"\nFinish Reason: {choice.finish_reason}")

    # Token usage is critical for cost management
    # Azure OpenAI bills per 1,000 tokens (varies by model)
    if response.usage:
        print(f"\nToken Usage:")
        print(f"  - Prompt tokens: {response.usage.prompt_tokens}")
        print(f"  - Completion tokens: {response.usage.completion_tokens}")
        print(f"  - Total tokens: {response.usage.total_tokens}")

    print("=" * 50)


def basic_chat():
    """
    Simple chat interaction demonstrating basic API usage.

    AI-102 NOTE: This is the simplest form of chat completion.
    The messages array contains the conversation history.
    Each message has a "role" and "content".
    """
    print("\n--- Basic Chat ---")
    print("Enter your message (or 'back' to return to menu):\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == 'back':
            break
        if not user_input:
            continue

        # =================================================================
        # CHAT COMPLETIONS API CALL
        # =================================================================
        # model: Your deployment name (NOT the model name like "gpt-4")
        # messages: Array of message objects with role and content
        #
        # Roles:
        # - "system": Sets behavior (optional but recommended)
        # - "user": Human input
        # - "assistant": Previous AI responses (for context)
        # =================================================================
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {"role": "user", "content": user_input}
            ]
        )

        display_response_details(response)


def system_prompt_explorer():
    """
    Explore how different system prompts affect responses.

    AI-102 EXAM TIP: System prompts are a key part of prompt engineering.
    The same user question with different system prompts produces
    dramatically different responses. This is how you customize AI behavior
    without fine-tuning the model.
    """
    print("\n--- System Prompt Explorer ---")
    print("See how different personas shape AI responses.\n")

    print("Available Personas:")
    print("  1. Professional assistant")
    print("  2. Casual/friendly helper")
    print("  3. Technical expert")
    print("  4. Creative storyteller")
    print("  5. Back to main menu\n")

    persona_map = {
        "1": ("professional", "Professional Assistant"),
        "2": ("casual", "Casual Helper"),
        "3": ("technical", "Technical Expert"),
        "4": ("creative", "Creative Storyteller")
    }

    choice = input("Select persona (1-5): ").strip()

    if choice == "5" or choice not in persona_map:
        return

    persona_key, persona_name = persona_map[choice]
    system_prompt = SYSTEM_PROMPTS[persona_key]

    print(f"\n[Using: {persona_name}]")
    print(f"System prompt: \"{system_prompt[:80]}...\"")
    print("\nEnter your message (or 'back' to return):\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == 'back':
            break
        if not user_input:
            continue

        # Notice the messages array now includes BOTH system and user messages
        # The system message comes FIRST and sets the context
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
        )

        display_response_details(response)


def parameter_playground():
    """
    Experiment with different API parameters.

    AI-102 EXAM TIP: Know these parameters and when to use them:
    - temperature: Controls randomness (0-2, default 1)
    - top_p: Nucleus sampling, alternative to temperature (0-1)
    - max_tokens: Maximum response length
    - n: Number of completions to generate
    - stop: Sequences where generation stops
    - presence_penalty: Reduces repetition of topics (-2 to 2)
    - frequency_penalty: Reduces repetition of exact phrases (-2 to 2)
    """
    print("\n--- Parameter Playground ---")
    print("Experiment with temperature, top_p, and max_tokens.\n")

    print("Select parameter to explore:")
    print("  1. Temperature (creativity vs determinism)")
    print("  2. Top_p (vocabulary diversity)")
    print("  3. Max_tokens (response length)")
    print("  4. Back to main menu\n")

    choice = input("Select option (1-4): ").strip()

    if choice == "4":
        return

    print("\nSelect a test prompt:")
    for i, prompt in enumerate(TEST_PROMPTS, 1):
        print(f"  {i}. {prompt}")
    print(f"  {len(TEST_PROMPTS) + 1}. Enter custom prompt")

    prompt_choice = input("\nSelect prompt: ").strip()

    try:
        prompt_idx = int(prompt_choice) - 1
        if prompt_idx == len(TEST_PROMPTS):
            test_prompt = input("Enter your custom prompt: ").strip()
        elif 0 <= prompt_idx < len(TEST_PROMPTS):
            test_prompt = TEST_PROMPTS[prompt_idx]
        else:
            print("Invalid selection.")
            return
    except ValueError:
        print("Invalid selection.")
        return

    if choice == "1":
        explore_temperature(test_prompt)
    elif choice == "2":
        explore_top_p(test_prompt)
    elif choice == "3":
        explore_max_tokens(test_prompt)


def explore_temperature(prompt):
    """
    Compare responses at different temperature settings.

    AI-102 EXAM TIP - TEMPERATURE:
    - Range: 0.0 to 2.0 (default: 1.0)
    - Lower = more deterministic, focused, consistent
    - Higher = more random, creative, varied

    Use cases:
    - 0.0-0.3: Factual Q&A, code generation, data extraction
    - 0.5-0.7: Balanced tasks, general conversation
    - 0.8-1.2: Creative writing, brainstorming
    - 1.5+: Very creative/experimental (may be incoherent)

    IMPORTANT: Don't use both temperature AND top_p together.
    Pick one approach for controlling randomness.
    """
    print(f"\n--- Temperature Exploration ---")
    print(f"Prompt: \"{prompt}\"")
    print("\nTemperature controls randomness/creativity:")
    print("  - 0.0 = Deterministic, focused responses")
    print("  - 1.0 = Balanced creativity")
    print("  - 1.5+ = More random, creative outputs\n")

    temperatures = [0.0, 0.5, 1.0, 1.5]

    for temp in temperatures:
        print(f"\n{'=' * 50}")
        print(f"TEMPERATURE: {temp}")
        print("=" * 50)

        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=temp,
            max_tokens=150
        )

        print(f"\nResponse:\n{response.choices[0].message.content}")
        print(f"\nTokens used: {response.usage.total_tokens}")

        input("\nPress Enter to continue...")


def explore_top_p(prompt):
    """
    Compare responses at different top_p settings.

    AI-102 EXAM TIP - TOP_P (Nucleus Sampling):
    - Range: 0.0 to 1.0 (default: 1.0)
    - Controls vocabulary diversity differently than temperature
    - 0.1 = Only consider top 10% most likely tokens
    - 0.9 = Consider top 90% of probability mass

    How it works:
    - Model ranks all possible next tokens by probability
    - top_p selects from smallest set that sums to p probability
    - Lower top_p = fewer choices = more predictable

    IMPORTANT: Microsoft recommends changing EITHER temperature OR top_p,
    not both. They are alternative approaches to the same goal.
    """
    print(f"\n--- Top_p Exploration ---")
    print(f"Prompt: \"{prompt}\"")
    print("\nTop_p (nucleus sampling) controls vocabulary diversity:")
    print("  - 0.1 = Very focused, common words only")
    print("  - 0.5 = Moderate diversity")
    print("  - 0.95 = Wide vocabulary, more variety\n")

    top_p_values = [0.1, 0.5, 0.95]

    for top_p in top_p_values:
        print(f"\n{'=' * 50}")
        print(f"TOP_P: {top_p}")
        print("=" * 50)

        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[{"role": "user", "content": prompt}],
            top_p=top_p,
            temperature=1.0,  # Keep temperature constant for comparison
            max_tokens=150
        )

        print(f"\nResponse:\n{response.choices[0].message.content}")
        print(f"\nTokens used: {response.usage.total_tokens}")

        input("\nPress Enter to continue...")


def explore_max_tokens(prompt):
    """
    Compare responses at different max_tokens settings.

    AI-102 EXAM TIP - MAX_TOKENS:
    - Limits the maximum LENGTH of the response
    - Does NOT guarantee that length (model may finish earlier)
    - If response is cut off, finish_reason will be "length"

    Important considerations:
    - Total tokens = prompt_tokens + completion_tokens
    - Each model has a context window limit (e.g., 8K, 32K, 128K)
    - max_tokens must fit within: context_limit - prompt_tokens
    - Setting max_tokens helps control costs and response time

    Token estimation (rough guide for English):
    - 1 token ≈ 4 characters or ¾ of a word
    - 100 tokens ≈ 75 words
    """
    print(f"\n--- Max Tokens Exploration ---")
    print(f"Prompt: \"{prompt}\"")
    print("\nMax_tokens limits response length:")
    print("  - 50 = Very short responses")
    print("  - 150 = Medium length")
    print("  - 500 = Longer, more detailed responses\n")

    max_tokens_values = [50, 150, 500]

    for max_tok in max_tokens_values:
        print(f"\n{'=' * 50}")
        print(f"MAX_TOKENS: {max_tok}")
        print("=" * 50)

        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tok
        )

        print(f"\nResponse:\n{response.choices[0].message.content}")
        # Check finish_reason to see if response was truncated
        print(f"\nFinish reason: {response.choices[0].finish_reason}")
        print(f"Completion tokens: {response.usage.completion_tokens} / {max_tok} limit")

        input("\nPress Enter to continue...")


def main():
    """Main application loop."""
    print("\n" + "=" * 50)
    print("   Azure OpenAI Chat Application")
    print("   Exploring Chat Completions")
    print("=" * 50)

    # Verify configuration before starting
    # In production, you'd want more robust error handling
    if not all([os.getenv("AZURE_OPENAI_ENDPOINT"),
                os.getenv("AZURE_OPENAI_API_KEY"),
                DEPLOYMENT_NAME]):
        print("\nError: Missing configuration!")
        print("Please copy .env.example to .env and add your Azure credentials.")
        return

    while True:
        print("\n--- Main Menu ---")
        print("1. Basic Chat")
        print("2. System Prompt Explorer")
        print("3. Parameter Playground")
        print("4. Exit\n")

        choice = input("Select option (1-4): ").strip()

        if choice == "1":
            basic_chat()
        elif choice == "2":
            system_prompt_explorer()
        elif choice == "3":
            parameter_playground()
        elif choice == "4":
            print("\nGoodbye!")
            break
        else:
            print("Invalid option. Please select 1-4.")


if __name__ == "__main__":
    main()
