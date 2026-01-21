# Azure AI Developer Projects

Hands-on projects for learning Azure AI services and preparing for the **AI-102: Azure AI Engineer Associate** certification.

## About This Repository

Each folder contains a self-contained project exploring specific Azure AI capabilities. Projects are designed for learning—code is heavily commented with certification-relevant notes and explanations.

## AI-102 Exam Objectives Coverage

The AI-102 exam covers these main areas. Projects in this repo map to specific objectives:

### Plan and manage an Azure AI solution (15-20%)

| Objective | Project(s) |
|-----------|------------|
| Select appropriate Azure AI services | Coming soon |
| Plan and configure security | Coming soon |
| Create and manage Azure AI resources | 01-basic-chat |

### Implement content moderation solutions (10-15%)

| Objective | Project(s) |
|-----------|------------|
| Analyze text content | Coming soon |
| Analyze images | Coming soon |

### Implement computer vision solutions (15-20%)

| Objective | Project(s) |
|-----------|------------|
| Analyze images | Coming soon |
| Implement custom image classification | Coming soon |
| Implement object detection | Coming soon |

### Implement natural language processing solutions (30-35%)

| Objective | Project(s) |
|-----------|------------|
| Analyze text | Coming soon |
| Implement language understanding | Coming soon |
| Create a question answering solution | Coming soon |
| **Implement Azure OpenAI Service** | **01-basic-chat**, **02-chatbot-memory** |

### Implement knowledge mining and document intelligence (10-15%)

| Objective | Project(s) |
|-----------|------------|
| Implement Azure AI Search | Coming soon |
| Implement document intelligence | Coming soon |

### Implement generative AI solutions (10-15%)

| Objective | Project(s) |
|-----------|------------|
| Use Azure OpenAI Service | **01-basic-chat**, **02-chatbot-memory** |
| Implement Retrieval Augmented Generation | Coming soon |

---

## Projects

### [01-basic-chat](./01-basic-chat/)
**Azure OpenAI Chat Completions**

Learn the fundamentals of Azure OpenAI chat completions:
- SDK and REST API approaches
- System prompts and prompt engineering
- Parameter tuning (temperature, top_p, max_tokens)
- Response structure and token management

**Certification topics:** Implement Azure OpenAI Service, prompt engineering, chat completions

### [02-chatbot-memory](./02-chatbot-memory/)
**Chatbot with Conversation Memory**

Build a multi-turn chatbot that maintains conversation context:
- Conversation history management
- Token counting with tiktoken
- Context window limits and trimming
- Travel Assistant persona implementation

**Certification topics:** Multi-turn conversations, state management, token management, context windows

---

## Getting Started

### Prerequisites
- Azure subscription ([free trial available](https://azure.microsoft.com/free/))
- Python 3.8+
- Azure CLI (optional but helpful)

### General Setup Pattern

Each project follows this structure:
```bash
cd <project-folder>
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your Azure credentials
python <main-app>.py
```

---

## Study Resources

### Official Microsoft Resources
- [AI-102 Exam Page](https://learn.microsoft.com/en-us/credentials/certifications/azure-ai-engineer/)
- [AI-102 Study Guide](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ai-102)
- [Azure AI Services Documentation](https://learn.microsoft.com/en-us/azure/ai-services/)
- [Microsoft Learn AI Learning Paths](https://learn.microsoft.com/en-us/training/browse/?products=azure&subjects=artificial-intelligence)

### Azure OpenAI Specific
- [Azure OpenAI Documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
- [Azure OpenAI REST API Reference](https://learn.microsoft.com/en-us/azure/ai-services/openai/reference)
- [Prompt Engineering Guide](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/prompt-engineering)

---

## Repository Structure

```
azure-ai-developer-projects/
├── README.md                 # This file - overview and exam mapping
├── .gitignore                # Git ignore rules
├── 01-basic-chat/            # Azure OpenAI chat completions
│   ├── README.md             # Project setup and concepts
│   ├── STUDY_GUIDE.md        # Certification Q&A
│   ├── chat_app.py           # SDK version (commented)
│   ├── chat_app_rest.py      # REST API version
│   ├── requirements.txt      # Dependencies
│   └── .env.example          # Environment template
├── 02-chatbot-memory/        # Multi-turn chatbot with memory
│   ├── README.md             # Project setup and concepts
│   ├── STUDY_GUIDE.md        # Certification Q&A
│   ├── chatbot.py            # Travel assistant chatbot
│   ├── requirements.txt      # Dependencies
│   └── .env.example          # Environment template
└── ...
```

---

## Contributing

This is a personal learning repository. Feel free to fork for your own AI-102 preparation journey.

---

## License

MIT - Use freely for learning purposes.
