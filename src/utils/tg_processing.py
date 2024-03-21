from src.database.chroma_service import ChromaManager
from src.app.loader import extractor

async def telegram_semantic_search(channel:str, query:str):
    chroma_manager = ChromaManager(channel=channel)
    await chroma_manager.update_collection()
    retriever = chroma_manager.collection.as_retriever()
    docs = retriever.get_relevant_documents(extractor.add_features(query=query), search_kwargs={"k": 5})
    relevant_post_urls = [
    f"[Пост {i+1}](t.me/{channel}/{doc.metadata['message_id']})"
    for i, doc in enumerate(docs)
][:5]
    
    return docs, relevant_post_urls

