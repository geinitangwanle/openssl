import json
from datetime import datetime
def parse_http_request(request_data):
    """解析 HTTP 请求"""
    lines = request_data.split("\r\n")
    if len(lines) < 1:
        return None, None, None, None

    request_line = lines[0].split(" ")  # 解析第一行
    if len(request_line) < 2:
        return None, None, None, None

    method, path = request_line[0], request_line[1]  # 提取方法和路径

    headers = {}
    body = ""
    is_body = False

    for line in lines[1:]:
        if line == "":
            is_body = True
            continue
        if is_body:
            body += line
        else:
            parts = line.split(": ", 1)
            if len(parts) == 2:
                headers[parts[0]] = parts[1]

    return method, path, headers, body

def handle_request(client_socket):
    """ 处理 HTTP 请求 """
    try:
        request_data = client_socket.recv(4096).decode('utf-8')
        if not request_data:
            return

        method, path, headers, body = parse_http_request(request_data)
        if method is None:
            return

        print(f"Received {method} request for {path}")

        if path == "/time":
            response_body = json.dumps({"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
            content_type = "application/json"

        elif path == "/echo" and method == "POST":
            try:
                json_data = json.loads(body)
                response_body = json.dumps({"received": json_data})
            except json.JSONDecodeError:
                response_body = json.dumps({"error": "Invalid JSON"})
            content_type = "application/json"

        else:
            response_body = f"<html><body><h1>Request to {path}</h1></body></html>"
            content_type = "text/html"

        response = f"""\
HTTP/1.1 200 OK
Content-Type: {content_type}
Content-Length: {len(response_body)}

{response_body}
"""
        client_socket.sendall(response.encode('utf-8'))

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
