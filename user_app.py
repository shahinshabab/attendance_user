import streamlit as st
import requests
import socket
import time

API_URL = 'http://<YOUR_API_SERVER_IP>:5000/report'  # Replace with your API server URL

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
        s.close()
    except Exception:
        local_ip = "Unable to determine local IP"
    return local_ip

st.title("User Interface")
user_name = st.text_input("Enter your name", "")
local_ip = get_local_ip()

st.write(f"Your local IP address is: {local_ip}")

if st.button("Start"):
    if not user_name:
        st.warning("Please enter your name.")
    else:
        # Report IP to API
        response = requests.post(API_URL, json={'ip_address': local_ip})
        if response.status_code == 200:
            st.success("IP address reported successfully.")
        else:
            st.error("Failed to report IP address.")

if st.button("Stop"):
    # Optionally, handle stopping logic
    st.write("Stopping functionality not implemented.")
