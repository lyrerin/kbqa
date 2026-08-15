"""
Day 8-10 集成测试
覆盖: 文档管理API | 问答API(单轮/多轮/流式) | API Key认证
"""
import requests
import json
import sys

BASE = "http://localhost:8000"
PASS = 0
FAIL = 0


def test(name: str, condition: bool, detail: str = ""):
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f"  ✅ {name}")
    else:
        FAIL += 1
        print(f"  ❌ {name}  — {detail}")
    return condition


def header(title: str):
    print(f"\n{'=' * 55}")
    print(f"  {title}")
    print(f"{'=' * 55}")


# ============================================================
# Day 8: 文档管理 API
# ============================================================
header("Day 8 — 文档管理 API")

# 8.1 根路径
resp = requests.get(f"{BASE}/")
test("GET / 返回首页信息",
     resp.status_code == 200 and "name" in resp.json(),
     f"status={resp.status_code} body={resp.text[:80]}")

# 8.2 健康检查
resp = requests.get(f"{BASE}/health")
data = resp.json()
test("GET /health 返回 healthy",
     resp.status_code == 200 and data.get("status") == "healthy",
     f"body={resp.text[:100]}")
test("GET /health 包含知识库状态",
     "knowledge_base" in data,
     f"keys={list(data.keys())}")

# 8.3 知识库状态
resp = requests.get(f"{BASE}/api/documents/status")
test("GET /api/documents/status 成功",
     resp.status_code == 200,
     f"status={resp.status_code}")
data = resp.json()
test("返回字段完整 (total_documents, total_chunks, sources)",
     all(k in data for k in ["total_documents", "total_chunks", "sources"]),
     f"keys={list(data.keys())}")

# 8.4 上传文档
print("\n  📤 上传测试文档...")
with open("knowledge_docs/员工手册.txt", "rb") as f:
    resp = requests.post(
        f"{BASE}/api/documents/upload",
        files={"file": ("测试上传.txt", f, "text/plain")},
    )
test("POST /api/documents/upload 上传成功",
     resp.status_code == 200,
     f"status={resp.status_code} body={resp.text[:100]}")
if resp.status_code == 200:
    upload_data = resp.json()
    test("返回 filename, chunks_count, message",
         all(k in upload_data for k in ["filename", "chunks_count", "message"]),
         f"keys={list(upload_data.keys())}")

# 8.5 上传后状态更新
resp = requests.get(f"{BASE}/api/documents/status")
test("上传后知识库文档数 > 0",
     resp.status_code == 200 and resp.json().get("total_documents", 0) > 0,
     f"total_documents={resp.json().get('total_documents', 0)}")

# 8.6 上传不支持的格式
print("\n  📤 测试拒绝不支持格式...")
resp = requests.post(
    f"{BASE}/api/documents/upload",
    files={"file": ("test.jpg", b"not-an-image", "image/jpeg")},
)
test("不支持格式返回 400",
     resp.status_code == 400,
     f"status={resp.status_code} body={resp.text[:80]}")


# ============================================================
# Day 9: 问答 API
# ============================================================
header("Day 9 — 问答 API")

# 9.1 单轮问答
payload = {"question": "员工入职满一年有多少天年假？", "session_id": "test_8_9_10"}
resp = requests.post(f"{BASE}/api/qa/ask", json=payload)
test("POST /api/qa/ask 返回 200",
     resp.status_code == 200,
     f"status={resp.status_code} body={resp.text[:120]}")
if resp.status_code == 200:
    data = resp.json()
    test("返回 question 字段",
         "question" in data)
    test("返回 answer 字段且非空",
         len(data.get("answer", "")) > 0)
    test("返回 sources 列表",
         isinstance(data.get("sources"), list))
    test("返回 session_id",
         data.get("session_id") == "test_8_9_10")
    # 年假相关答案应包含关键词
    has_keyword = "5天" in data.get("answer", "") or "5 天" in data.get("answer", "")
    test("答案包含正确信息 (年假5天)",
         has_keyword,
         f"answer={data.get('answer', '')[:100]}")

# 9.2 问知识库没有的内容（诚实测试）
payload2 = {"question": "公司CEO的私人手机号是什么？", "session_id": "test_honest"}
resp = requests.post(f"{BASE}/api/qa/ask", json=payload2)
if resp.status_code == 200:
    answer = resp.json().get("answer", "")
    test("知识库没有的信息 → 诚实说不知道",
         "无法回答" in answer or "没有" in answer or "未提及" in answer or "无法提供" in answer,
         f"answer={answer[:100]}")


# 9.3 多轮对话
print("\n  🔄 多轮对话记忆测试...")
session = "multi_turn_test_001"
# 第一轮
resp1 = requests.post(f"{BASE}/api/qa/chat", json={
    "question": "绩效考核有几个等级？", "session_id": session,
})
test("多轮对话 第1轮 返回 200",
     resp1.status_code == 200,
     f"status={resp1.status_code}")
a1 = resp1.json().get("answer", "") if resp1.status_code == 200 else ""

# 第二轮（追问，省略主语）
resp2 = requests.post(f"{BASE}/api/qa/chat", json={
    "question": "最高等级是什么？", "session_id": session,
})
test("多轮对话 第2轮 返回 200",
     resp2.status_code == 200,
     f"status={resp2.status_code}")
a2 = resp2.json().get("answer", "") if resp2.status_code == 200 else ""
# 如果记忆生效，应该知道"最高等级"指的是 S
test('多轮对话记忆生效（理解"最高等级"指的是绩效考核的 S）',
     "S" in a2.upper() or "卓越" in a2,
     f"answer={a2[:100]}")

# 9.4 会话历史
resp = requests.get(f"{BASE}/api/qa/history/{session}")
test("GET /api/qa/history/{session_id} 成功",
     resp.status_code == 200,
     f"status={resp.status_code}")
if resp.status_code == 200:
    hdata = resp.json()
    test("历史包含 messages 列表",
         "messages" in hdata)
    test("历史消息数 ≥ 4（2轮对话=4条消息）",
         hdata.get("count", 0) >= 4,
         f"count={hdata.get('count', 0)}")

# 9.5 清除会话历史
resp = requests.delete(f"{BASE}/api/qa/history/{session}")
test("DELETE /api/qa/history/{session_id} 成功",
     resp.status_code == 200,
     f"status={resp.status_code}")

# 清除后查历史应返回空
resp = requests.get(f"{BASE}/api/qa/history/{session}")
if resp.status_code == 200:
    test("清除后历史为空",
         resp.json().get("count", -1) == 0,
         f"count={resp.json().get('count')}")

# 9.6 流式输出
print("\n  🌊 流式输出测试...")
resp = requests.post(f"{BASE}/api/qa/ask/stream", json={
    "question": "团建预算多少？", "session_id": "stream_test",
}, stream=True)
test("POST /api/qa/ask/stream 返回 200",
     resp.status_code == 200,
     f"status={resp.status_code}")

if resp.status_code == 200:
    content_type = resp.headers.get("content-type", "")
    test("流式返回 text/event-stream",
         "event-stream" in content_type,
         f"content-type={content_type}")

    tokens = []
    for line in resp.iter_lines(decode_unicode=True):
        if line:
            tokens.append(line)
    test("收到 SSE token 事件",
         len(tokens) > 0,
         f"token_count={len(tokens)}")

    # 检查 done 事件（在 event: 行，不在 data: 行）
    has_done = any("done" in t for t in tokens)
    test("流式输出包含 done 事件",
         has_done,
         f"last tokens={tokens[-4:] if tokens else 'none'}")


# ============================================================
# Day 10: API Key 认证
# ============================================================
header("Day 10 — API Key 认证")

# 10.1 不带 Key → 401
resp = requests.get(f"{BASE}/api/auth/me")
test("不传 X-API-Key → 401",
     resp.status_code == 401,
     f"status={resp.status_code} body={resp.text[:80]}")

# 10.2 带错误 Key → 403
resp = requests.get(f"{BASE}/api/auth/me",
                    headers={"X-API-Key": "wrong-key-999"})
test("传错误 API Key → 403",
     resp.status_code == 403,
     f"status={resp.status_code} body={resp.text[:80]}")

# 10.3 管理员 Key → 200，返回用户信息
resp = requests.get(f"{BASE}/api/auth/me",
                    headers={"X-API-Key": "admin-key-123"})
test("admin-key-123 → 200",
     resp.status_code == 200,
     f"status={resp.status_code}")
if resp.status_code == 200:
    data = resp.json()
    test("admin 角色为 admin",
         data.get("role") == "admin",
         f"data={data}")
    test("admin 名称为 管理员",
         data.get("name") == "管理员",
         f"data={data}")

# 10.4 普通用户 Key → 200
resp = requests.get(f"{BASE}/api/auth/me",
                    headers={"X-API-Key": "user-key-456"})
test("user-key-456 → 200",
     resp.status_code == 200,
     f"status={resp.status_code}")
if resp.status_code == 200:
    data = resp.json()
    test("user 角色为 user",
         data.get("role") == "user",
         f"data={data}")


# ============================================================
# 结果汇总
# ============================================================
header("测试结果汇总")
total = PASS + FAIL
print(f"  通过: {PASS}/{total}")
print(f"  失败: {FAIL}/{total}")
print(f"  通过率: {PASS/total*100:.1f}%" if total > 0 else "  无测试")

if FAIL > 0:
    print(f"\n  ⚠️  有 {FAIL} 项未通过，请检查对应接口")
else:
    print(f"\n  🎉 Day 8-10 全部验收通过！")

sys.exit(0 if FAIL == 0 else 1)
