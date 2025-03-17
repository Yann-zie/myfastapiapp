import streamlit as st
import json
from main import main  # Import the main function from main.py
import time
import asyncio

# Streamlit layout and interaction
st.set_page_config(page_title="Voice Assistant", page_icon="🎙️")

# Function to simulate listening state and run the assistant logic
def run_assistant():
    # Check if there is an existing event loop and close it if needed
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            print("Closing existing event loop...")
            loop.stop()
            loop.close()  # Close the existing loop to ensure we start a new one
    except RuntimeError:
        # No event loop is currently running
        pass

    # Set the 'listening' state
    st.session_state.listening = True
    st.session_state.speaking = False
    st.session_state.logs = []  # Clear previous logs for a new conversation
    
    # Display "Listening" state
    st.session_state.logs.insert(0,{"role": "assistant", "message": "Listening..."})
    
    # Run the main function to start the assistant logic (which does the listening and responding)
    main()  # This invokes the VoiceAssistant logic

    # After the assistant speaks, set the 'speaking' state
    st.session_state.listening = False
    st.session_state.speaking = True
    st.session_state.logs.insert(0,{"role": "assistant", "message": "Speaking..."})
    time.sleep(2)  # Simulate delay for speech output
    st.session_state.speaking = False

# Function to load and show conversation logs from the conversation.json file
def show_conversation():
    try:
        # Load conversation logs from the JSON file
        with open('conversation.json', 'r') as file:
            conversation_data = json.load(file)

        # Display the conversation in chat format
        for entry in conversation_data:
            st.markdown(f"**You**: {entry['user']}")
            st.markdown(f"**Assistant**: {entry['bot']}")
            st.markdown("---")

    except FileNotFoundError:
        st.write("Conversation log file not found.")
    except json.JSONDecodeError:
        st.write("Error reading the conversation log file.")


# Display conversation log button and new conversation button
col1, col2 = st.columns([1, 5])
with col1:
    st.markdown('[Conversation Log](#)')  # Placeholder link to log section, can add functionality later
with col2:
    if st.button('New Conversation'):
        st.session_state.logs = []  # Clear logs and restart the conversation

# Display the main interface
st.title("Voice Assistant")
st.write("Press the microphone button or spacebar to start listening.")

# Create a centered microphone button
col1, col2, col3 = st.columns([1, 5, 1])
with col2:
    if st.button("🎤 Start Listening"):
        run_assistant()

# Display listening and speaking states
if 'listening' in st.session_state and st.session_state.listening:
    st.write("**Listening...**")
elif 'speaking' in st.session_state and st.session_state.speaking:
    st.write("**Speaking...**")

# Show the conversation in chat format from the JSON file
show_conversation()

# Display quit button to end the conversation
if st.button("Quit"):
    st.write("Conversation ended. Goodbye!")
    st.stop()  # Ends the Streamlit app session
