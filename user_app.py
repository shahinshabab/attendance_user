import streamlit as st

# Define the URL of your local server
server_url = 'http://192.168.1.14:5000/'

# Streamlit app layout
st.title('Send HTTP Request with JavaScript')

# Simplified HTML and JavaScript embedded in the Streamlit app
html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Send Request</title>
</head>
<body>
    <h2>Send HTTP Request</h2>
    <button onclick="sendRequest()">Send Request</button>
    <p id="response"></p>
    
    <script>
        const serverUrl = '{server_url}';
        
        function sendRequest() {{
            fetch(serverUrl, {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json'
                }},
                body: JSON.stringify({{key1: 'value1', key2: 'value2'}})
            }})
            .then(response => response.json())
            .then(data => {{
                document.getElementById('response').innerText = 'Response from server: ' + JSON.stringify(data);
            }})
            .catch(error => {{
                document.getElementById('response').innerText = 'Error: ' + error;
            }});
        }}
    </script>
</body>
</html>
"""

# Render HTML with JavaScript in the Streamlit app
st.markdown(html_code, unsafe_allow_html=True)
