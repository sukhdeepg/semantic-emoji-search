import numpy as np
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class EmojiSearchModel:
    """
    A class that uses deep learning to search for emojis based on user input.
    """
    
    def __init__(self, emoji_data: List[Dict[str, Any]]):
        """
        Initialize the EmojiSearchModel with the emoji dataset and deep learning model.
        
        Args:
            emoji_data (List[Dict[str, Any]]): List of emoji dictionaries containing emoji, name, and group.
        """
        self.emoji_data = emoji_data
        
        # Load pre-trained sentence transformer model
        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
        
        # Create embeddings for all emoji names and store them
        self.emoji_embeddings = self._create_emoji_embeddings()
    
    def _create_emoji_embeddings(self) -> np.ndarray:
        """
        Create embeddings for all emoji names using the deep learning model.
        
        Returns:
            np.ndarray: Array of emoji embeddings.
        """
        emoji_texts = []
        
        # Collect text descriptions for each emoji
        for emoji_entry in self.emoji_data:
            name = emoji_entry["name"]
            
            # Create a rich description for the embedding
            description = f"{name}"
            if "keywords" in emoji_entry:
                description += " " + " ".join(emoji_entry["keywords"])
                
            emoji_texts.append(description)
        
        # Create embeddings
        embeddings = self.model.encode(emoji_texts)
        return embeddings
    
    def search(self, query: str, top_k: int = 20) -> List[Dict[str, Any]]:
        """
        Search for emojis based on the user query.
        
        Args:
            query (str): The user query.
            top_k (int): Number of top results to return.
            
        Returns:
            List[Dict[str, Any]]: List of top matching emoji dictionaries with additional score.
        """
        # Encode the user query
        query_embedding = self.model.encode([query])[0]
        
        # Calculate similarity with all emoji embeddings
        similarities = cosine_similarity([query_embedding], self.emoji_embeddings)[0]
        
        # Get indices of top k results
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        # Create results with similarity scores
        results = []
        for idx in top_indices:
            emoji_entry = self.emoji_data[idx].copy()
            emoji_entry["score"] = float(similarities[idx])
            results.append(emoji_entry)
            
        return results 