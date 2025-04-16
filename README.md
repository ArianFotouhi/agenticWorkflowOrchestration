# 🤖 Agentic Workflow Orchestration with LLMs & Pinecone

This repository implements a modular **agent-based workflow orchestration system** using OpenAI's LLMs and Pinecone vector search. It features:

- Multi-agent routing (billing, security, renewal, cancelation)
- Document-grounded responses via Pinecone search
- Tool invocation per agent
- Streaming LLM output
- Visualized agent graph structure (via `draw_graph`)

In this work, to optimize embedding search speed in the vector store, agents filter documents by category — reducing the vector search space and minimizing processing and computation overhead.

-----

## 🚀 Quick Start


▶️ Run the Workflow
```bash
OPENAI_API_KEY=your-openai-key PINECONE_API_KEY=your-pinecone-key python3 main.py
```

The Workflow will:

- Spawn a Triage Agent

- Route the query to one of the domain agents

- Agents fetch relevant info via Pinecone

- LLM provides a document-grounded answer




Each agent routes to Pinecone for relevant document chunks

The Runner.run_sync() or run_streamed() methods execute the agent flow

🗃 Vector Store (LLM/pinecone_vec_store.py)
Wrapper over Pinecone’s API

Supports:

Index creation (if absent), Data upsert, Category-filtered semantic search, Re-ranking with bge-reranker-v2-m3 in Pinecone

To run the application, it can be either sync or async (eg in case of streaming). The default output is by streaming however, it can be sync using the below code: 
```python
result1= Runner.run_sync(
starting_agent=triage_agent,
input="check the documents and tell me refund is acceptanle within how many days of purchase?",
)
for result in result1.new_items:
    print(result)
print('-'*80)
for result in result1.raw_responses:
    print(result)
print('-'*80)
print(result1)




result2= Runner.run_sync(
starting_agent=triage_agent,
input="check the documents and tell me refund is acceptanle within how many days of purchase?",
)


for result in result2.new_items:
    print(result)
print('-'*80)
for result in result2.raw_responses:
    print(result)
print('-'*80)
print(result2)

```


🧪 Example Queries
Assuming these are the records in the vector store
```python
billing_policies = [
    {"_id": "billing-1", "chunk_text": "Customers will be billed on the first day of every month.", "category": "billing"},
    {"_id": "billing-2", "chunk_text": "Refunds must be requested within 30 days of the original transaction.", "category": "billing"},
    {"_id": "billing-3", "chunk_text": "All transactions are subject to a 5% processing fee.", "category": "billing"},
    {"_id": "billing-4", "chunk_text": "Subscription renewals will be automatically processed.", "category": "billing"},
    {"_id": "billing-5", "chunk_text": "Late payments will incur a penalty of $25.", "category": "billing"},
]

security_policies = [
    {"_id": "security-1", "chunk_text": "All user data is encrypted in transit and at rest.", "category": "security"},
    {"_id": "security-2", "chunk_text": "Multi-factor authentication is required for admin accounts.", "category": "security"},
    {"_id": "security-3", "chunk_text": "System access is logged and audited regularly.", "category": "security"},
    {"_id": "security-4", "chunk_text": "Security patches are applied within 48 hours of release.", "category": "security"},
    {"_id": "security-5", "chunk_text": "Password complexity requirements include at least 12 characters.", "category": "security"},
]
```

```python
Runner.run_sync(
    starting_agent=triage_agent,
    input="check the documents and tell refund is acceptable within how many days of purchase?"
)
```
Vector Store Output for K=3
```bash
ℹ️ Using existing Pinecone index 'index-policies'
🔍 Performing category-filtered search for: 'check the documents and tell refund is acceptable within how many days of purchase' in 'billing'
------------------------------
Refunds must be requested within 30 days of the original transaction.

All transactions are subject to a 5% processing fee.

Customers will be billed on the first day of every month.
```
Final Output 
```bash
Refunds are acceptable within 30 days of the original purchase.                                                                                                                           
```

```python
Runner.run_streamed(
    starting_agent=triage_agent,
    input="check the documents and tell when security patches are applied?"
)
```
Vector Store Output for K=3
```bash
ℹ️ Using existing Pinecone index 'index-policies'
🔍 Performing category-filtered search for: 'security patches application dates' in 'security'
------------------------------
Security patches are applied within 48 hours of release.

System access is logged and audited regularly.

Multi-factor authentication is required for admin accounts.
```
Final Output
```bash
Security patches are applied within 48 hours of their release.
```

Also to visualize the agents workflow:
```python 
Use draw_graph(triage_agent).view() #to visualize agent relationships.
```

🧯 Error Handling
All tool functions are wrapped with try/except and use format_error() for traceback visibility:

```python
def format_error(e):
    ...
    return {
        'error': str(e),
        'trace': traceback.format_exc()
    }
```

📈 Future Improvements
Add tool_use_behavior='always' for stricter tool invocation

Improve tool return formatting (structured JSON output)

Add agent memory (conversation context)

Support multi-turn interactions

Integrate LangChain or CrewAI if needed

