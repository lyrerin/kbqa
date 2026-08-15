from pydantic import BaseModel,Field
from typing import List ,Optional
class DocumentUploadResponse(BaseModel):
    """文档上传响应"""
    filename:str
    chunks_count: int
    message:str

class QuestionRequest(BaseModel):
    """提问请求"""
    question: str = Field(...,min_length=1,max_length=1000,description = '用户问题')
    session_id: str = Field(default = 'default',description = '会话ID（用于多轮对话）')

class SourceInfo(BaseModel):
    content:str = Field(...,description = '引用内容摘要')
    source:str = Field(...,description ='来源文件名')

class AnswerResponse(BaseModel):
    question:str
    answer:str
    sources: List[SourceInfo]
    session_id:str

class KnowledgeBaseStatus(BaseModel):
    """知识库状态"""
    total_documents: int
    total_chunks: int
    sources: List[str]

class ErrorResponse(BaseModel):
    """错误响应"""
    detail: str
