import socket
import ssl
import json
import time
# 服务器信息
SERVER_HOST = "127.0.0.1" # 仅在本机监听 
SERVER_PORT = 4433 # 选用 4433 作为 HTTPS 服务器端口
CA_CERT = "/Users/tangren/Documents/GitHub/openssl/Tianyu/server.crt"  # 服务器 CA 证书

# 创建 TCP 连接
client_socket = socket.create_connection((SERVER_HOST, SERVER_PORT)) # 创建 TCP 套接字并连接服务器

# 创建 SSL 上下文，启用 TLS 1.2 及以上，并验证服务器证书
context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
context.minimum_version = ssl.TLSVersion.TLSv1_2
context.load_verify_locations(CA_CERT)  # 加载 CA 证书以验证服务器

# 将 TCP 套接字转换为 TLS 套接字
with context.wrap_socket(client_socket, server_hostname=SERVER_HOST) as tls_socket:
    print(f"Connected to {SERVER_HOST}:{SERVER_PORT} via TLS")

def send_http_request(method, path, body=None):
    """ 发送 HTTP 请求并接收响应 """

    client_socket = socket.create_connection((SERVER_HOST, SERVER_PORT))
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.load_verify_locations(CA_CERT)

    with context.wrap_socket(client_socket, server_hostname=SERVER_HOST) as tls_socket:
        print(f"Connected to {SERVER_HOST}:{SERVER_PORT} via TLS")

        # 构造 HTTP 请求
        request = f"{method} {path} HTTP/1.1\r\n"
        request += f"Host: {SERVER_HOST}\r\n"
        request += "Connection: close\r\n"
        if body:
            request += "Content-Type: application/json\r\n"
            request += f"Content-Length: {len(body)}\r\n"
        request += "\r\n"
        if body:
            request += body

        # 发送请求
        tls_socket.sendall(request.encode("utf-8"))

        # 接收服务器响应
        response = tls_socket.recv(4096).decode("utf-8")
        print(f"Received Response:\n{response}")

while True:
    # 发送 GET 请求
    send_http_request("GET", "/time")
    time.sleep(5)
    # 发送 POST 请求
    send_http_request("POST", "/echo", json.dumps({"message": "Hello, TLS Server"}))

