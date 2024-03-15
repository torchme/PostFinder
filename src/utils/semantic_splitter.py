import re
from typing import List
import numpy as np
from scipy.spatial.distance import cosine
import re
from langchain_openai import OpenAIEmbeddings
from typing import List




class SemanticSplitter:
    """
    A class to split text semantically into chunks based on the embeddings similarity.

    Parameters
    ----------
    model : Any
        The sentence embedding model to use.
    buffer_back : int, optional
        The number of sentences to look back for context, by default 1.
    buffer_forward : int, optional
        The number of sentences to look forward for context, by default 1.
    threshold : int, optional
        The percentile threshold to determine breakpoints, by default 90.
    """

    def __init__(
        self,
        model: OpenAIEmbeddings,
        buffer_back: int = 1,
        buffer_forward: int = 1,
        threshold: int = 90,
    ) -> None:
        self.model = model
        self.buffer_back = buffer_back
        self.buffer_forward = buffer_forward
        self.threshold = threshold

    def split(self, text: str) -> List[str]:
        """
        Split the given text into semantically coherent chunks.
        Chucks are not overlapping group of sentences that are semantically coherent.

        Parameters
        ----------
        text : str
            The text to be split.

        Returns
        -------
        List[str]
            A list of semantically coherent text chunks.
        """
        sentences = self._split_text(text)
        combined_sentences = self._combine_sentences(sentences)
        embeddings = self.model.embed_documents(combined_sentences)
        distances = self._calculate_distances(embeddings)
        indices = self._find_breakpoints(distances)
        chunks = self._group_sentences(sentences, indices)
        print(len(distances), len(indices))
        return chunks

    def _split_text(self, text: str) -> List[str]:
        """
        Split the input text into individual sentences based on punctuation and newline characters.

        This method uses regular expressions to identify sentence boundaries, considering periods,
        exclamation points, question marks, and newline characters as potential separators.

        Parameters
        ----------
        text : str
            The text to be split into sentences.

        Returns
        -------
        List[str]
            A list of sentences extracted from the input text.
        """
        pattern = r"[А-Я][^А-Я]*"
        segments = [segment for segment in re.findall(pattern, text) if segment]
        return segments

    def _combine_sentences(self, sentences: List[str]) -> List[str]:
        """
        Combine adjacent sentences to create a context window around each sentence.

        This method creates a sliding window of sentences based on the specified buffer_back and buffer_forward
        parameters, allowing each sentence to be considered within its surrounding context.

        Parameters
        ----------
        sentences : List[str]
            The list of sentences to be combined.

        Returns
        -------
        List[str]
            A list of combined sentences, each representing a contextual window around an individual sentence.

        Examples
        --------
        >>> sentences = ["a", "b", "c", "d", "e"]
        >>> splitter = SemanticSplitter(..., buffer_back=1, buffer_forward=1)
        >>> splitter._combine_sentences(sentences)
        ["a b", "a b c", "b c d", "c d e", "d e"]
        >>> splitter = SemanticSplitter(..., buffer_back=2, buffer_forward=0)
        >>> splitter._combine_sentences(sentences)
        ["a", "a b", "a b c", "b c d", "c d e"]
        >>> splitter = SemanticSplitter(..., buffer_back=1, buffer_forward=2)
        ["a b c", "a b c d", "b c d e", "c d e", "d e"]
        """
        combined_sentences = []
        for i in range(len(sentences)):
            if (i-self.buffer_back)>=0 and (i+self.buffer_forward)<=len(sentences):
                combined = ''.join(sentences[(i - self.buffer_back):(i+self.buffer_forward+1)])
                combined_sentences.append(combined)
            else:
                pass
            
        return combined_sentences

    def _calculate_distances(self, embeddings: np.ndarray) -> List[float]:
        """
        Calculate the cosine distances between consecutive sentence embeddings.

        This method computes the cosine distance between each pair of consecutive embeddings,
        serving as a measure of semantic dissimilarity.

        The length of the returned list will be len(embeddings) - 1.

        Parameters
        ----------
        embeddings : List[np.ndarray]
            The embeddings of the combined sentences.

        Returns
        -------
        List[float]
            A list of distances between consecutive sentence embeddings.

        Examples
        --------
        >>> embeddings = np.array([[1, 0], [0, 1], [0, -1]])
        >>> splitter = SemanticSplitter(...)
        >>> splitter._calculate_distances(embeddings)
        [1.0, 2.0]
        """
        return [float(cosine(embeddings[i], embeddings[i+1])) for i in range(len(embeddings)-1)]

    def _find_breakpoints(self, distances: List[float]) -> List[int]:
        """
        Find indices where the semantic shift is significant.

        Parameters
        ----------
        distances : List[float]
            The list of distances between sentence embeddings.
            distance > threshold is considered a breakpoint.

        Returns
        -------
        List[int]
            Indices indicating where text should be split.

        Examples
        --------
        >>> distances = [0.1, 0.2, 0.3, 0.4, 0.5]
        >>> splitter = SemanticSplitter(..., threshold=60)
        >>> splitter._find_breakpoints(distances)
        [3, 4]
        """
        quantile = np.quantile(a=distances, q=self.threshold/100)
        return [i for i in range(len(distances)) if distances[i] > quantile]

    def _group_sentences(
        self, sentences: List[str], breakpoints: List[int]
    ) -> List[str]:
        """
        Group sentences into chunks based on identified breakpoints.

        This method uses the breakpoints determined from the cosine distances to split the list of sentences
        into semantically coherent chunks.

        Parameters
        ----------
        sentences : List[str]
            The original list of sentences.
        breakpoints : List[int]
            Indices indicating where significant semantic shifts occur, used as split points.

        Returns
        -------
        List[str]
            A list of semantically coherent text chunks, each composed of grouped sentences.

        Examples
        --------
        >>> sentences = ["a", "b", "c", "d", "e"]
        >>> breakpoints = [1, 3]
        >>> splitter = SemanticSplitter(...)
        >>> splitter._group_sentences(sentences, breakpoints)
        ["a b", "c d", "e"]
        """
        chunks = []

        for i, index in enumerate(breakpoints):
            if i==0:
                chunks.append(' '.join(sentences[:(index+1)]))
            elif i!=len(breakpoints):
                chunks.append(' '.join(sentences[(breakpoints[i-1] + 1):(index+1)]))
            else:
                chunks.append(' '.join(sentences[(breakpoints[i-1] + 1):]))
        return chunks