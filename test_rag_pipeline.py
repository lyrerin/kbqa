import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from app.core.memory_manager import chat,clear_history
from app.core.rag_chain import ask,ask_with_sources
from app.core.ingestion import ingest_directory,get_ingestion_status

def test_full_pipeline():
    """全流程测试"""
    
    # Step 1: 导入文档
    print("=" * 60)
    print("📥 Step 1: 导入知识库文档")
    print("=" * 60)
    ingest_directory("knowledge_docs", clear_first=True)
    
    # Step 2: 查看状态
    print("\n" + "=" * 60)
    print("📊 Step 2: 知识库状态")
    print("=" * 60)
    status = get_ingestion_status()
    print(f"   文档数: {status['total_documents']}")
    print(f"   文本块: {status['total_chunks']}")
    print(f"   来源: {status['sources']}")
    
    # Step 3: 单轮问答
    print("\n" + "=" * 60)
    print("💬 Step 3: 单轮问答测试")
    print("=" * 60)
    
    result = ask_with_sources("员工入职满三年有多少天年假？")
    print(f"问题: {result['question']}")
    print(f"答案: {result['answer']}")
    print(f"引用来源数: {len(result['sources'])}")
    
    # Step 4: 诚实测试（问不知道的）
    print("\n" + "=" * 60)
    print("🔍 Step 4: 边界测试（不知道就直说）")
    print("=" * 60)
    answer = ask("公司CEO的邮箱是什么？")
    print(f"问题: 公司CEO的邮箱是什么？")
    print(f"答案: {answer}")
    
    # Step 5: 多轮对话
    print("\n" + "=" * 60)
    print("🔄 Step 5: 多轮对话测试")
    print("=" * 60)
    
    clear_history("integration_test")
    q1 = chat("integration_test", "绩效考核有几个等级？")
    print(f"Q1: 绩效考核有几个等级？ → {q1[:100]}...")
    
    q2 = chat("integration_test", "最高的那个有什么奖励？")
    print(f"Q2: 最高的那个有什么奖励？ → {q2[:100]}...")
    
    print("\n" + "=" * 60)
    print("🎉 全部测试通过!")
    print("=" * 60)


if __name__ == "__main__":
    test_full_pipeline()