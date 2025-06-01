import streamlit as st
from vitos_pizza_cafe import VitosClient

# Page configuration
st.set_page_config(page_title="Vito's Pizza Cafe Assistant", layout="wide")

# Initialize session state
if "conversations" not in st.session_state:
    st.session_state.conversations = [{
        "id": 0, 
        "messages": [{
            "role": "assistant", 
            "content": "Welcome to Vito's Pizza Cafe! I'm your smart assistant here to help with registration, login, order tracking, placing orders, and understanding our promotions and refunds."
        }]
    }]
if "current_conversation" not in st.session_state:
    st.session_state.current_conversation = 0
if "form_key" not in st.session_state:
    st.session_state.form_key = 0
if "client" not in st.session_state:
    st.session_state.client = VitosClient(thread_id=str(st.session_state.current_conversation))

# Sidebar - Conversation Management
with st.sidebar:
    st.title("Conversation Management")
    
    # New conversation button
    if st.button("New Conversation"):
        new_conv_id = len(st.session_state.conversations)
        st.session_state.conversations.append({
            "id": new_conv_id, 
            "messages": [{
                "role": "assistant", 
                "content": "Welcome to Vito's Pizza Cafe! I'm your smart assistant here to help with registration, login, order tracking, placing orders, and understanding our promotions and refunds."
            }]
        })
        st.session_state.current_conversation = new_conv_id
        st.session_state.client = VitosClient(thread_id=str(new_conv_id))
        st.rerun()
    
    # Conversation list
    st.write("Select Conversation:")
    for conv in st.session_state.conversations:
        if st.button(f"Conversation {conv['id']}", key=f"conv_{conv['id']}"):
            st.session_state.current_conversation = conv['id']
            st.session_state.client = VitosClient(thread_id=str(conv['id']))
            st.rerun()

# Main interface
st.title("Vito's Pizza Cafe AI Assistant")

# Display current conversation
current_conv = st.session_state.conversations[st.session_state.current_conversation]
# st.subheader(f"Current Conversation: {current_conv['id']}")

# Display conversation history
for message in current_conv["messages"]:
    if message["role"] == "user":
        st.write(f"👤 User: {message['content']}")
        st.write("")  # Add empty line after user message
    else:
        # Format assistant messages with orange color and bold, allowing markdown rendering
        formatted_content = message['content'].replace('\n', '\n\n')  # Proper markdown line breaks
        st.markdown(
            f"""<div style='color:#ff9800; font-weight:bold;'>🤖 Assistant:</div>""",
            unsafe_allow_html=True
        )
        st.markdown(
            f"""<div style='color:#ff9800; font-weight:bold;'>{formatted_content}</div>""",
            unsafe_allow_html=True
        )
        st.write("")  # Add empty line after assistant message

# Create input placeholder
input_placeholder = st.empty()

# Use form to support enter key submission
with input_placeholder.form(f"chat_form_{st.session_state.form_key}"):
    user_input = st.text_area(
        "Please enter your question:",
        key=f"user_input_{st.session_state.form_key}",
        height=100,  # set the input box hight
        placeholder="Type your message here... Press Shift+Enter for new line",  # hint text
    )
    submit_button = st.form_submit_button("Send")

if submit_button and user_input:
    # Add user message to history
    current_conv["messages"].append({"role": "user", "content": user_input})
    
    # Get assistant response
    response = st.session_state.client.query(user_input)
    
    # Add assistant response to history
    current_conv["messages"].append({"role": "assistant", "content": response})
    
    # Update form key
    st.session_state.form_key += 1
    
    # Refresh page
    st.rerun()