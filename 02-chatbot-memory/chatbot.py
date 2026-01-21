"""
Azure OpenAI Chatbot with Memory
Demonstrates conversation history management for multi-turn interactions.

=============================================================================
AI-102 CERTIFICATION TOPICS COVERED:
- Implement multi-turn conversations with Azure OpenAI
- Manage conversation history (context/memory)
- Understand token limits and context window management
- Use system prompts to define chatbot persona
- Handle conversation state in chat applications
=============================================================================
"""

import os
from dotenv import load_dotenv
from openai import AzureOpenAI
import tiktoken

load_dotenv()

# =============================================================================
# CLIENT INITIALIZATION
# =============================================================================
client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2025-01-01-preview")
)

DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# =============================================================================
# CONFIGURATION
# =============================================================================
# AI-102 EXAM TIP: Know common context window sizes:
# - GPT-3.5-turbo: 4K-16K tokens
# - GPT-4: 8K-128K tokens
# - GPT-4o-mini: 128K tokens
#
# You must ensure: prompt_tokens + max_completion_tokens <= context_window
# =============================================================================
MAX_CONTEXT_TOKENS = 4000  # Conservative limit for demonstration
MAX_RESPONSE_TOKENS = 500  # Reserve tokens for response

# =============================================================================
# SYSTEM PROMPT (PERSONA DEFINITION)
# =============================================================================
# AI-102 EXAM TIP: System prompts define the chatbot's:
# - Persona and personality
# - Knowledge domain
# - Behavioral constraints
# - Response format preferences
#
# The system message is included with EVERY request and counts toward tokens.
# =============================================================================
SYSTEM_PROMPT = """You are a friendly and knowledgeable Travel Assistant named "Voyage".

Your expertise includes:
- Destination recommendations worldwide
- Travel planning and itineraries
- Local customs and cultural tips
- Budget advice and money-saving tips
- Accommodation and transportation suggestions
- Food and restaurant recommendations

Guidelines:
- Be enthusiastic but professional
- Ask clarifying questions to give better recommendations
- Remember details the user shares (preferences, budget, travel dates)
- Provide specific, actionable advice
- If you don't know something, admit it honestly

Start by greeting the user and asking how you can help with their travel plans."""


def count_tokens(messages, model="gpt-4"):
    """
    Count tokens in a messages array using tiktoken.

    AI-102 EXAM TIP: Token counting is essential for:
    - Cost estimation (billing is per token)
    - Staying within context window limits
    - Managing conversation history length

    Different models use different tokenizers. GPT-4 and GPT-3.5-turbo
    use the 'cl100k_base' encoding.
    """
    try:
        # cl100k_base is used by GPT-4 and GPT-3.5-turbo models
        encoding = tiktoken.get_encoding("cl100k_base")
    except Exception:
        # Fallback if tiktoken fails
        return sum(len(m.get("content", "")) // 4 for m in messages)

    num_tokens = 0
    for message in messages:
        # Every message has overhead tokens for role formatting
        num_tokens += 4  # <|im_start|>{role}\n ... <|im_end|>\n
        for key, value in message.items():
            num_tokens += len(encoding.encode(str(value)))
    num_tokens += 2  # Priming tokens for assistant response
    return num_tokens


def trim_conversation_history(conversation, max_tokens):
    """
    Trim old messages when approaching token limit.

    AI-102 EXAM TIP: Managing conversation history is YOUR responsibility.
    The model has NO memory - you must send the full context each time.

    Strategy: Remove oldest messages (after system prompt) when limit approached.
    This preserves recent context while staying within limits.

    IMPORTANT: Always keep the system message (index 0).
    """
    while len(conversation) > 1:  # Keep at least system message
        current_tokens = count_tokens(conversation)
        if current_tokens + MAX_RESPONSE_TOKENS <= max_tokens:
            break
        # Remove the oldest non-system message (index 1)
        removed = conversation.pop(1)
        print(f"\n[System: Removed old message to stay within token limit]")

    return conversation


def display_conversation_stats(conversation):
    """Display current conversation statistics."""
    token_count = count_tokens(conversation)
    message_count = len(conversation) - 1  # Exclude system message

    print(f"\n--- Conversation Stats ---")
    print(f"Messages in history: {message_count}")
    print(f"Total tokens: {token_count} / {MAX_CONTEXT_TOKENS}")
    print(f"Available for response: {MAX_CONTEXT_TOKENS - token_count}")
    print("-" * 26)


def chat():
    """
    Main chat loop with conversation memory.

    AI-102 EXAM TIP: The conversation pattern:
    1. Initialize with system message
    2. Add user message to history
    3. Send ENTIRE history to API
    4. Add assistant response to history
    5. Repeat

    The model sees the full conversation each time - this is how it
    "remembers" previous exchanges. Without this, each message would
    be treated as a new conversation.
    """
    # ==========================================================================
    # CONVERSATION INITIALIZATION
    # ==========================================================================
    # Start with system message that defines the assistant's behavior
    # This message is included in EVERY API call
    # ==========================================================================
    conversation = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    print("\n" + "=" * 60)
    print("   Travel Assistant - Voyage")
    print("   (Type 'quit' to exit, 'clear' to reset, 'stats' for info)")
    print("=" * 60)

    # Get initial greeting from the assistant
    response = client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=conversation,
        max_tokens=MAX_RESPONSE_TOKENS,
        temperature=0.7
    )

    assistant_message = response.choices[0].message.content
    conversation.append({"role": "assistant", "content": assistant_message})

    print(f"\nVoyage: {assistant_message}\n")

    # ==========================================================================
    # MAIN CONVERSATION LOOP
    # ==========================================================================
    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        # Handle special commands
        if user_input.lower() == 'quit':
            print("\nVoyage: Safe travels! Come back anytime you need travel advice. ✈️")
            break

        if user_input.lower() == 'clear':
            # Reset conversation but keep system prompt
            conversation = [{"role": "system", "content": SYSTEM_PROMPT}]
            print("\n[Conversation cleared. Starting fresh!]\n")
            print("Voyage: Hello again! How can I help with your travel plans?\n")
            continue

        if user_input.lower() == 'stats':
            display_conversation_stats(conversation)
            continue

        # ==================================================================
        # ADD USER MESSAGE TO HISTORY
        # ==================================================================
        # AI-102 EXAM TIP: Every user message must be added to the
        # conversation array with role="user"
        # ==================================================================
        conversation.append({"role": "user", "content": user_input})

        # ==================================================================
        # MANAGE CONTEXT WINDOW
        # ==================================================================
        # AI-102 EXAM TIP: Before sending, check if we're within limits.
        # If not, trim oldest messages to make room.
        # ==================================================================
        conversation = trim_conversation_history(conversation, MAX_CONTEXT_TOKENS)

        # ==================================================================
        # SEND ENTIRE CONVERSATION HISTORY
        # ==================================================================
        # AI-102 EXAM TIP: The model has NO memory. We must send the
        # COMPLETE conversation history with each request. The model
        # uses this to understand context and maintain coherence.
        # ==================================================================
        try:
            response = client.chat.completions.create(
                model=DEPLOYMENT_NAME,
                messages=conversation,  # Full history sent each time!
                max_tokens=MAX_RESPONSE_TOKENS,
                temperature=0.7
            )

            # ==============================================================
            # ADD ASSISTANT RESPONSE TO HISTORY
            # ==============================================================
            # AI-102 EXAM TIP: The assistant's response must also be
            # added to maintain continuity. Without this, the model
            # won't know what it said previously.
            # ==============================================================
            assistant_message = response.choices[0].message.content
            conversation.append({"role": "assistant", "content": assistant_message})

            print(f"\nVoyage: {assistant_message}\n")

            # Show token usage for learning purposes
            if response.usage:
                print(f"[Tokens - Prompt: {response.usage.prompt_tokens}, "
                      f"Response: {response.usage.completion_tokens}, "
                      f"Total: {response.usage.total_tokens}]")

        except Exception as e:
            print(f"\nError: {e}")
            # Remove the failed user message from history
            conversation.pop()


def main():
    """Application entry point."""
    # Verify configuration
    if not all([os.getenv("AZURE_OPENAI_ENDPOINT"),
                os.getenv("AZURE_OPENAI_API_KEY"),
                DEPLOYMENT_NAME]):
        print("\nError: Missing configuration!")
        print("Please copy .env.example to .env and add your Azure credentials.")
        return

    print("\n" + "=" * 60)
    print("   Chatbot with Memory - Azure OpenAI Demo")
    print("=" * 60)
    print("\nThis demo shows how conversation history creates 'memory'.")
    print("The assistant will remember what you discussed earlier.\n")

    chat()


if __name__ == "__main__":
    main()
