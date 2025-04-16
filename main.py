from agents import Agent, Runner, function_tool, guardrail, trace
from agents import  ItemHelpers, MessageOutputItem

import os
from openai import OpenAI
from vector_store.vector_store import PineconeVectorStore
import traceback
import sys
import asyncio
from openai.types.responses import ResponseTextDeltaEvent
from agents.extensions.visualization import draw_graph

client = OpenAI()
MODEL_NAME = 'gpt-4.1-nano'
# MODEL_NAME = 'gpt-4.1'
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
    context = "1 day"
    try:

        vector_store = PineconeVectorStore(namespace="policy-knowledge")
        chunks = vector_store.search(user_query, category="billing")
        context = "\n\n".join(c[0] for c in chunks)
        print('-'*30)
        print(context)
        print('-'*30)
        return context
    except Exception as e:
        
        print(f"Error initializing vector store: {format_error(e)}")
        return format_error(e)

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
    instructions="You handle all security-related user questions. Always use tools to fetch document information",
    tools=[get_security_info],
    model=MODEL_NAME
)

cancelation_agent = Agent(
    name="Cancelation Agent",
    instructions="You assist users with canceling services or subscriptions. Always use tools to fetch document information",
    tools=[get_cancelation_info],
    model=MODEL_NAME
)

renewal_agent = Agent(
    name="Renewal Agent",
    instructions="You help users renew their services or subscriptions. Always use tools to fetch document information",
    tools=[get_renewal_info],
    model=MODEL_NAME
)

billing_agent = Agent(
    name="Billing Agent",
    instructions="You handle questions related to billing based on user question. Always use tools to fetch document information",
    tools=[get_billing_info],
    model=MODEL_NAME
)

# Triage agent
triage_agent = Agent(
    name="Triage Agent",
    instructions="Route the user to the correct agent based on their question.",
    handoffs=[billing_agent, security_agent, renewal_agent, cancelation_agent],
    model=MODEL_NAME
    # handoff_description="questions related to billing are passed to billing agent along with user question, and questions related to ..."
)


# result1= Runner.run_sync(
# starting_agent=triage_agent,
# input="check the documents and tell me refund is acceptanle within how many days of purchase?",
# )
# for result in result1.new_items:
#     print(result)
# print('-'*80)
# for result in result1.raw_responses:
#     print(result)
# print('-'*80)



# print(
# Runner.run_sync(
# starting_agent=triage_agent,
# input="check the documents and tell me refund is acceptanle within how many days of purchase?",
# )

# )
# print('-'*80)


# print(
# Runner.run_sync(
# starting_agent=triage_agent,
# input="check the documents and tell me when security patches are applied?"
# ))




async def main():
    # draw_graph(triage_agent).view()

    with trace("workflow"): 


        
 

        result =  Runner.run_streamed(
        starting_agent=triage_agent,
        input="heck the documents and tell when security patches are applied?"
        )
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                print(event.data.delta, end="", flush=True)
        
        print('\n')
        print('-'*80)
        print('\n')

        result =  Runner.run_streamed(
        starting_agent=triage_agent,
        input="heck the documents and tell refund is acceptanle within how many days of purchase?"
        )
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                print(event.data.delta, end="", flush=True)
        
        



if __name__ == "__main__":
    asyncio.run(main())