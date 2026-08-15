# 企业知识库智能问答系统

基于 **RAG（检索增强生成）** 的企业知识库问答系统。用户上传 PDF / Word / TXT / CSV 文档，系统自动切分并向量化入库；提问时先检索相关段落，再由 DeepSeek 大模型生成带引用来源的答案，支持多轮对话记忆。

## 功能特性

- 多格式文档上传：PDF、Word（.docx/.doc）、TXT、CSV
- 自动文本切分 + 向量化，存入 ChromaDB
- 语义检索 + LLM 生成答案，附带引用来源
- 多轮对话记忆（上下文管理）
- 流式输出（SSE）
- 提供 FastAPI 后端 + Streamlit 前端

## 技术栈

Python 3.11+ · FastAPI · LangChain · ChromaDB · DeepSeek API · Streamlit · Docker

## 系统流程

```
上传文档 → 文本切分 → 向量化 → 存入 ChromaDB
                                        ↓
用户提问 → 向量检索相关段落 → LLM 生成答案（带引用） → 多轮记忆
```

## 目录结构

```
kbqa/
├── app/
│   ├── main.py            # FastAPI 入口
│   ├── config.py          # 配置（API Key、切分参数等）
│   ├── api/               # documents / qa / auth 路由
│   ├── core/              # loader、splitter、embeddings、vectorstore、retriever、rag_chain、memory_manager
│   ├── models/            # Pydantic 数据模型
│   └── utils/             # 日志等工具
├── streamlit_app.py       # Streamlit 前端
├── knowledge_docs/        # 待导入的知识文档
├── uploads/               # 上传文件暂存
├── chroma_db/             # 向量数据库持久化目录
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

## 快速开始

### 1. 环境要求

- Python 3.11+
- 一个 DeepSeek API Key

### 2. 创建虚拟环境

```bash
python -m venv .venv
# Windows (Git Bash)
source .venv/Scripts/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

在项目根目录创建 `.env` 文件（文本文件），内容：

```env
DEEPSEEK_API_KEY=你的APIKey
DEEPSEEK_BASE_URL=https://api.deepseek.com
```

> `DEEPSEEK_BASE_URL` 可省略，默认就是官方地址。

### 5. 启动后端

```bash
uvicorn app.main:app --reload --port 8000
```

- 接口文档（Swagger）：http://127.0.0.1:8000/docs
- 健康检查：http://127.0.0.1:8000/health

### 6. 启动前端

另开一个终端：

```bash
streamlit run streamlit_app.py
```

浏览器访问 http://127.0.0.1:8501

## API 接口

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/` | 欢迎页 |
| GET | `/health` | 健康检查 + 知识库状态 |
| POST | `/api/documents/upload` | 上传文档（PDF/Word/TXT/CSV） |
| POST | `/api/qa/ask` | 单轮问答（带引用来源） |
| POST | `/api/qa/chat` | 多轮对话（带记忆） |
| POST | `/api/auth/*` | 用户认证 |

## Docker 部署

```bash
docker compose up -d
```

- 后端 API：http://localhost:8000
- 前端界面：http://localhost:8501

## 配置说明

| 配置项 | 位置 | 默认值 |
|---|---|---|
| `DEEPSEEK_API_KEY` | `.env` | 必填 |
| `DEEPSEEK_BASE_URL` | `.env` | `https://api.deepseek.com` |
| `DEEPSEEK_MODEL` | `app/config.py` | `deepseek-v4-flash` |
| `CHUNK_SIZE` / `CHUNK_OVERLAP` | `app/config.py` | `200` / `30` |
