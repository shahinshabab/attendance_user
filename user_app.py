import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

# Define the HTML and JavaScript code
html_code = """
<!DOCTYPE html>
<html>
<head>
    <title>Local IP Detection</title>
</head>
<body>
    <h1>Local IP Detection</h1>
    <div id="local-ip">Detecting...</div>
    <script>
        function getLocalIPs() {
            var ips = [];
            var pc = new RTCPeerConnection({iceServers: []});
            pc.createDataChannel('');
            
            pc.createOffer().then(function(sdp) {
                return pc.setLocalDescription(sdp);
            }).catch(function(error) {
                console.error('Error creating offer:', error);
            });

            pc.onicecandidate = function(event) {
                if (event.candidate) {
                    var ip = /([0-9]{1,3}\.){3}[0-9]{1,3}/.exec(event.candidate.candidate);
                    if (ip) {
                        ips.push(ip[0]);
                        document.getElementById('local-ip').innerText = 'Local IP Addresses: ' + ips.join(', ');
                        
                        // Post message to Streamlit
                        window.parent.postMessage({type: 'local_ip', ips: ips}, '*');
                    }
                }
            };

            setTimeout(() => {
                if (ips.length === 0) {
                    document.getElementById('local-ip').innerText = 'Local IP Addresses: No IP detected';
                    window.parent.postMessage({type: 'local_ip', ips: ['No IP detected']}, '*');
                }
            }, 5000); // Adjust timeout as necessary
        }

        document.addEventListener("DOMContentLoaded", function() {
            getLocalIPs();
        });

        window.addEventListener("message", function(event) {
            if (event.data.type === 'local_ip') {
                // Send detected IPs to Streamlit
                const form = document.createElement('form');
                form.method = 'POST';
                form.action = window.location.href;
                const input = document.createElement('input');
                input.type = 'hidden';
                input.name = 'ips';
                input.value = event.data.ips.join(',');
                form.appendChild(input);
                document.body.appendChild(form);
                form.submit();
            }
        });
    </script>
</body>
</html>
"""

def main():
    st.title("Local IP Detection")

    # Display the HTML
    components.html(html_code, height=600)

    # Handle form data
    ips = st.experimental_get_query_params().get('ips', [''])[0]

    # Initialize or update DataFrame
    if 'df' not in st.session_state:
        st.session_state.df = pd.DataFrame(columns=["IP Address"])

    if ips:
        # Append new IP to DataFrame
        st.write("ip detected")
        new_entry = {"IP Address": ips}
        st.session_state.df = st.session_state.df.append(new_entry, ignore_index=True)
        st.write("Detected IP Addresses:")
        st.dataframe(st.session_state.df)

if __name__ == "__main__":
    main()
