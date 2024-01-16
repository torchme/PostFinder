from typing import List
from langchain_community.vectorstores.chroma import Chroma
from langchain_community.document_loaders import DataFrameLoader
from langchain_core.documents import Document
import pandas as pd

from src.app.loader import emb_fn
from src.handlers.utils.scrapper import scrape_telegram_messages
from src.app.loader import client


class ChromaManager:
    def __init__(
        self, channel: str, persist_directory: str = "./chroma_db", emb_fn=emb_fn
    ):
        self.persist_directory = persist_directory
        self.emb_fn = emb_fn
        self.channel = channel
        self.collection = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.emb_fn,
            collection_name=self.channel,
        )

    def create_collection(self, docs: List[Document]) -> None:
        self.collection.from_documents(
            documents=docs,
            embedding=self.emb_fn,
            persist_directory=self.persist_directory,
            collection_name=self.channel,
        )

    def last_msg_id(self):
        metadatas = self.collection.get()["metadatas"]
        last_metadata = max(metadatas, key=lambda x: x["message_id"])
        last_message_id = last_metadata["message_id"]

        return last_message_id

    def dataframe_to_documents(self, data: pd.DataFrame) -> List[Document]:
        loader = DataFrameLoader(data, page_content_column="text")
        return loader.load()

    def collection_exists(self) -> bool:
        return bool(self.collection.get()["ids"])

    async def update_collection(self):
        if self.collection_exists():
            last_message_id = self.last_msg_id()
            new_data = await scrape_telegram_messages(
                client=client, channel=self.channel, min_id=last_message_id
            )
            if new_data:
                df = pd.DataFrame(new_data)
                print(df)
                docs = self.dataframe_to_documents(df)
                self.collection.add_documents(docs)
        else:
            initial_data = await scrape_telegram_messages(
                client=client, channel=self.channel
            )
            if initial_data:
                df = pd.DataFrame(initial_data)
                print(df)
                docs = self.dataframe_to_documents(df)
                self.create_collection(docs)
