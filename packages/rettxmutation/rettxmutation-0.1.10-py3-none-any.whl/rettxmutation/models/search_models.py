"""
Azure AI Search Models

Contains models specifically designed for Azure AI Search integration,
including the MutationVectorDocument and related search-specific models.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class MutationVectorDocument(BaseModel):
    """Azure AI Search document model for mutation data with vector embeddings."""
      # --- Core Identifier ---
    id: str
    vector: Optional[List[float]] = Field(default=None, description="Vector embeddings for similarity search")
    
    # --- Filterable & Facetable Metadata ---
    gene_id: Optional[str]
    variant_type: Optional[str]
    
    # --- Flattened Numeric Coordinate Fields ---
    grch37_start: Optional[int]
    grch37_end: Optional[int]
    grch38_start: Optional[int]
    grch38_end: Optional[int]
    
    # --- Primary & Secondary Transcript Positions ---
    primary_cdna_start: Optional[int]
    primary_cdna_end: Optional[int]
    primary_protein_start: Optional[int]
    primary_protein_end: Optional[int]
    secondary_cdna_start: Optional[int]
    secondary_cdna_end: Optional[int]
    secondary_protein_start: Optional[int]
    secondary_protein_end: Optional[int]
    
    # --- Occurrence Count ---
    occurrences: Optional[int]
    
    # --- Display & Filterable String Fields ---
    primary_transcript: Optional[str]
    primary_mutation: Optional[str]
    primary_protein_tlr: Optional[str]
    primary_protein_slr: Optional[str]
    secondary_transcript: Optional[str]
    secondary_mutation: Optional[str]
    secondary_protein_tlr: Optional[str]
    secondary_protein_slr: Optional[str]
    grch37_hgvs: Optional[str]
    grch38_hgvs: Optional[str]
    embedding_model: Optional[str]
    
    # --- Searchable, Tokenized Fields ---
    mutation_tokens: Optional[str]
    literal_mutation_tokens: Optional[List[str]] = Field(
        default=None,
        description="Exact match tokens for mutations, e.g. ['A>T', 'C>T']"
    )
    
    # --- Debugging / Raw Inputs ---
    embedding_input: Optional[str]


class MutationSearchResult(BaseModel):
    """Wrapper for search results with metadata."""
    
    document: MutationVectorDocument
    score: float
    query_context: Optional[str] = None
    highlights: Optional[dict] = None
