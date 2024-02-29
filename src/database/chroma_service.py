from typing import List
from langchain_community.vectorstores.chroma import Chroma
from langchain_community.document_loaders import DataFrameLoader
from langchain_core.documents import Document
import pandas as pd

from src.app.loader import emb_fn
from src.utils.scrapper import scrape_telegram_messages
from src.app.loader import client


class ChromaManager:
    def __init__(
        self, channel: str, persist_directory: str = "./chroma_db", emb_fn=emb_fn
    ):
        """
        Initialize the ChromaDB object.

        Parameters
        ----------
        channel : str
            The name of the channel.
        persist_directory : str, optional
            The directory to persist the ChromaDB data. Defaults to "./chroma_db".
        emb_fn
            The embedding function.
        """
        self.persist_directory = persist_directory
        self.emb_fn = emb_fn
        self.channel = channel
        self.collection = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.emb_fn,
            collection_name=self.channel,
        )

    async def create_collection(self, docs: List[Document]) -> None:
        """
        Asynchronously creates a collection with the given list of documents.

        Parameters
        ----------
        docs : List[Document]
            The list of documents to be added to the collection.

        Returns
        -------
        None
        """
        await self.collection.afrom_documents(
            documents=docs,
            embedding=self.emb_fn,
            persist_directory=self.persist_directory,
            collection_name=self.channel,
        )

    def last_msg_id(self):
        """
        Returns the last message ID from the metadatas collection.
        """
        metadatas = self.collection.get()["metadatas"]
        last_metadata = max(metadatas, key=lambda x: x["message_id"])
        last_message_id = last_metadata["message_id"]

        return last_message_id

    def dataframe_to_documents(self, data: pd.DataFrame) -> List[Document]:
        """
        Convert a pandas DataFrame to a list of Document objects.

        Parameters
        ----------
        data : pd.DataFrame
            The input pandas DataFrame.

        Returns
        -------
        List[Document]
            A list of Document objects.
        """
        loader = DataFrameLoader(data, page_content_column="text")
        return loader.load()

    def collection_exists(self) -> bool:
        """
        Check if the collection exists and return a boolean value.
        """
        return bool(self.collection.get()["ids"])

    async def update_collection(self):
        """
        An async function that updates the collection. It checks if the collection exists, and if so, it retrieves the last message ID and scrapes new data from the Telegram messages. If new data is found, it creates a dataframe, converts it to documents, and adds the documents to the collection. If the collection does not exist, it scrapes initial data from the Telegram messages, creates a dataframe, converts it to documents, and creates a new collection. After the update, it sets the collection with a new Chroma instance.
        """
        if self.collection_exists():
            last_message_id = self.last_msg_id()
            new_data = await scrape_telegram_messages(
                client=client, channel=self.channel, min_id=last_message_id
            )
            if new_data:
                df = pd.DataFrame(new_data)
                docs = self.dataframe_to_documents(df)
                await self.collection.aadd_documents(docs)
        else:
            initial_data = await scrape_telegram_messages(
                client=client, channel=self.channel
            )
            if initial_data:
                df = pd.DataFrame(initial_data)
                docs = self.dataframe_to_documents(df)
                await self.create_collection(docs)

        self.collection = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.emb_fn,
            collection_name=self.channel,
        )
