# from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.embeddings import DashScopeEmbeddings



# def get_embeddings():
#     return HuggingFaceEmbeddings(
#         model_name="BAAI/bge-small-zh-v1.5",
#         model_kwargs={"device": "cpu"},
#         encode_kwargs={"normalize_embeddings": True},
#     )

def get_embeddings():
    return DashScopeEmbeddings(model="text-embedding-v2")
def demo_embedding_intution():
    import numpy as np

    embeddings = get_embeddings()
    # embeddings = DashScopeEmbeddings(model="text-embedding-v2")

    sentences = [
        "员工年假有几天？",
        "我想请假出去玩",
        "公司考勤制度是什么？",
        "今天天气真好啊",
    ]

    vectors = embeddings.embed_documents(sentences)

    print('句子之间的余弦相似度矩阵：\n')
    print(f'{'':20s}',end = '')
    for s in sentences:
        print(f'{s[:15]}:15s',end = '')
    print('\n')

    for i , s1 in enumerate(sentences):
        print(f'{s1[:20]}:20s',end = '')
        for j , s2 in enumerate(sentences):
            v1 = np.array(vectors[i])
            v2 = np.array(vectors[j])
            cos_sin = np.dot(v1,v2)/(np.linalg.norm(v1)*np.linalg.norm(v2))
            print(f'{cos_sin:.3f}',end = '')
        print('\n')

    print("\n💡 观察：语义相关的句子（年假-请假、考勤制度-年假）相似度应该更高")
    print("💡 无关的句子（天气）和其他句子相似度应该更低")

if __name__ == '__main__':
    demo_embedding_intution()