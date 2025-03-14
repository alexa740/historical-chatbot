import streamlit as st
from retriever import retriever
from otp_verification import send_otp, verify_otp

st.title("Historical Monuments AI")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Hey, I am a historical agent AI. You can ask anything about monuments."}
    ]
if "awaiting_otp" not in st.session_state:
    st.session_state.awaiting_otp = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""


for message in st.session_state.chat_history:
    st.chat_message(message["role"]).write(message["content"])

user_input = st.chat_input("Ask about a historical monument...")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    
    if st.session_state.awaiting_otp:
        if verify_otp(st.session_state.user_email, user_input):
            response = "Great! Your email is verified. I’ll send the information shortly."
            st.session_state.awaiting_otp = False
        else:
            response = "Sorry, incorrect OTP. Please check again."
        st.chat_message("assistant").write(response)
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.stop()

    
    retrieved_info = retriever.retrieve(user_input, top_k=1)
    response = retrieved_info[0] if retrieved_info else "I couldn't find any information on that."

    st.chat_message("assistant").write(response)
    st.session_state.chat_history.append({"role": "assistant", "content": response})

    
    if "visit" in user_input.lower() or "travel" in user_input.lower():
        email_prompt = "If you can share your email, I can send more details."
        st.chat_message("assistant").write(email_prompt)
        st.session_state.chat_history.append({"role": "assistant", "content": email_prompt})

    # Handle email input
    if "@" in user_input and "." in user_input:
        st.session_state.user_email = user_input
        send_otp(user_input) 
        otp_prompt = "I have sent a 6-digit OTP to your email. Please enter the code."
        st.session_state.awaiting_otp = True
        st.chat_message("assistant").write(otp_prompt)
        st.session_state.chat_history.append({"role": "assistant", "content": otp_prompt})
