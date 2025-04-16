from agents import Agent, Runner, function_tool, guardrail
import os
from openai import OpenAI
from vector_store.vector_store import PineconeVectorStore
import traceback
import sys

client = OpenAI()

def format_error(e):
    exc_type, exc_obj, tb = sys.exc_info()
    fname = traceback.extract_tb(tb)[-1].filename
    lineno = traceback.extract_tb(tb)[-1].lineno
    trace = traceback.format_exc()

    error_info = {
        'error': str(e),
        'type': exc_type.__name__,
        'file': fname,
        'line': lineno,
        'trace': trace
    }


    return error_info





@function_tool
def get_billing_info(user_query: str):

    try:

        vector_store = PineconeVectorStore(namespace="policy-knowledge")
        chunks = vector_store.search(user_query, category="billing")
        context = "\n\n".join(c[0] for c in chunks)
        print('-'*30)
        print(context)
        print('-'*30)

    except Exception as e:
        
        print(f"Error initializing vector store: {format_error(e)}")
    return context

@function_tool
def get_security_info(query: str):
    try:

        
        vector_store = PineconeVectorStore(namespace="policy-knowledge")
        chunks = vector_store.search(query, category="security")
        context = "\n\n".join(c[0] for c in chunks)
        
        print('-'*30)
        print(context)
        print('-'*30)
        return context
    
    except Exception as e:
        print(f"Error initializing vector store: {format_error(e)}")
        return f"Error initializing vector store: {format_error(e)}"


@function_tool
def get_cancelation_info(query: str):
    try:

        vector_store = PineconeVectorStore(namespace="policy-knowledge")
        chunks = vector_store.search(query, category="cancelation")
        context = "\n\n".join(c[0] for c in chunks)
        print('-'*30)
        print(context)
        print('-'*30)
        return context
    except Exception as e:
        print(f"Error initializing vector store: {format_error(e)}")
        return f"Error initializing vector store: {format_error(e)}"
@function_tool
def get_renewal_info(query: str):
    try:

        vector_store = PineconeVectorStore(namespace="policy-knowledge")
        chunks = vector_store.search(query, category="renewal")
        context = "\n\n".join(c[0] for c in chunks)
        
        print('-'*30)
        print(context)
        print('-'*30)
        return context
    except Exception as e:
        print(f"Error initializing vector store: {format_error(e)}")
        return f"Error initializing vector store: {format_error(e)}"
    

security_agent = Agent(
    name="Security Agent",
    instructions="You handle all security-related user questions.",
    tools=[get_security_info]
)

cancelation_agent = Agent(
    name="Cancelation Agent",
    instructions="You assist users with canceling services or subscriptions.",
    tools=[get_cancelation_info]
)

renewal_agent = Agent(
    name="Renewal Agent",
    instructions="You help users renew their services or subscriptions.",
    tools=[get_renewal_info]
)

billing_agent = Agent(
    name="Billing Agent",
    instructions="You handle questions related to billing based on user question.",
    tools=[get_billing_info]
)

# Triage agent
triage_agent = Agent(
    name="Triage Agent",
    instructions="Route the user to the correct agent based on their question.",
    handoffs=[billing_agent, security_agent, renewal_agent, cancelation_agent],
    # handoff_description="questions related to billing are passed to billing agent along with user question, and questions related to weather are passed to weather agent along with the city"
)


print(
    Runner.run_sync(
    starting_agent=security_agent,
    input="When security patches are applied?"
))

print('-'*80)

print(Runner.run_sync(
    starting_agent=billing_agent,
    input="refund is acceptanle within how many days of purchase?",
    max_turns=9
))

