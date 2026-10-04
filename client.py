import socket

PROXY_HOST = "10.0.0.3"
PROXY_PORT = 8000
BUFFER_SIZE = 1024

print("====================================")
print(" TCP Client")
print("====================================")
print("Enter a site/message to send through the proxy.")
print("Type 'exit' to close.\n")

while True:
    message = input("Enter request: ").strip()

    if message.lower() == "exit":
        print("Client closed.")
        break

    if not message:
        print("Request cannot be empty.\n")
        continue

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(5)

    try:
        client.connect((PROXY_HOST, PROXY_PORT))
        client.sendall(message.encode())
        response = client.recv(BUFFER_SIZE).decode(errors="replace")
        print("Proxy replied:", response)
    except ConnectionRefusedError:
        print("Could not connect to proxy. Start proxy.py first.")
        break
    except socket.timeout:
        print("Request timed out.")
    except OSError as error:
        print(f"Client error: {error}")
    finally:
        client.close()

    print()
