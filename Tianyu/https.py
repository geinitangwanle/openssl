import socket #用于创建 TCP 服务器，监听客户端连接。
import ssl #用于封装 socket，实现 TLS 加密通信。
HOST = '127.0.0.1' # 仅在本机监听
PORT = 4433  # 选用 4433 作为 HTTPS 服务器端口

"""127.0.0.1：本地回环地址，服务器 仅允许本机访问。
PORT = 4433：443 是 HTTPS 的标准端口，但非 root 用户无法监听 1024 以下端口，所以这里用 4433。
"""

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER) #ssl.PROTOCOL_TLS_SERVER 默认支持 TLS 1.2（Python 3.6+）。
context.minimum_version = ssl.TLSVersion.TLSv1_2  # 禁用 TLS 1.0 和 1.1
context.load_cert_chain(certfile="/Users/tangren/Documents/GitHub/openssl/Tianyu/server.crt", keyfile="/Users/tangren/Documents/GitHub/openssl/Tianyu/server.key")
"""
ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)：创建一个 TLS 服务器端 SSL 上下文（context）。
context.load_cert_chain(certfile=..., keyfile=...)：加载 服务器证书和私钥，用于加密通信。
"""

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # 使用 IPv4 地址,创建 TCP 连接（基于流的通信）。
server_socket.bind((HOST, PORT)) # 绑定地址和端口,让服务器监听该地址。
server_socket.listen(5) #允许最多 5 个等待连接。
"""
这部分是最基本的 TCP 服务器，它本身还不支持 TLS。
"""

def handle_request(client_socket):
    request = client_socket.recv(1024).decode('utf-8') #接收 HTTP 请求（最多 1024 字节），并转换为字符串。
    print(f"Received request:\n{request}") #打印收到的请求内容（通常是 GET / HTTP/1.1）。

    response = """\
HTTP/1.1 200 OK
Content-Type: text/html

<html><body><h1>HTTPS Server Running</h1></body></html>
"""
    """
    HTTP/1.1 200 OK：表示 HTTP 响应成功（状态码 200）。
    Content-Type: text/html：告诉浏览器返回的是 HTML 网页。
    """

    client_socket.sendall(response.encode('utf-8')) #将 HTTP 响应发送给客户端。
    client_socket.close() #关闭客户端连接。


#使用 SSL 封装 TCP 服务器，实现 HTTPS 通信。
with context.wrap_socket(server_socket, server_side=True) as secure_sock: #封装 TCP 服务器，让它支持 TLS 加密,server_side=True 说明 服务器端使用 TLS。
    print(f"HTTPS Server listening on {HOST}:{PORT}...")

    while True:
        client_socket, addr = secure_sock.accept() #等待客户端连接。secure_sock.accept()：当客户端连接时，服务器会 自动进行 TLS 握手。
        print(f"TLS connection from {addr}") #打印客户端 IP。
        handle_request(client_socket) #调用 handle_request() 处理 HTTP 请求。


