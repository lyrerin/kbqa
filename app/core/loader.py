"""多格式文档加载器 —— 支持 TXT、PDF、CSV、DOCX"""
import os
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    CSVLoader,
    Docx2txtLoader,
    
)


def load_document(file_path: str) -> List[Document]:
    """根据文件后缀自动选择加载器"""
    ext = os.path.splitext(file_path)[1].lower()

    loaders = {
        ".txt":  lambda p: TextLoader(p, encoding="utf-8").load(),
        ".pdf":  lambda p: PyPDFLoader(p).load(),
        ".csv":  lambda p: CSVLoader(p, encoding="utf-8").load(),
        ".docx": lambda p: Docx2txtLoader(p).load(),
    }

    if ext not in loaders:
        raise ValueError(f"不支持的文件格式: {ext}，支持的格式: {list(loaders.keys())}")

    return loaders[ext](file_path)


def load_documents_from_directory(directory: str) -> List[Document]:
    """批量加载目录下所有支持的文档"""
    all_docs = []
    supported = {".txt", ".pdf", ".csv", ".docx"}

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        ext = os.path.splitext(filename)[1].lower()

        if ext in supported :
            try:
                docs = load_document(file_path)
                for doc in docs:
                    doc.metadata["source"] = filename
                all_docs.extend(docs)
                print(f"[OK] 已加载: {filename} ({len(docs)} 页/段落)")
            except Exception as e:
                print(f"[FAIL] 加载失败: {filename}, 错误: {e}")

    return all_docs
