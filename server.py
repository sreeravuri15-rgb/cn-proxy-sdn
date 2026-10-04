import socket
import threading

HOST = "0.0.0.0"
PORT = 9000
BUFFER_SIZE = 1024


def handle_connection(connection, address):
    """Handle one proxy connection."""
    try:
        print(f"Destination server received connection from {address}")

        message = connection.recv(BUFFER_SIZE).decode().strip()
        if not message:
            return

        print(f"Destination server received: {message}")

        response = f"Hello from Server! Request '{message}' was processed."
        connection.sendall(response.encode())

    except (ConnectionResetError, BrokenPipeError):
        print(f"Connection closed unexpectedly: {address}")

    finally:
        connection.close()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(10)

print("====================================")
print(" Simulated Destination Server")
print("====================================")
print(f"Server listening on {HOST}:{PORT}")
print("Waiting for proxy connections...\n")

try:
    while True:
        connection, address = server.accept()

        thread = threading.Thread(
            target=handle_connection,
            args=(connection, address),
            daemon=True,
        )
        thread.start()

except KeyboardInterrupt:
    print("\nServer stopped.")

finally:
    server.close()
