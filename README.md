# Semantic Emoji Search

An application to search for emojis using natural language processing. The application uses a deep learning model to find relevant emojis based on user input.

## Features

- Search for emojis using natural language queries
- Real-time emoji suggestions
- Copy emojis to clipboard with a single click

## Working

The application uses several deep learning concepts to provide intelligent semantic emoji search capabilities. Let's go through the core concepts.

### 1. Sentence Transformers

At the heart of this application is a technology called **Sentence Transformers**. This is a type of deep learning model that can understand the meaning of words and sentences.

**What it does**: The application uses a pre-trained model called `paraphrase-MiniLM-L6-v2` which has already "learned" the relationships between words by processing vast amounts of text from the internet. Think of it as a model that has read millions of books and articles and understands how words relate to each other.

**How it works in simple terms**: When we type a word like "happy", the model doesn't just look for emojis with "happy" in their name. Instead, it understands that concepts like "joy", "cheerful", "smile", and "celebration" are semantically related to happiness, and can find emojis that match these concepts as well.

### 2. Word Embeddings

The model converts words into what are called **embeddings** - essentially long lists of numbers (vectors) that represent the meaning of those words in a multi-dimensional space.

**Simple explanation**: Imagine that each word in the English language can be placed somewhere on a huge map. Words with similar meanings would be placed close together on this map. The embedding is like the coordinates of each word on this map.

For example:
- Words like "happy", "joy", and "delighted" would be clustered close together
- Words like "sad" and "unhappy" would be in another cluster
- Words like "food", "eat", and "meal" would be in yet another cluster

The model in our application creates these number representations (embeddings) for both:
- The emoji descriptions (during initialization)
- The search query (when we search)

### 3. Cosine Similarity

Once both the emojis and our search query are converted into these number representations (vectors), the application uses a mathematical technique called **cosine similarity** to find matches.

**What it means**: Cosine similarity measures the angle between two vectors. The smaller the angle, the more similar the meanings.

**Simple explanation**: Imagine pointing in a direction to represent "happy" and another direction to represent "joy". Since these concepts are similar, we would be pointing in nearly the same direction. The cosine similarity would be close to 1 (maximum similarity). If we pointed in directions for "happy" and "sad", the directions would be very different, and the similarity would be closer to 0.

In the code, this happens in the `search` function of the `EmojiSearchModel` class, where it calculates similarities between our query and all the emoji embeddings.

### 4. Deep Learning Model Architecture

The model being used (`paraphrase-MiniLM-L6-v2`) is a smaller version of much larger language models. It's based on a transformer architecture, which is the same technology that powers models like GPT and BERT.

**What makes it "deep"**: The model consists of multiple layers of artificial neurons stacked on top of each other (hence "deep"). Each layer learns different aspects of language, from simple word patterns to complex semantic relationships.

**Why it's efficient**: The "Mini" in the name indicates this is a compressed version of a larger model. It's been distilled to capture most of the knowledge while being much faster and using less memory, making it suitable for a web application.

### 5. How It All Works Together

Here's the complete flow of how the deep learning works in this application:

1. **Preprocessing**: When the application starts, it takes all emoji names and descriptions and converts them into embeddings (numerical representations) using the Sentence Transformer model.

2. **Query Processing**: When we type a search query, the application converts our query into an embedding using the same model.

3. **Similarity Calculation**: The application calculates how similar our query embedding is to each emoji embedding using cosine similarity.

4. **Ranking**: Emojis are ranked based on their similarity scores, with the most relevant ones (highest similarity) displayed first.

5. **Score Display**: The application shows the match percentage for each emoji, which is derived from the cosine similarity score multiplied by 100.

This approach allows the search to go beyond simple keyword matching and understand the semantic meaning behind our query, providing more intuitive and relevant results.

## Technology Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML, CSS, JavaScript with Bootstrap
- **NLP**: Sentence Transformers for semantic search

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Start the FastAPI server:
   ```
   uvicorn main:app --reload
   ```

## Usage

1. Enter a query in the search box (e.g., "happy", "celebration", "food")
2. The application will display relevant emojis based on our query
3. Click on an emoji to copy it to the clipboard
