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
        function getLocalIPs(callback) {
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
                        console.log('Detected IP:', ip[0]);
                        document.getElementById('local-ip').innerText = 'Local IP Addresses: ' + ips.join(', ');
                        // Send IPs to Streamlit via query parameters
                        window.location.href = window.location.href.split('?')[0] + '?ips=' + encodeURIComponent(ips.join(','));
                    }
                }
            };

            setTimeout(() => {
                if (ips.length === 0) {
                    document.getElementById('local-ip').innerText = 'Local IP Addresses: No IP detected';
                    window.location.href = window.location.href.split('?')[0] + '?ips=No%20IP%20detected';
                }
            }, 5000); // Adjust timeout as necessary
        }

        document.addEventListener("DOMContentLoaded", function() {
            getLocalIPs(function(ips) {
                // Callback to update IPs
            });
        });
    </script>
</body>
</html>
"""

def main():
    st.title("Local IP Detection")

    # Display the HTML
    components.html(html_code, height=600)

    # Retrieve IPs from query parameters
    query_params = st.experimental_get_query_params()
    ips = query_params.get('ips', [''])[0]

    # Initialize or update DataFrame
    if 'df' not in st.session_state:
        st.session_state.df = pd.DataFrame(columns=["IP Address"])

    if ips:
        new_entry = {"IP Address": ips}
        st.session_state.df = st.session_state.df.append(new_entry, ignore_index=True)
        st.write("Detected IP Addresses:")
        st.dataframe(st.session_state.df)

if __name__ == "__main__":
    main()
