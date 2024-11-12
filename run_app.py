import subprocess
import sys
import os
import socket
import time

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('127.0.0.1', port))
            return False
        except socket.error:
            return True

def find_available_port(start_port=8501, max_port=8599):
    for port in range(start_port, max_port + 1):
        if not is_port_in_use(port):
            return port
    return None

def main():
    # Find an available port
    port = find_available_port()
    if not port:
        print("Error: No available ports found between 8501 and 8599")
        sys.exit(1)

    # Update the Streamlit config
    os.makedirs('.streamlit', exist_ok=True)
    config_path = os.path.join('.streamlit', 'config.toml')
    
    with open(config_path, 'w') as f:
        f.write(f"""[server]
port = {port}
address = "127.0.0.1"
baseUrlPath = ""
enableCORS = false
enableXsrfProtection = true
maxUploadSize = 200
maxMessageSize = 200
enableWebsocketCompression = false
""")

    # Run the Streamlit app
    try:
        cmd = [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "src/frontend/app.py",
            "--server.address=127.0.0.1",
            f"--server.port={port}",
        ]
        
        process = subprocess.Popen(cmd)
        
        # Wait a few seconds to ensure the server starts
        time.sleep(3)
        
        # Check if the process is still running
        if process.poll() is None:
            print(f"\nApplication started successfully on port {port}")
            print(f"URL: http://127.0.0.1:{port}")
            process.wait()
        else:
            print("Failed to start the application")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\nShutting down the application...")
        process.terminate()
        sys.exit(0)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()