import re
import requests
from langchain_community.document_loaders import YoutubeLoader
from src.app.loader import semantic_splitter, emb_fn
import numpy as np
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
    '''
    Function to split video subtitle to chunks with langchain SemunticChunker
    '''
    subtitles = get_subtitles(video_id=video_id)
    sents = re.findall('[А-Я][^А-Я]*', subtitles)
    text_with_punctuation = ''.join(map(lambda x: x.strip()+'. ', sents))
    chunks = semantic_splitter.create_documents([text_with_punctuation])
    chunks = [chunk.page_content for chunk in chunks]
    return chunks

def get_youtube_docs(query:str, chunks:list):
    '''
    Function for semantic search
    '''
    query_embedding = emb_fn.embed_query(query)
    chunks_embeddings = emb_fn.embed_documents(chunks)
    t = AnnoyIndex(f=len(chunks_embeddings[0]), metric='euclidean')
    for i in range(len(chunks_embeddings)):
        t.add_item(i, chunks_embeddings[i])
    t.build(10)
    index = t.get_nns_by_vector(vector=query_embedding, n=1)
    docs = chunks[index] 
    return docs
