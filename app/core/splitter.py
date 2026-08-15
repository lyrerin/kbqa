from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from app.config import CHUNK_SIZE, CHUNK_OVERLAP
import os

# def demo_splitter_effects():
#     file_path = os.path.join('knowledge_docs', '员工手册.txt')
#     loader = TextLoader(
#         file_path,
#         encoding='utf-8',
#     )
#     print(type(loader))
#     docs = loader.load()
#     # print(type(docs))
#     print(f'原始文档长度{len(docs[0].page_content)}')
#     print(f'原始文档前100字\n{docs[0].page_content[:100]}\n')

#     configs =[
#         ('大块(chunk_size=1000, chunk_overlap=100)',1000,100),
#         ('中块(chunk_size=500, chunk_overlap=50)',500,50),
#         ('小块(chunk_size=200, chunk_overlap=30)',200,30),
#     ]
#     for name,chunk_size,chunk_overlap in configs:
#         splitter = RecursiveCharacterTextSplitter(
#             chunk_size=chunk_size,
#             chunk_overlap=chunk_overlap,
#             separators=["\n\n", "\n", "。", "；", "，", " ", ""],
#         )
#         chunks = splitter.split_documents(docs)
#         print(f"\n{'='*60}")
#         print(f"🔧 {name}")
#         print(f"   切出块数: {len(chunks)}")
#         print(f"   第1块长度: {len(chunks[0].page_content)} 字符")
#         print(f"   第1块内容:\n{chunks[0].page_content[:150]}...\n")

#         if len(chunks) >= 2:
#             print(f"第1块内容最后:\n{chunks[0].page_content[-80:]}...\n")
#             print(f'第二块内容前面：\n{chunks[1].page_content[:80]}...\n')

# if __name__ == '__main__':
#     demo_splitter_effects()
def get_text_splitter(
    chunk_size : int = 500,
    chunk_overlap : int = 50,
) -> RecursiveCharacterTextSplitter:
    return RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", "。", "；", "，", " ", "",],
            length_function = len,
        )
def split_document(file_path: str, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP):
    """加载并分割单个文档"""
    loader = TextLoader(file_path, encoding="utf-8")
    docs = loader.load()
    splitter = get_text_splitter(chunk_size, chunk_overlap)
    chunks = splitter.split_documents(docs)
    for i,chunk in enumerate(chunks):
        chunk.metadata['source'] = file_path
        chunk.metadata['chunk_index'] = i
    return chunks
