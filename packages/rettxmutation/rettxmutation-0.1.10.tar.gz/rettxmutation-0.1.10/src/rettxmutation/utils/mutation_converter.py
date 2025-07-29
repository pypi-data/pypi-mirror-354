"""
Mutation Conversion Utilities

Utilities for converting between different mutation model representations,
particularly between Azure AI Search documents and internal gene models.
"""

import logging
from typing import Optional, List, Dict
from ..models.search_models import MutationVectorDocument
from ..models.gene_models import GeneMutation, TranscriptMutation, GenomicCoordinate
from ..models.mutation_model import Mutation

logger = logging.getLogger(__name__)


class MutationConverter:
    """Utility class for converting between mutation model formats."""
    
    @staticmethod
    def document_to_gene_mutation(doc: MutationVectorDocument) -> GeneMutation:
        """
        Convert MutationVectorDocument to GeneMutation.
        
        Args:
            doc: The Azure AI Search document
            
        Returns:
            GeneMutation object with data mapped from the search document
        """
        try:
            # Build primary transcript if available
            primary_transcript = None
            if doc.primary_transcript and doc.primary_mutation:
                primary_transcript = TranscriptMutation(
                    gene_id=doc.gene_id,
                    transcript_id=doc.primary_transcript,
                    hgvs_transcript_variant=doc.primary_mutation,
                    protein_consequence_tlr=doc.primary_protein_tlr,
                    protein_consequence_slr=doc.primary_protein_slr
                )
            # Build secondary transcript if available
            secondary_transcript = None
            if doc.secondary_transcript and doc.secondary_mutation:
                secondary_transcript = TranscriptMutation(
                    gene_id=doc.gene_id,
                    transcript_id=doc.secondary_transcript,
                    hgvs_transcript_variant=doc.secondary_mutation,
                    protein_consequence_tlr=doc.secondary_protein_tlr,
                    protein_consequence_slr=doc.secondary_protein_slr
                )
            # Build genomic coordinates
            genomic_coordinates = {}
            if doc.grch37_start is not None and doc.grch37_end is not None and doc.grch37_hgvs:
                genomic_coordinates["GRCh37"] = GenomicCoordinate(
                    assembly="GRCh37",
                    hgvs=doc.grch37_hgvs,
                    start=doc.grch37_start,
                    end=doc.grch37_end
                )
            if doc.grch38_start is not None and doc.grch38_end is not None and doc.grch38_hgvs:
                genomic_coordinates["GRCh38"] = GenomicCoordinate(
                    assembly="GRCh38",
                    hgvs=doc.grch38_hgvs,
                    start=doc.grch38_start,
                    end=doc.grch38_end
                )
            # Build the GeneMutation object
            gene_mutation = GeneMutation(
                variant_type=doc.variant_type,
                primary_transcript=primary_transcript,
                secondary_transcript=secondary_transcript,
                genomic_coordinates=genomic_coordinates if genomic_coordinates else None
            )
            
            return gene_mutation
            
        except Exception as e:
            logger.error(f"Error converting MutationVectorDocument to GeneMutation: {e}")
            logger.error(f"Document data: {doc.model_dump()}")
            raise
    
    @staticmethod
    def documents_to_gene_mutations(docs: List[MutationVectorDocument]) -> List[GeneMutation]:
        """Convert a list of MutationVectorDocuments to GeneMutations."""
        mutations = []
        for doc in docs:
            try:
                mutation = MutationConverter.document_to_gene_mutation(doc)
                mutations.append(mutation)
            except Exception as e:
                logger.warning(f"Failed to convert document {doc.id}: {e}")
                continue
        return mutations
    
    @staticmethod
    def gene_mutation_to_document(mutation: GeneMutation) -> MutationVectorDocument:
        """
        Convert GeneMutation back to MutationVectorDocument.
        Note: This requires vector embeddings to be generated separately.        """
        # Extract coordinate data
        grch37_coord = mutation.genomic_coordinates.get("GRCh37") if mutation.genomic_coordinates else None
        grch38_coord = mutation.genomic_coordinates.get("GRCh38") if mutation.genomic_coordinates else None
        
        return MutationVectorDocument(
            id=f"converted_{hash(str(mutation))}",  # Generate a unique ID
            vector=[],  # Vector needs to be generated separately
            gene_id=mutation.primary_transcript.gene_id if mutation.primary_transcript and mutation.primary_transcript.gene_id else "UNKNOWN",
            variant_type=mutation.variant_type,

            # GRCh37 coordinates
            grch37_start=grch37_coord.start if grch37_coord else None,
            grch37_end=grch37_coord.end if grch37_coord else None,
            grch37_hgvs=grch37_coord.hgvs if grch37_coord else None,

            # GRCh38 coordinates
            grch38_start=grch38_coord.start if grch38_coord else None,
            grch38_end=grch38_coord.end if grch38_coord else None,
            grch38_hgvs=grch38_coord.hgvs if grch38_coord else None,

            # Primary transcript
            primary_transcript=mutation.primary_transcript.transcript_id if mutation.primary_transcript else None,
            primary_mutation=mutation.primary_transcript.hgvs_transcript_variant if mutation.primary_transcript else None,
            primary_protein_tlr=mutation.primary_transcript.protein_consequence_tlr if mutation.primary_transcript else None,
            primary_cdna_start=None, # Not stored in TranscriptMutation model
            primary_cdna_end=None, # Not stored in TranscriptMutation model
            primary_protein_start=None, # Not stored in TranscriptMutation model
            primary_protein_end=None, # Not stored in TranscriptMutation model

            # Secondary transcript
            secondary_transcript=mutation.secondary_transcript.transcript_id if mutation.secondary_transcript else None,
            secondary_mutation=mutation.secondary_transcript.hgvs_transcript_variant if mutation.secondary_transcript else None,
            secondary_protein_tlr=mutation.secondary_transcript.protein_consequence_tlr if mutation.secondary_transcript else None,
            secondary_cdna_start=None, # Not stored in TranscriptMutation model
            secondary_cdna_end=None, # Not stored in TranscriptMutation model
            secondary_protein_start=None, # Not stored in TranscriptMutation model
            secondary_protein_end=None, # Not stored in TranscriptMutation model
            
            # Metadata (using defaults since GeneMutation doesn't store these)
            occurrences=None,
            embedding_model=None,
            mutation_tokens=None,
            literal_mutation_tokens=None
        )
