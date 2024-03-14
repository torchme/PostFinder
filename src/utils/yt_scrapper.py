import requests
from langchain_community.document_loaders import YoutubeLoader
import re
from src.app.loader import semantic_splitter


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

