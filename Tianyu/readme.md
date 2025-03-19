📌 测试

✅ 1. 访问 /time
curl -k https://127.0.0.1:4433/time
✅ 服务器返回：

{"time": "2025-03-19 19:00:00"}
✅ 2. 访问 /echo 发送 JSON
curl -k -X POST https://127.0.0.1:4433/echo -H "Content-Type: application/json" -d '{"msg": "Hello"}'
✅ 服务器返回：

{"received": {"msg": "Hello"}}