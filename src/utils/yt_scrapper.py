import re
import requests
from langchain_community.document_loaders import YoutubeLoader
from src.app.loader import semantic_splitter, emb_fn
from annoy import AnnoyIndex 

def get_subtitles(video_id:str):
    '''
    Function to get subtitles for given video 
    '''    
    loader = YoutubeLoader.from_youtube_url(
    f"https://www.youtube.com/watch?v={video_id}", add_video_info=True,
    language=["ru", "en"], translation="ru",
    )

    docs = loader.load()
    return docs[0].page_content


def parse_video(video_id:str):
    
    subtitles = get_subtitles(video_id=video_id)
    chunks = semantic_splitter.split(subtitles)
      
    return chunks

def get_youtube_docs(query:str, chunks:list):
    query_embedding = emb_fn.embed_query(query)
    print(chunks)
    chunks_embeddings = emb_fn.embed_documents(chunks)
    t = AnnoyIndex(f=len(chunks_embeddings[0]), metric='euclidean')
    for i in range(len(chunks_embeddings)):
        t.add_item(i, chunks_embeddings[i])
    docs = chunks[t.get_nns_by_vector(vector=query_embedding, n=5)] 
    return docs
