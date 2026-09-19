import asyncio
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage  # Import message types
from main_agent import create_travel_agent

# --------------------------------------------------
# Streamlit setup
# --------------------------------------------------

st.set_page_config(
    page_title="Singapore Travel Assistant",
    page_icon="✈️",
)

st.title("✈️ Singapore Travel Planning Assistant")


# --------------------------------------------------
# Create agent
# --------------------------------------------------

if "agent" not in st.session_state:
    st.session_state.agent = asyncio.run(create_travel_agent())


# --------------------------------------------------
# Chat history
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# --------------------------------------------------
# User question
# --------------------------------------------------

if question := st.chat_input("Ask about Singapore..."):

    # 1. Store user question in Streamlit session state
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    # --------------------------------------------------
    # Agent Execution
    # --------------------------------------------------

    with st.chat_message("assistant"):

        with st.status("Thinking and selecting the required tools..."):

            # 2. Convert stored UI history into LangChain BaseMessage objects
            formatted_messages = []
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    formatted_messages.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    formatted_messages.append(AIMessage(content=msg["content"]))

            # 3. Pass the full BaseMessage history to the agent
            response = asyncio.run(
                st.session_state.agent.ainvoke(
                    {
                        "messages": formatted_messages
                    }
                )
            )

        # Get final agent response
        messages = response["messages"]
        final_message = messages[-1]
        answer = final_message.content

        # Gemini structured content safety check
        if isinstance(answer, list):
            answer = "".join(
                item.get("text", "") for item in answer if isinstance(item, dict)
            )

        st.markdown(answer)

    # 4. Save assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )