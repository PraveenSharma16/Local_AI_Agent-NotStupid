import os
import re
import time
from typing import TypedDict, Annotated

from dotenv import load_dotenv
from imap_tools import MailBox, AND

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool

from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages



# LOAD ENV

load_dotenv()

IMAP_HOST = os.getenv('IMAP_HOST')
IMAP_USER = os.getenv('IMAP_USER')
IMAP_PASSWORD = os.getenv('IMAP_PASSWORD')

IMAP_FOLDER = 'INBOX'

# Local model
CHAT_MODEL = 'llama3.2'



# STATE

class ChatState(TypedDict):
    messages: Annotated[list, add_messages]



# PERFORMANCE METRICS


metrics = {
    "total_requests": 0,
    "successful_requests": 0,
    "failed_requests": 0,
    "total_response_time": 0
}



# GLOBAL QUERY TRACKER


latest_user_query = ""



# EMAIL CONNECTION

def connect():

    mail_box = MailBox(IMAP_HOST)

    mail_box.login(
        IMAP_USER,
        IMAP_PASSWORD,
        initial_folder=IMAP_FOLDER
    )

    return mail_box



# TOOL


@tool
def list_unread_emails():
    """
    Fetch latest unread emails.
    Automatically detects how many emails user wants.
    """

    print('🔧 List Unread Emails Tool Called')

    global latest_user_query

    try:

        # Default limit
        limit = 5

        q = latest_user_query.lower()

        
        # DETECT EMAIL COUNT
        

        if (
            'latest mail' in q
            or 'latest email' in q
        ):
            limit = 1

        # Extract numbers
        # latest 2 mails
        # show 3 emails

        match = re.search(r'(\d+)', q)

        if match:

            limit = int(match.group(1))

            # Max limit = 10
            if limit > 10:
                limit = 10

        
        # FETCH EMAILS
        

        with connect() as mb:

            unread = list(
                mb.fetch(
                    criteria=AND(seen=False),
                    limit=limit,
                    reverse=True,
                    mark_seen=False
                )
            )

        if not unread:
            return 'You have no unread messages.'

        emails = []

        
        # FORMAT OUTPUT
        

        for idx, mail in enumerate(unread, start=1):

            content = (
                mail.text
                or mail.html
                or "No content available."
            )

            # Fast summary
            summary = (
                content[:200]
                .replace('\n', ' ')
                .replace('\r', ' ')
            )

            formatted_email = f"""
-------------------------------------------------------

[{idx}] {mail.subject or '(No Subject)'}

From:
{str(mail.from_)}

Date:
{mail.date.astimezone().strftime('%Y-%m-%d %H:%M')}

Summary:
{summary}

-------------------------------------------------------
"""

            emails.append(formatted_email)

        return "\n".join(emails)

    except Exception as e:

        return f"Error fetching emails: {str(e)}"



# INITIALIZE MODEL


llm = init_chat_model(
    CHAT_MODEL,
    model_provider='ollama'
)

# Bind ONLY one tool
llm = llm.bind_tools([
    list_unread_emails
])



# LLM NODE


def llm_node(state: ChatState):

    response = llm.invoke(state['messages'])

    return {
        'messages': [response]
    }



# ROUTER


def router(state: ChatState):

    last_message = state['messages'][-1]

    if (
        hasattr(last_message, 'tool_calls')
        and last_message.tool_calls
    ):
        return 'tools'

    return END



# TOOL NODE


tool_node = ToolNode([
    list_unread_emails
])


def tools_node(state: ChatState):

    return tool_node.invoke(state)



# BUILD GRAPH


builder = StateGraph(ChatState)

builder.add_node('llm', llm_node)
builder.add_node('tools', tools_node)

builder.add_edge(START, 'llm')
builder.add_edge('tools', 'llm')

builder.add_conditional_edges(
    'llm',
    router
)

graph = builder.compile()



# MAIN LOOP

if __name__ == '__main__':

    state = {
        'messages': []
    }

    print("\n📧 NotStupid : Am ready to sneek into yout mailbox 🫪 ")
    print("Welcome Aryan ")
    print("Type your instructions (or 'quit' to exit).\n")

    while True:

        try:

            user_input = input('> ').strip()

            if user_input.lower() in {
                'quit',
                'exit',
                'q'
            }:
                print("\nGoodbye Aryan 👋\n")
                break

            if not user_input:
                continue

            
            # STORE USER QUERY
            

            latest_user_query = user_input

            
            # START TIMER
            

            start_time = time.time()

            metrics["total_requests"] += 1

        
            # ADD MESSAGE
            

            state['messages'].append(
                HumanMessage(content=user_input)
            )

        
            # RUN GRAPH
        

            state = graph.invoke(state)

    
            # END TIMER
        

            end_time = time.time()

            response_time = round(
                end_time - start_time,
                2
            )

            metrics["total_response_time"] += response_time

            metrics["successful_requests"] += 1

        
            # FINAL RESPONSE
        

            final_msg = state['messages'][-1]

            print("\n")
            print(final_msg.content)
            print("\n")

        
            # PERFORMANCE METRICS
        

            avg_time = round(
                metrics["total_response_time"] /
                metrics["successful_requests"],
                2
            )

            success_rate = round(
                (
                    metrics["successful_requests"] /
                    metrics["total_requests"]
                ) * 100,
                2
            )

            print("---------- PERFORMANCE METRICS ----------")

            print(f"Total Requests        : {metrics['total_requests']}")
            print(f"Successful Requests   : {metrics['successful_requests']}")
            print(f"Failed Requests       : {metrics['failed_requests']}")
            print(f"Current Response Time : {response_time} sec")
            print(f"Average Response Time : {avg_time} sec")
            print(f"Success Rate          : {success_rate}%")

            print("\n")

        except KeyboardInterrupt:

            print("\nExiting NotStupid AI...\n")
            break

        except Exception as e:

            metrics["failed_requests"] += 1

            print(f"\n Error: {e}\n")
