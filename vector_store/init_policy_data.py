from vector_store import PineconeVectorStore

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

# Combine policies
documents = billing_policies + security_policies

# Initialize vector store and upsert documents
store = PineconeVectorStore(texts_with_meta=documents, namespace="policy-knowledge")
store.upsert_data(texts_with_meta=documents)