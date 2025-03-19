"""
这段代码的核心功能是解析 HTTP 请求并返回相应的响应，它可以：

解析 HTTP 请求（支持 GET 和 POST）。
根据路径处理请求：
/time：返回服务器时间（JSON 格式）。
/echo：接收 POST 请求的 JSON 数据，并原样返回。
其他路径：返回简单的 HTML 响应。

"""
import json
from datetime import datetime

# 解析 HTTP 请求，可在图示例中找到“解析请求示例”中的详细说明。
def parse_http_request(request_data):
    """解析 HTTP 请求"""
    lines = request_data.split("\r\n") # 按 HTTP 规范换行符拆分请求
    if len(lines) < 1:
        return None, None, None, None

    request_line = lines[0].split(" ")  # # 解析请求行 (GET /path HTTP/1.1)
    if len(request_line) < 2:
        return None, None, None, None

    method, path = request_line[0], request_line[1]  # 提取方法和路径

    headers = {}
    body = ""
    is_body = False

    for line in lines[1:]:  # 遍历请求的剩余部分
        if line == "":  # 遇到空行，表示 HTTP 头部结束，开始读取请求体
            is_body = True
            continue
        if is_body:
            body += line  # 读取请求体
        else:
            parts = line.split(": ", 1) # 解析 HTTP 头部（格式：Header: Value）
            if len(parts) == 2:
                headers[parts[0]] = parts[1]

    return method, path, headers, body  # 返回解析后的数据 


def handle_request(client_socket):
    """ 处理 HTTP 请求 """
    try:
        request_data = client_socket.recv(4096).decode('utf-8') # 读取请求数据
        if not request_data:
            return

        method, path, headers, body = parse_http_request(request_data) # 解析请求
        if method is None:
            return

        print(f"Received {method} request for {path}") # 记录日志

        # 处理不同的路径
        if path == "/time": # 访问 /time 返回服务器时间
            response_body = json.dumps({"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
            content_type = "application/json"

        elif path == "/echo" and method == "POST": # 访问 /echo 需要 POST 请求
            try:
                json_data = json.loads(body) # 尝试解析 JSON 数据
                response_body = json.dumps({"received": json_data})
            except json.JSONDecodeError:
                response_body = json.dumps({"error": "Invalid JSON"})
            content_type = "application/json"

        else:  # 其他路径返回 HTML 页面
            response_body = f"<html><body><h1>Request to {path}</h1></body></html>"
            content_type = "text/html"

        # 生成 HTTP 响应
        response = f"""\
HTTP/1.1 200 OK
Content-Type: {content_type}
Content-Length: {len(response_body)}

{response_body}
"""
        client_socket.sendall(response.encode('utf-8'))  # 发送响应

    except Exception as e:
        print(f"Error: {e}")  # 记录错误
    finally:
        client_socket.close() # 关闭连接
