import os
from openai import OpenAI, APIConnectionError, RateLimitError, APIStatusError
from typing import List, Dict, Optional

class OpenAIHelper:
    def __init__(self, model: str = None, embedding_model: str = None):
        """
        Initialize the OpenAI helper with specified models.
        
        Args:
            model (str): Chat completion model (default: gpt-3.5-turbo or from env)
            embedding_model (str): Embedding model (default: text-embedding-3-small or from env)
        """
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise EnvironmentError("OPENAI_API_KEY not set in environment.")
        
        # Initialize the OpenAI client
        self.client = OpenAI(api_key=self.api_key)
        
        # Set models with defaults
        self.chat_model = model or os.getenv("OPENAI_CHAT_MODEL", "gpt-3.5-turbo")
        self.embedding_model = embedding_model or os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")

    def get_embedding(self, text: str, dimensions: Optional[int] = None) -> List[float]:
        """
        Get embedding for a single text input.
        
        Args:
            text (str): Input text to embed
            dimensions (int, optional): Optional dimension size for the embedding
            
        Returns:
            List[float]: The embedding vector
            
        Raises:
            RuntimeError: If embedding fails
        """
        try:
            response = self.client.embeddings.create(
                input=[text],
                model=self.embedding_model,
                dimensions=dimensions
            )
            return response.data[0].embedding
        except APIConnectionError as e:
            raise RuntimeError(f"Failed to connect to OpenAI API: {e.__cause__}")
        except (RateLimitError, APIStatusError) as e:
            raise RuntimeError(f"OpenAI API error: {e.message}")
        except Exception as e:
            raise RuntimeError(f"Failed to get embedding: {e}")

    def get_embeddings(self, texts: List[str], dimensions: Optional[int] = None) -> List[List[float]]:
        """
        Get embeddings for multiple text inputs.
        
        Args:
            texts (List[str]): List of texts to embed
            dimensions (int, optional): Optional dimension size for the embeddings
            
        Returns:
            List[List[float]]: List of embedding vectors
        """
        try:
            response = self.client.embeddings.create(
                input=texts,
                model=self.embedding_model,
                dimensions=dimensions
            )
            return [item.embedding for item in response.data]
        except Exception as e:
            raise RuntimeError(f"Failed to get embeddings: {e}")

    def chat(self, 
             messages: List[Dict[str, str]], 
             temperature: float = 0.7, 
             max_tokens: int = 512,
             stream: bool = False,
             **kwargs) -> str:
        """
        Generate chat completion.
        
        Args:
            messages (List[Dict]): Conversation history in format:
                [{"role": "system", "content": "..."}, 
                 {"role": "user", "content": "..."}]
            temperature (float): Creativity parameter (0-2)
            max_tokens (int): Maximum tokens to generate
            stream (bool): Whether to stream the response
            **kwargs: Additional parameters for completion
            
        Returns:
            str: Generated response content
            
        Raises:
            RuntimeError: If chat completion fails
        """
        try:
            response = self.client.chat.completions.create(
                model=self.chat_model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=stream,
                **kwargs
            )
            
            if stream:
                # Handle streaming response
                collected_chunks = []
                for chunk in response:
                    if chunk.choices[0].delta.content is not None:
                        collected_chunks.append(chunk.choices[0].delta.content)
                return "".join(collected_chunks)
            else:
                return response.choices[0].message.content
                
        except APIConnectionError as e:
            raise RuntimeError(f"Failed to connect to OpenAI API: {e.__cause__}")
        except (RateLimitError, APIStatusError) as e:
            raise RuntimeError(f"OpenAI API error: {e.message}")
        except Exception as e:
            raise RuntimeError(f"Chat completion failed: {e}")

    def count_tokens(self, text: str, model: str = None) -> int:
        """
        Count tokens in text using tiktoken.
        
        Args:
            text (str): Input text
            model (str): Model name (for tokenizer)
            
        Returns:
            int: Number of tokens
        """
        try:
            import tiktoken
            model = model or self.chat_model
            encoder = tiktoken.encoding_for_model(model)
            return len(encoder.encode(text))
        except ImportError:
            raise ImportError("Please install tiktoken: pip install tiktoken")
        except Exception as e:
            raise RuntimeError(f"Failed to count tokens: {e}")

    def list_models(self) -> List[str]:
        """
        List available OpenAI models.
        
        Returns:
            List[str]: List of model names
        """
        try:
            models = self.client.models.list()
            return [model.id for model in models.data]
        except Exception as e:
            raise RuntimeError(f"Could not list OpenAI models: {e}")

    def moderate(self, text: str) -> Dict:
        """
        Check if text violates OpenAI's content policy.
        
        Args:
            text (str): Text to moderate
            
        Returns:
            Dict: Moderation results
        """
        try:
            response = self.client.moderations.create(input=text)
            return response.results[0].model_dump()
        except Exception as e:
            raise RuntimeError(f"Moderation failed: {e}")