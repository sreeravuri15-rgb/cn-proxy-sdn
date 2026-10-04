import socket
import threading
from datetime import datetime
from sdn_rules import check_rule

PROXY_HOST = "0.0.0.0"
PROXY_PORT = 8000
SERVER_HOST = "10.0.0.4"
SERVER_PORT = 9000
BUFFER_SIZE = 1024

log_lock = threading.Lock()


def write_log(message, action, client_address):
    """Write every allowed/blocked request safely to the log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with log_lock:
        with open("proxy_log.txt", "a", encoding="utf-8") as log:
            log.write(
                f"{timestamp} - {client_address[0]}:{client_address[1]} - "
                f"{message} - {action}\n"
            )


def handle_client(client_connection, client_address):
    """Handle one client. Each client runs in its own thread."""
    print(f"\nClient connected: {client_address}")

    server_connection = None

    try:
        message = client_connection.recv(BUFFER_SIZE).decode().strip()

        if not message:
            return

        print(f"Request from {client_address}: {message}")

        # Read the current SDN rule at request time.
        action = check_rule(message)

        if action == "BLOCK":
            print(f"Request BLOCKED: {message}")
            write_log(message, "BLOCKED", client_address)
            client_connection.sendall(b"Request blocked by proxy!")
            return

        print(f"Request ALLOWED: {message}")
        write_log(message, "ALLOWED", client_address)

        # Forward allowed request to the simulated destination server.
        server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_connection.settimeout(5)
        server_connection.connect((SERVER_HOST, SERVER_PORT))
        server_connection.sendall(message.encode())

        response = server_connection.recv(BUFFER_SIZE)
        print(f"Server response: {response.decode(errors='replace')}")

        client_connection.sendall(response)

    except ConnectionRefusedError:
        print("Could not connect to the destination server. Is server.py running?")
        try:
            client_connection.sendall(b"Proxy error: destination server is unavailable.")
        except OSError:
            pass

    except (ConnectionResetError, BrokenPipeError):
        print(f"Client disconnected: {client_address}")

    except Exception as error:
        print(f"Error while handling {client_address}: {error}")

    finally:
        if server_connection is not None:
            server_connection.close()
        client_connection.close()
        print(f"Connection closed: {client_address}")


proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
proxy.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
proxy.bind((PROXY_HOST, PROXY_PORT))
proxy.listen(10)

print("====================================")
print(" TCP Proxy + Content Filtering System")
print("====================================")
print(f"Proxy listening on {PROXY_HOST}:{PROXY_PORT}")
print(f"Forwarding allowed requests to {SERVER_HOST}:{SERVER_PORT}")
print("Waiting for clients...\n")

try:
    while True:
        client_connection, client_address = proxy.accept()

        client_thread = threading.Thread(
            target=handle_client,
            args=(client_connection, client_address),
            daemon=True,
        )
        client_thread.start()

except KeyboardInterrupt:
    print("\nProxy stopped.")

finally:
    proxy.close()
