import socket
import ssl
HOST = '127.0.0.1' 
PORT = 4433  # 选用非特权端口

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="/Users/tangren/Documents/GitHub/openssl/Tianyu/server.crt", keyfile="/Users/tangren/Documents/GitHub/openssl/Tianyu/server.key")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

def handle_request(client_socket):
    request = client_socket.recv(1024).decode('utf-8')
    print(f"Received request:\n{request}")

    response = """\
HTTP/1.1 200 OK
Content-Type: text/html

<html><body><h1>HTTPS Server Running</h1></body></html>
"""
    client_socket.sendall(response.encode('utf-8'))
    client_socket.close()

with context.wrap_socket(server_socket, server_side=True) as secure_sock:
    print(f"HTTPS Server listening on {HOST}:{PORT}...")

    while True:
        client_socket, addr = secure_sock.accept()
        print(f"TLS connection from {addr}")
        handle_request(client_socket)


