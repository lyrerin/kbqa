import os
from langchain_community.vectorstores import Chroma
from app.core.embeddings import get_embeddings
from app.config import CHROMA_DIR
from app.core.splitter import split_document


def create_vectorstore_from_file(file_path: str) -> Chroma:
    print(f"📄 正在处理: {file_path}")
    chunks = split_document(file_path)
    print(f' 分割为{len(chunks)}个文本块')

    # 清理旧数据，避免每次运行重复追加
    import shutil
    if os.path.exists(CHROMA_DIR):
        shutil.rmtree(CHROMA_DIR)

    embeddings = get_embeddings()
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR,
    )
    print(f' 向量数据库已保存到{CHROMA_DIR}')

    return vectorstore

def load_vectorstore() -> Chroma:
    if not os.path.exists(CHROMA_DIR) or not os.listdir(CHROMA_DIR):
        raise FileNotFoundError(f"向量数据库目录{CHROMA_DIR}为空,请先导入文档")
    
    embeddings = get_embeddings()
    return Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings,
    )

def demo_retrieval():
    vectorstore = load_vectorstore()
    
    test_questions = [
        "年假有多少天？",
        "怎么报销差旅费？", 
        "绩效考核多久一次？",
        "公司有什么节日福利？",
        "迟到会扣钱吗？",
    ]
    for q in test_questions:
        print(f"\n{'='*50}")
        print(f'问题: {q}')
        print(f"\n{'='*50}")

        docs = vectorstore.similarity_search(q, k=3)

        for i, doc in enumerate(docs):
            print(f'\n 结果{i+1}(来源:{doc.metadata.get("source","未知")})')
            print(f'{doc.page_content[:200]}...')

if __name__ == '__main__':
    import glob
    txt_files = glob.glob('knowledge_docs/*.txt')
    if txt_files:
        create_vectorstore_from_file(txt_files[0])

        
    demo_retrieval()
