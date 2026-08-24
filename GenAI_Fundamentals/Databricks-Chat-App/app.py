import os
import streamlit as st

from openai import OpenAI
from databricks.sdk.core import Config

# Databricks Authentication
cfg = Config()

token = cfg.oauth_token().access_token

client = OpenAI(
    api_key=token,
    base_url=f"{cfg.host}/serving-endpoints"
)

# Serving endpoint name supplied through app.yaml
MODEL_NAME = os.environ["SERVING_ENDPOINT"]

st.set_page_config(
    page_title="Ask Batman",
    page_icon="🦇"
)

# Streamlit UI
st.title("🦇 Ask Batman")
st.caption("Powered by Databricks Model Serving")


# Initialize conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Chat input
prompt = st.chat_input("Ask Batman something...")


if prompt:

    # Store user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)


    # Send request to Databricks Model Serving
    completion = client.chat.completions.create(

        model=MODEL_NAME,

        messages=[
            {
                "role": "system",
                "content": "You are Batman, the protector of Gotham City."
            },
            *st.session_state.messages
        ]
    )


    response = completion.choices[0].message.content


    # Display Batman response
    with st.chat_message("assistant"):
        st.markdown(response)


    # Store response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )