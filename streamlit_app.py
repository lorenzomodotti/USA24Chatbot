import streamlit as st
from copilot import Copilot
import os
### set openai key, first check if it is in environment variable, if not, check if it is in streamlit secrets, if not, raise error

st.image("https://raw.githubusercontent.com/lorenzomodotti/USA24Chatbot/refs/heads/main/images/white_house.png")
st.header(":flag-us: 2024 US Presidential Election ChatBot :flag-us:")
st.write(
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
)


openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key: ### get openai key from user input
    openai_api_key = st.text_input("Please enter your OpenAI API Key", type="password")

if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    if "messages" not in st.session_state.keys():  # Initialize the chat messages history
        st.session_state.messages = [
            {"role": "assistant", "avatar": "https://raw.githubusercontent.com/lorenzomodotti/USA24Chatbot/de013ed1c1939795c1a2781dc97b99abbdb4a5b5/images/capitol.png", "content": "I am an expert about the political program of the Democratic Party and the Republican Party for the 2024 US presidential election :flag-us: Ask me anything related to the parties' agendas."}
        ]

    @st.cache_resource
    def load_copilot():
        return Copilot(key = openai_api_key)



    if "chat_copilot" not in st.session_state.keys():  # Initialize the chat engine
        st.session_state.chat_copilot = load_copilot()

    if prompt := st.chat_input(
        "Ask me anything related to the political programs of the Democratic Party and the Republican Party for the 2024 US presidential election."
    ):  # Prompt for user input and save to chat history
        st.session_state.messages.append({"role": "user", "avatar": "https://raw.githubusercontent.com/lorenzomodotti/USA24Chatbot/de013ed1c1939795c1a2781dc97b99abbdb4a5b5/images/user.png", "content": prompt})

    for message in st.session_state.messages:  # Write message history to UI
        with st.chat_message(message["role"], avatar = message["avatar"]):
            st.write(message["content"])

    # If last message is not from assistant, generate a new response
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant", avatar = "https://raw.githubusercontent.com/lorenzomodotti/USA24Chatbot/de013ed1c1939795c1a2781dc97b99abbdb4a5b5/images/capitol.png"):

            retrived_info, answer = st.session_state.chat_copilot.ask(prompt, messages=st.session_state.messages[:-1])
            ### answer can be a generator or a string

            #print(retrived_info)
            if isinstance(answer, str):
                st.write(answer)
            else:
                ### write stream answer to UI
                def generate():
                    for chunk in answer:
                        content = chunk.choices[0].delta.content
                        if content:
                            yield content
                answer = st.write_stream(generate())

            st.session_state.messages.append({"role": "assistant", "content": answer})
