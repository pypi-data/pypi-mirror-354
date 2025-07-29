import logging
import numpy as np
from typing import List, Dict, Any
from rettxmutation.models.mutation_model import Mutation
from rettxmutation.models.gene_models import GeneMutation
from rettxmutation.openai_agent.embedding_client import EmbeddingClient
from rettxmutation.config import RettxConfig, validate_config_fields

logger = logging.getLogger(__name__)


class EmbeddingService:
    """
    Service for creating and managing embeddings from GeneMutation objects.
    
    This service integrates with Azure OpenAI to create embeddings for search, clustering,
    or similarity comparisons of genetic mutations. It follows Azure best practices for
    error handling, retry logic, and resource management.
    """

    def __init__(self, config: RettxConfig):
        """
        Initialize the embedding service with configuration.
        
        The service validates its required configuration fields and creates the
        embedding client with proper error handling and resource management.

        Args:
            config: Configuration object implementing RettxConfig protocol
            
        Raises:
            ValueError: If required configuration fields are missing or invalid
        """
        # Validate required configuration fields for this service
        required_fields = [
            'RETTX_OPENAI_ENDPOINT',
            'RETTX_OPENAI_KEY',
            'RETTX_EMBEDDING_DEPLOYMENT',
            'RETTX_OPENAI_MODEL_VERSION',
            'RETTX_OPENAI_MODEL_NAME'
        ]
        validate_config_fields(config, required_fields, 'EmbeddingService')
        
        # Store config for internal use
        self._config = config
        
        # Initialize the embedding client with validated configuration
        try:
            self.embedding_client = EmbeddingClient(
                api_key=config.RETTX_OPENAI_KEY,
                api_version=config.RETTX_OPENAI_MODEL_VERSION,
                azure_endpoint=config.RETTX_OPENAI_ENDPOINT,
                model_name=config.RETTX_OPENAI_MODEL_NAME,
                embedding_deployment=config.RETTX_EMBEDDING_DEPLOYMENT
            )
            logger.debug("EmbeddingService initialized with Azure OpenAI client")
        except Exception as e:
            logger.error(f"Failed to initialize EmbeddingClient: {e}")
            raise ValueError(f"EmbeddingService initialization failed: {e}") from e

    @staticmethod
    def mutation_to_embedding_string(mutation: GeneMutation) -> str:
        """
        Convert a GeneMutation to a string for embedding

        Args:
            mutation: The GeneMutation object to convert

        Returns:
            str: String representation of the mutation
        """
        parts = []

        # gene (use primary if present, else secondary)
        gene = (
            mutation.primary_transcript.gene_id
            if mutation.primary_transcript and mutation.primary_transcript.gene_id
            else getattr(mutation.secondary_transcript, "gene_id", "")
        )
        parts.append(f"Gene: {gene}")

        # primary transcript/protein
        if mutation.primary_transcript:
            pt = mutation.primary_transcript
            parts.append(f"Primary transcript: {pt.hgvs_transcript_variant}")
            if pt.protein_consequence_slr or pt.protein_consequence_tlr:
                prot = pt.protein_consequence_slr or pt.protein_consequence_tlr
                parts.append(f"Primary protein: {prot}")

        # secondary transcript/protein
        if mutation.secondary_transcript:
            st = mutation.secondary_transcript
            parts.append(f"Secondary transcript: {st.hgvs_transcript_variant}")
            if st.protein_consequence_slr or st.protein_consequence_tlr:
                sprot = st.protein_consequence_slr or st.protein_consequence_tlr
                parts.append(f"Secondary protein: {sprot}")

        # variant type
        parts.append(f"Variant type: {mutation.variant_type}")

        # genomic coords (pick both assemblies if present)
        if mutation.genomic_coordinates:
            for coord in mutation.genomic_coordinates.values():
                parts.append(f"{coord.assembly}: {coord.hgvs}")
        # legacy fallback
        elif mutation.genomic_coordinate:
            parts.append(f"Genomic coordinate: {mutation.genomic_coordinate}")

        # domain context
        parts.append("Rett Syndrome")

        return " | ".join(parts)

    @staticmethod
    def parse_hgvs_string(input: str) -> Mutation:
        """
        Get mutation details from an input string.

        Args:
            input: The input string to parse

        Returns:
            Mutation: The parsed mutation object
        """        # This should be replaced with actual parsing logic
        # Example for OpenAI:
        # response = openai.Mutation.create(input=input)
        # mutation = response["data"]

        # Placeholder:
        mutation = Mutation.from_hgvs_string(input)
        return mutation

    def create_embedding(self, mutation: GeneMutation) -> np.ndarray:
        """
        Convert a GeneMutation object to an embedding vector using Azure OpenAI.

        Args:
            mutation: The GeneMutation object to convert

        Returns:
            numpy.ndarray: The embedding vector from Azure OpenAI
            
        Raises:
            Exception: If embedding generation fails after retries
        """
        # Convert the mutation to a string representation
        text = self.mutation_to_embedding_string(mutation)
        logger.debug(f"Creating embedding for mutation text: {text[:100]}...")

        # Generate embedding using Azure OpenAI client
        return self._get_embedding_from_model(text)

    def create_embeddings(self, mutations: List[GeneMutation]) -> List[np.ndarray]:
        """        Create embeddings for a list of mutations.

        Args:
            mutations: List of GeneMutation objects

        Returns:
            List of embedding vectors
        """
        return [self.create_embedding(mutation) for mutation in mutations]

    def _get_embedding_from_model(self, text: str) -> np.ndarray:
        """
        Get embedding from Azure OpenAI using the configured embedding client.
        
        Implements Azure best practices with proper error handling and retry logic
        (handled by the EmbeddingClient's backoff decorator).

        Args:
            text: The text to embed

        Returns:
            numpy.ndarray: The embedding vector from Azure OpenAI
            
        Raises:
            Exception: If embedding generation fails after retries
        """
        try:
            logger.debug(f"Generating embedding for text of length: {len(text)}")
            
            # Use Azure OpenAI client with built-in retry logic
            embedding_vector = self.embedding_client.create_embedding(text)
            
            # Convert to numpy array for consistency with existing interface
            embedding_array = np.array(embedding_vector, dtype=np.float32)
            
            logger.debug(f"Successfully generated embedding vector of dimension: {len(embedding_array)}")
            return embedding_array
            
        except Exception as e:
            logger.error(f"Error generating embedding from Azure OpenAI: {str(e)}")
            # Re-raise the exception to fail fast as per requirements
            raise RuntimeError(f"Failed to generate embedding: {str(e)}") from e

    def find_similar_mutations(
        self,
        query_mutation: GeneMutation,
        mutation_library: List[GeneMutation],
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Find mutations similar to the query mutation using Azure OpenAI embeddings.

        Args:
            query_mutation: The mutation to find similar mutations for
            mutation_library: The library of mutations to search
            top_k: The number of similar mutations to return

        Returns:
            List of dictionaries with mutation and similarity score
        """
        query_embedding = self.create_embedding(query_mutation)

        results = []
        for mutation in mutation_library:
            mutation_embedding = self.create_embedding(mutation)
            similarity = self._calculate_similarity(query_embedding, mutation_embedding)
            results.append({
                "mutation": mutation,
                "similarity": similarity
            })

        # Sort by similarity score (highest first)
        results.sort(key=lambda x: x["similarity"], reverse=True)

        # Return top_k results
        return results[:top_k]

    @staticmethod
    def _calculate_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Calculate cosine similarity between two vectors.

        Args:
            vec1: First vector
            vec2: Second vector

        Returns:
            float: Cosine similarity score between 0 and 1
        """
        # Cosine similarity: dot product divided by the product of magnitudes
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        # Avoid division by zero
        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)
