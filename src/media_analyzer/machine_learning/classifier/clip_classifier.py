from functools import lru_cache
from typing import Any

import numpy as np
from numpy.typing import NDArray
from scipy.special import softmax
from sklearn.metrics.pairwise import cosine_similarity

from media_analyzer.machine_learning.classifier.base_classifier import BaseClassifier
from media_analyzer.machine_learning.embedding.clip_embedder import CLIPEmbedder
from media_analyzer.machine_learning.embedding.embedder_protocol import EmbedderProtocol


class CLIPClassifier(BaseClassifier):
    embedder:EmbedderProtocol

    def __init__(self, embedder: EmbedderProtocol= CLIPEmbedder()) -> None:
        self.embedder = embedder

    @lru_cache
    def cached_embed_text(self, text: str) -> NDArray[Any]:
        return self.embedder.embed_text(text)

    def classify_image(
            self,
            image_embedding: NDArray[Any],
            classes: list[str],
    ) -> tuple[int, float]:
        text_embeddings = [self.cached_embed_text(c) for c in classes]
        similarities = cosine_similarity([image_embedding], text_embeddings)
        normalized: NDArray[Any] = softmax(similarities)
        best_index = np.argmax(normalized)
        confidence = normalized[0, best_index].item()
        return int(best_index), confidence

    def binary_classify_image(
            self,
            image_embedding: NDArray[Any],
            positive_prompt: str,
            negative_prompt: str,
    ) -> tuple[bool, float]:
        index, confidence = self.classify_image(
            image_embedding,
            [negative_prompt, positive_prompt],
        )
        return bool(index), confidence
