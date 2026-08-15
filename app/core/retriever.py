from typing import List
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from app.core.vectorstore import load_vectorstore

def get_retriever(search_type: str = 'similarity', k: int = 3) -> ChromaRetriever:
    """获取检索器
    
    Args:
        search_type: 
            - "similarity": 纯相似度检索（默认）
            - "mmr": 最大边际相关（结果更多样，避免重复）
        k: 返回的文档数
    """
    vectorstore = load_vectorstore()
    return vectorstore.as_retriever(
        search_type = search_type,
        search_kwargs = {'k': k}
    )

def similarity_search_with_score(query:str , k :int = 5,score_threshole:float = 0.0):
    """带相似度分数的检索"""
    vectorstore = load_vectorstore()
    return vectorstore.similarity_search_with_relevance_scores(query, k=k)

def mmr_search(query:str ,k: int = 4,fetch_k: int = 10,lambda_mult:float = 0.5):
    """MMR 检索"""
    vectorstore = load_vectorstore()
    return vectorstore.max_marginal_relevance_search(query,k = k,fetch_k=fetch_k,lambda_mult=lambda_mult)

def demo_search_comparison():
    """对比三种检索方式的效果"""
    queries = [
        "员工福利有哪些？",
        "请假和年假的规定",
    ]
    
    for query in queries:
        print(f"\n{'='*70}")
        print(f"🔍 检索问题: {query}")
        print(f"{'='*70}")

    print('纯相似度检索')
    retriever = get_retriever("similarity", k=3)
    for i,doc in enumerate(retriever.invoke(query),1):
        print(f'{i}.[{doc.metadata.get('source')}]{doc.page_content[:100]}...')
    print("\n📌 MMR 检索 (更多样化):")
    mmr_docs = mmr_search(query,k = 3,fetch_k = 10 ,lambda_mult = 0.5)
    for i,doc in enumerate(mmr_docs,1):
        print(f"  {i}. [{doc.metadata.get('source')}] {doc.page_content[:100]}...")
    print("\n📌 带分数检索 (看相关度):")
    scored_docs = similarity_search_with_score(query, k=3)
    for i,(doc,score) in enumerate(scored_docs,1):
        print(f"  {i}. [{doc.metadata.get('source')}] {doc.page_content[:100]}... {score:.4f}")
        
if __name__ == "__main__":
    demo_search_comparison()

def hybrid_search(query:str,k: int =4,alpha:float = 0.5):

    vectorstore = load_vectorstore()
    vector_docs = vectorstore.similarity_search(query, k=k*2)

    from rank_bm25 import BM25Okapi
    import jieba

    all_docs = vectorstore._collection.get()['documents']
    tokenized_docs = [list(jieba.cut(doc)) for doc in all_docs]
    tokenized_query = list(jieba.cut(query))

    bm25 = BM25Okapi(tokenized_docs)
    bm25_scores = bm25.get_scores(tokenized_query)
    bm25_top_indices = sorted(range(len(bm25_scores)), key=lambda i: bm25_scores[i], reverse=True)[:k*2]

# 这里简化处理，实际项目用 RRF (Reciprocal Rank Fusion)
    return vector_docs[:k]
