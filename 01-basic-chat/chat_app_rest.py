"""
Azure OpenAI Chat Application - REST API Version
Demonstrates the same functionality using direct REST API calls instead of SDK.

=============================================================================
AI-102 CERTIFICATION: WHY LEARN BOTH SDK AND REST?
- Exam may test knowledge of both approaches
- REST helps you understand what the SDK does under the hood
- Some languages/platforms may not have an SDK
- Useful for debugging and understanding HTTP-level issues
- Required for some advanced scenarios (custom headers, proxies, etc.)
=============================================================================
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

# =============================================================================
# CONFIGURATION
# =============================================================================
# For REST API, we construct the full URL ourselves
# Format: {endpoint}/openai/deployments/{deployment}/chat/completions?api-version={version}
#
# AI-102 EXAM TIP: Know the URL structure for Azure OpenAI REST endpoints:
# - Base: https://{resource-name}.openai.azure.com/
# - Path: /openai/deployments/{deployment-name}/chat/completions
# - Query: ?api-version={api-version}
# =============================================================================
ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT").rstrip("/")
API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")
API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")

# Construct the full API URL
API_URL = f"{ENDPOINT}/openai/deployments/{DEPLOYMENT}/chat/completions?api-version={API_VERSION}"

# =============================================================================
# AUTHENTICATION HEADERS
# =============================================================================
# Azure OpenAI uses "api-key" header (NOT "Authorization: Bearer")
# This is different from standard OpenAI which uses Bearer token
#
# AI-102 EXAM TIP: Know the authentication methods:
# - API Key: "api-key" header (what we use here)
# - Azure AD/Entra ID: "Authorization: Bearer {token}" header
#   - More secure for production
#   - Supports Managed Identity
#   - Required for some enterprise scenarios
# =============================================================================
HEADERS = {
    "Content-Type": "application/json",
    "api-key": API_KEY
}


def call_chat_api(messages, temperature=1.0, max_tokens=None, top_p=1.0):
    """
    Make a direct REST API call to Azure OpenAI.

    AI-102 EXAM TIP: The request body structure:
    {
        "messages": [...],      # Required: conversation history
        "temperature": 1.0,     # Optional: randomness (0-2)
        "max_tokens": 100,      # Optional: response length limit
        "top_p": 1.0,           # Optional: nucleus sampling (0-1)
        "n": 1,                 # Optional: number of completions
        "stop": null,           # Optional: stop sequences
        "presence_penalty": 0,  # Optional: topic repetition penalty
        "frequency_penalty": 0  # Optional: word repetition penalty
    }
    """
    # Build the request payload
    payload = {
        "messages": messages,
        "temperature": temperature,
        "top_p": top_p
    }

    # Only include max_tokens if specified (otherwise use model default)
    if max_tokens:
        payload["max_tokens"] = max_tokens

    # Make the POST request
    response = requests.post(API_URL, headers=HEADERS, json=payload)

    # Check for errors
    if response.status_code != 200:
        print(f"\nAPI Error: {response.status_code}")
        print(f"Response: {response.text}")
        return None

    return response.json()


def display_response(response_json):
    """
    Display the REST API response.

    AI-102 EXAM TIP: The response JSON structure:
    {
        "id": "chatcmpl-xxx",
        "object": "chat.completion",
        "created": 1234567890,
        "model": "gpt-4",
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "The response text..."
            },
            "finish_reason": "stop"
        }],
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 20,
            "total_tokens": 30
        }
    }
    """
    if not response_json:
        return

    print("\n" + "=" * 50)
    print("RESPONSE DETAILS (REST API):")
    print("=" * 50)

    # Navigate the JSON structure
    choice = response_json["choices"][0]
    message = choice["message"]

    print(f"\nMessage Content:\n{message['content']}")
    print(f"\nFinish Reason: {choice['finish_reason']}")

    usage = response_json.get("usage", {})
    if usage:
        print(f"\nToken Usage:")
        print(f"  - Prompt tokens: {usage.get('prompt_tokens', 'N/A')}")
        print(f"  - Completion tokens: {usage.get('completion_tokens', 'N/A')}")
        print(f"  - Total tokens: {usage.get('total_tokens', 'N/A')}")

    print("=" * 50)


def basic_chat():
    """Simple chat using REST API."""
    print("\n--- Basic Chat (REST API) ---")
    print("Enter your message (or 'back' to return to menu):\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == 'back':
            break
        if not user_input:
            continue

        messages = [{"role": "user", "content": user_input}]
        response = call_chat_api(messages)
        display_response(response)


def chat_with_system_prompt():
    """Chat with a system prompt using REST API."""
    print("\n--- Chat with System Prompt (REST API) ---")

    system_prompts = {
        "1": "You are a professional business assistant.",
        "2": "You are a friendly, casual helper.",
        "3": "You are a technical expert.",
        "4": "You are a creative storyteller."
    }

    print("Select a persona:")
    print("  1. Professional")
    print("  2. Casual")
    print("  3. Technical")
    print("  4. Creative")
    print("  5. Back\n")

    choice = input("Select (1-5): ").strip()
    if choice == "5" or choice not in system_prompts:
        return

    system_prompt = system_prompts[choice]
    print(f"\nUsing system prompt: \"{system_prompt}\"")
    print("Enter your message (or 'back' to return):\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == 'back':
            break
        if not user_input:
            continue

        # REST API: messages array with system + user
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
        response = call_chat_api(messages)
        display_response(response)


def explore_parameters():
    """Explore API parameters using REST API."""
    print("\n--- Parameter Exploration (REST API) ---")
    print("  1. Temperature comparison")
    print("  2. Max tokens comparison")
    print("  3. Back\n")

    choice = input("Select (1-3): ").strip()
    if choice == "3":
        return

    prompt = input("Enter a test prompt: ").strip()
    if not prompt:
        prompt = "Write a short poem about technology"

    messages = [{"role": "user", "content": prompt}]

    if choice == "1":
        print(f"\nComparing temperatures for: \"{prompt}\"")
        for temp in [0.0, 0.7, 1.5]:
            print(f"\n{'=' * 40}")
            print(f"TEMPERATURE: {temp}")
            print("=" * 40)
            response = call_chat_api(messages, temperature=temp, max_tokens=100)
            if response:
                print(f"\n{response['choices'][0]['message']['content']}")
            input("\nPress Enter...")

    elif choice == "2":
        print(f"\nComparing max_tokens for: \"{prompt}\"")
        for tokens in [30, 100, 300]:
            print(f"\n{'=' * 40}")
            print(f"MAX_TOKENS: {tokens}")
            print("=" * 40)
            response = call_chat_api(messages, max_tokens=tokens)
            if response:
                content = response['choices'][0]['message']['content']
                finish = response['choices'][0]['finish_reason']
                print(f"\n{content}")
                print(f"\nFinish reason: {finish}")
            input("\nPress Enter...")


def show_raw_request():
    """
    Show what the raw HTTP request looks like.
    Useful for understanding what happens under the hood.
    """
    print("\n--- Raw Request Example ---")
    print("\nThis is what the SDK sends to Azure:\n")

    print(f"POST {API_URL}")
    print(f"Content-Type: application/json")
    print(f"api-key: ****{API_KEY[-4:] if API_KEY else '****'}")
    print()
    print("Body:")
    print("""{
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ],
    "temperature": 0.7,
    "max_tokens": 100
}""")

    input("\nPress Enter to continue...")


def main():
    """Main application loop."""
    print("\n" + "=" * 50)
    print("   Azure OpenAI Chat - REST API Version")
    print("   Understanding the API at HTTP level")
    print("=" * 50)

    # Verify configuration
    if not all([ENDPOINT, API_KEY, DEPLOYMENT]):
        print("\nError: Missing configuration!")
        print("Please copy .env.example to .env and add your Azure credentials.")
        return

    print(f"\nAPI URL: {API_URL[:50]}...")

    while True:
        print("\n--- Main Menu ---")
        print("1. Basic Chat")
        print("2. Chat with System Prompt")
        print("3. Explore Parameters")
        print("4. Show Raw Request Example")
        print("5. Exit\n")

        choice = input("Select option (1-5): ").strip()

        if choice == "1":
            basic_chat()
        elif choice == "2":
            chat_with_system_prompt()
        elif choice == "3":
            explore_parameters()
        elif choice == "4":
            show_raw_request()
        elif choice == "5":
            print("\nGoodbye!")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
