# 🔧 PydanticAI Tool-Calling Agent — Structured Agent Design with Native Tool Use

A Python project that rebuilds the multi-turn agent architect pipeline using [PydanticAI](https://ai.pydantic.dev) — demonstrating **native tool-calling**, structured outputs, and persistent conversation history without relying on `instructor`.

This represents a migration from the `instructor` + Groq pattern to PydanticAI's first-class agentic abstractions, unlocking reliable tool registration, cleaner message history management, and better compatibility with Groq's strict schema validation.

---

## 📌 What It Does

You have an ongoing conversation with a Senior AI Agent Architect persona. On each turn, the agent can optionally call a registered tool (`CurrentDateTime`) before generating its structured response — demonstrating the core agentic loop of **reason → tool call → respond**.

Every response is validated against the `Assistant` Pydantic schema, and conversation history is maintained across turns using PydanticAI's native `message_history` and `new_messages()` API.

---

## 🔑 Key Concepts

### Native Tool Calling
Tools are registered directly on the agent using the `@agent.tool_plain` decorator — no manual schema construction or JSON wrangling required:

```python
@agent.tool_plain
def CurrentDateTime(timezone: str = 'UTC') -> str:
    '''Get the current date & time.'''
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
```

PydanticAI automatically infers the tool's JSON schema from the type hints and docstring, and passes it to the model natively.

### Message History
Rather than manually serialising responses back to JSON (as required with `instructor`), PydanticAI handles history through its own message types:

```python
History: list[ModelMessage] = []

data = agent.run_sync(user_string, message_history=History)
History.extend(data.new_messages())
```

`new_messages()` returns only the messages from the latest turn, which are appended to the running history — keeping context clean and avoiding duplication.

### Structured Output
The agent's output type is declared at construction time:

```python
agent = Agent(
    model='groq:llama-3.3-70b-versatile',
    output_type=Assistant,
    instructions=system_prompt
)
```

The validated result is accessed via `data.output`, which is a fully typed `Assistant` instance.

---

## 🧱 Output Schema

| Field                  | Type              | Constraints                         |
|------------------------|-------------------|-------------------------------------|
| `agent_name`           | `str`             | 5–50 characters                     |
| `short_description`    | `str`             | 100–1500 characters                 |
| `target_users`         | `list[str]`       | 3–5 specific personas               |
| `core_tools_needed`    | `list[str]`       | 4–6 specific functions/integrations |
| `suggested_tech_stack` | `list[str]`       | 4–7 Python-based tools              |
| `first_milestone`      | `str`             | 100–500 characters, 14-day target   |
| `potential_challenges` | `list[str]`       | 3–5 technical or logical risks      |
| `confidence`           | `Confidence` enum | `"high"`, `"medium"`, or `"low"`    |

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| [PydanticAI](https://ai.pydantic.dev) | Agent framework with native tool-calling and structured outputs |
| [Groq](https://groq.com/) | Fast LLM inference (LLaMA 3.3 70B) |
| [Pydantic v2](https://docs.pydantic.dev/) | Data validation and schema definition |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | Secure API key management |

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Dark5301/pydanticai-tool-calling-agent.git
cd pydanticai-tool-calling-agent
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install pydantic-ai groq pydantic python-dotenv
```

### 4. Set up your environment variables

Create a `.env` file in the root of the project:

```env
GROQ_API_KEY=your_groq_api_key_here
```

> Get your free Groq API key at [console.groq.com](https://console.groq.com).

### 5. Run the script

```bash
python tool_calling.py
```

---

## 📤 Example Session

```
Enter your query ("exit" for exit):
> Design an agent that helps freelancers track invoices and chase late payments

[TOOL CALLED] CurrentDateTime → 2026-04-25 14:32:07

Agent Name: InvoiceGuard AI
Short Description: InvoiceGuard AI monitors outstanding invoices, sends automated
payment reminders via email, and escalates overdue accounts — helping freelancers
recover revenue without awkward manual follow-ups.
Target Users:
. Independent software developers with 5–15 active clients
. Freelance designers billing on project milestones
. Consultants managing retainer agreements across time zones
Core Tools Needed:
. Invoice status checker (integration with Razorpay / Stripe)
. Automated email reminder scheduler
. Overdue escalation engine with configurable thresholds
. Payment confirmation listener via webhook
Suggested Tech Stack:
. PydanticAI for agent logic and tool orchestration
. FastAPI for webhook endpoints
. SQLite for invoice state tracking
. httpx for API calls to payment gateways
First Milestone: Build a CLI tool that reads a CSV of invoice records, identifies
overdue ones based on today's date, and prints a formatted list of clients to
follow up with — completable in 14 days using only local data and no external APIs.
Potential Challenges:
. Payment gateway APIs differ significantly across providers
. Email deliverability issues may cause reminders to land in spam
. Freelancers may have inconsistent invoice data formats
Confidence: high

Enter your query ("exit" for exit):
> exit
```

---

## ⚠️ Known Limitations

- **No session persistence**: History exists only in memory for the duration of the script run. Restarting clears all prior context.
- **Context window growth**: Each turn appends all new messages to history. Long sessions with tool calls can grow context quickly — monitor token usage for extended sessions.
- **Synchronous only**: The script uses `agent.run_sync()`. For concurrent or async workflows, PydanticAI also exposes `agent.run()` as an async coroutine.

---

## 🔮 Roadmap

- [ ] Add more tools (e.g., web search, file I/O) to expand agent capabilities
- [ ] Persist conversation history to disk between sessions
- [ ] Migrate to `agent.run()` for async support
- [ ] Add a `deps` context object using PydanticAI's dependency injection pattern
- [ ] Build a multi-agent pipeline where this agent hands off to a specialised sub-agent

---

## 👤 Author

**Prince**
Aspiring AI/Cybersecurity Developer · Python · Bash · JavaScript
Building a portfolio at the intersection of AI agents and penetration testing.

---

## 📄 License

MIT License — feel free to fork, modify, and build on this.
