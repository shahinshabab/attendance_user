import streamlit as st
import http.client
import json

# Define the URL and port of your local server
server_host = '192.168.1.14'
server_port = 5000

# Streamlit app layout
st.title('Send HTTP Request with Python')

# Input fields for data to send
key1 = st.text_input('Key 1', 'value1')
key2 = st.text_input('Key 2', 'value2')

if st.button('Send Request'):
    # Create the data to send
    data = json.dumps({
        key1: key2
    })
    
    try:
        # Create a connection
        conn = http.client.HTTPConnection(server_host, server_port)
        
        # Send the POST request
        conn.request('POST', '/', body=data, headers={'Content-Type': 'application/json'})
        
        # Get the response
        response = conn.getresponse()
        response_data = response.read().decode()
        
        # Display the response
        st.write('Response from server:', response_data)
        
        # Close the connection
        conn.close()
    except Exception as e:
        st.error(f'Error: {e}')
