import re
import numpy as np
from langchain_community.document_loaders import YoutubeLoader
from langchain.docstore.document import Document
from annoy import AnnoyIndex 
from src.app.loader import semantic_splitter, emb_fn


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

def split_subtitles(subtitles:str):
    '''
    Function to split video subtitles to chunks with langchain SemunticChunker
    '''
    print(subtitles)
    sents = re.findall('[А-Я][^А-Я]*', subtitles)
    text_with_punctuation = ''.join(map(lambda x: x.strip()+'. ', sents))
    chunks = semantic_splitter.create_documents([text_with_punctuation])
    chunks = [chunk.page_content for chunk in chunks]
    return chunks

def get_youtube_docs(query:str, chunks:list):
    '''
    Function for semantic search with spotify annoy
    '''
    query_embedding = emb_fn.embed_query(query)
    chunks_embeddings = emb_fn.embed_documents(chunks)
    t = AnnoyIndex(f=len(chunks_embeddings[0]), metric='euclidean')
    for i in range(len(chunks_embeddings)):
        t.add_item(i, chunks_embeddings[i])
    t.build(10)
    index = t.get_nns_by_vector(vector=query_embedding, n=1)[0]
    print(index)
    docs = chunks[index] 
    return docs


def youtube_semantic_search(video_id:str, query:str):
    '''
    Final pipeline function
    '''
    subtitles = get_subtitles(video_id=video_id)
    chunks = split_subtitles(subtitles=subtitles)
    relevant_doc = get_youtube_docs(query, chunks)
    relevant_doc = Document(page_content=relevant_doc,
                            metadata={"source": "local"})
    
    return [relevant_doc], ['a', 'b']
