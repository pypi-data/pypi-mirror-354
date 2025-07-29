"""
Variant Validator Service - Business Logic Layer

This service contains the business logic for variant validation operations,
acting as an intermediary between pipelines and the VariantValidator repository.
It handles:
- Variant normalization with error handling
- Transcript resolution and versioning logic  
- Response processing and mapping
- Variant formatting operations

Follows the 3-layer architecture:
- Pipelines use this service for business operations
- This service uses the VariantValidatorRepository for infrastructure
"""

import logging
from typing import Optional, Tuple, List, Dict, Any

from rettxmutation.models.gene_models import TranscriptMutation, GeneMutation, GenomicCoordinate
from rettxmutation.models.gene_registry import registry
from rettxmutation.models.gene_assembly import GenomeAssembly
from rettxmutation.utils.hgvs_descriptor import HgvsDescriptor
from rettxmutation.repositories import (
    VariantValidatorRepository,
    VariantValidatorNormalizationError
)
from rettxmutation.services.variant_validator_mapping_service import VariantValidatorMappingService

logger = logging.getLogger(__name__)


class VariantValidatorService:
    """
    Business logic service for VariantValidator operations.
    
    Handles variant normalization, transcript resolution, and response processing
    while delegating infrastructure concerns to the repository.
    """

    def __init__(self, repository: VariantValidatorRepository):
        """
        Initialize the service with a VariantValidator repository.
        
        Args:
            repository: VariantValidator repository for infrastructure operations
        """
        self._repository = repository
        self._mapping_service = VariantValidatorMappingService()

    def close(self):
        """Clean up any open sessions or resources."""
        self._repository.close()

    def normalize_variant_to_assemblies(
        self, 
        hgvs_string: str, 
        target_assembly: str = "grch38", 
        legacy_assembly: Optional[str] = "grch37"
    ) -> Dict[str, Tuple[str, int]]:
        """
        Normalize transcript-level HGVS to genomic HGVS + position across assemblies.
        
        Args:
            hgvs_string: HGVS variant description
            target_assembly: Primary genome assembly
            legacy_assembly: Optional legacy assembly for cross-reference
            
        Returns:
            Dict mapping assembly names to (hgvs, position) tuples
            
        Raises:
            VariantValidatorNormalizationError: If normalization fails
            ValueError: If input format is invalid
        """
        transcript, detail = self._split_and_resolve_transcript(hgvs_string)

        def normalize_to_assembly(build: str) -> Tuple[str, int]:
            """Normalize to a specific genome assembly."""
            try:
                response = self._repository.normalize_variant(
                    genome_build=build,
                    variant_description=f"{transcript}:{detail}",
                    select_transcripts=transcript
                )
            except VariantValidatorNormalizationError as e:
                logger.error(f"Normalization error on {build} for {hgvs_string}: {e}")
                raise

            if response.get("messages"):
                raise Exception(f"Normalization warnings: {response['messages']}")

            unwrapped = self._mapping_service.unwrap_response(response)
            loci = unwrapped.get("primary_assembly_loci", {})
            details = loci.get(build.lower()) or loci.get(build)
            
            if not details:
                raise ValueError(f"No primary_assembly_loci for {build}")
                
            hgvs = details["hgvs_genomic_description"]
            pos = int(details["vcf"]["pos"])
            return hgvs, pos

        # Normalize to target assembly
        result = {target_assembly: normalize_to_assembly(target_assembly)}
        
        # Optionally normalize to legacy assembly
        if legacy_assembly and legacy_assembly != target_assembly:
            result[legacy_assembly] = normalize_to_assembly(legacy_assembly)
            return result

    def normalize_complex_variant(
        self,
        assembly_build: str,
        assembly_refseq: str,
        hgvs_complex: str
    ) -> Dict[str, Tuple[str, int]]:
        """
        Normalize a complex variant (large del/dup/ins) across genome assemblies.
        
        Args:
            assembly_build: Genome build (e.g., "GRCh38")
            assembly_refseq: Reference sequence (e.g., "NC_000023.11")
            hgvs_complex: Complex HGVS variant description (can be full HGVS or just variant part)
            
        Returns:
            Dict mapping assembly build names to (hgvs, position) tuples
            
        Raises:
            VariantValidatorNormalizationError: If normalization fails
        """
        # Check if hgvs_complex already contains a reference sequence
        if ":" in hgvs_complex:
            # Full HGVS string already provided (e.g., "NC_000023.11:g.154031326G>A")
            variant_description = hgvs_complex
        else:
            # Only variant part provided (e.g., "g.154031326G>A")
            variant_description = f"{assembly_refseq}:{hgvs_complex}"

        try:
            response = self._repository.normalize_variant(
                genome_build=assembly_build,
                variant_description=variant_description,
                select_transcripts=assembly_refseq
            )
        except VariantValidatorNormalizationError as e:
            logger.error(f"Normalization error on {assembly_build} for {hgvs_complex}: {e}")
            raise

        if response.get("messages"):
            raise Exception(f"Normalization warnings: {response['messages']}")

        unwrapped = self._mapping_service.unwrap_response(response)
        loci = unwrapped.get("primary_assembly_loci", {})
        
        # Also check alt_genomic_loci for alternative assemblies (like grch37)
        alt_loci = unwrapped.get("alt_genomic_loci", [])
        
        results: Dict[str, Tuple[str, int]] = {}
        
        # Process primary assembly loci
        for build_key, details in loci.items():
            hgvs = details["hgvs_genomic_description"]
            pos = int(details["vcf"]["pos"])
            results[build_key.lower()] = (hgvs, pos)
        
        # Process alternative assembly loci
        for alt_entry in alt_loci:
            for build_key, details in alt_entry.items():
                hgvs = details["hgvs_genomic_description"]
                pos = int(details["vcf"]["pos"])
                results[build_key.lower()] = (hgvs, pos)

        return results

    def get_transcript_and_protein_annotations(
        self,
        genomic_hgvs: str,
        primary_transcript: str,
        secondary_transcript: Optional[str] = None,
        genome_build: str = "GRCh38"
    ) -> Dict[str, Dict[str, Any]]:
        """
        Get transcript and protein annotations for a genomic variant.
        
        Args:
            genomic_hgvs: Genomic HGVS description
            primary_transcript: Primary transcript ID
            secondary_transcript: Optional secondary transcript ID
            genome_build: Genome build version
            
        Returns:
            Dict mapping transcript IDs to their annotation data
            
        Raises:
            VariantValidatorNormalizationError: If formatting fails
        """
        # Build transcript selection string
        select_transcripts = primary_transcript
        if secondary_transcript:
            select_transcripts = f"{primary_transcript}|{secondary_transcript}"
        
        try:
            formatter_response = self._repository.format_variant(
                genomic_hgvs=genomic_hgvs,
                select_transcripts=select_transcripts,
                genome_build=genome_build
            )
        except VariantValidatorNormalizationError as e:
            logger.error(f"Formatter error for {genomic_hgvs}: {e}")
            raise

        # Map the formatter response to structured data
        return self._mapping_service.map_formatter_response(
            formatter_response,
            primary_transcript=primary_transcript,
            secondary_transcript=secondary_transcript
        )

    def _split_and_resolve_transcript(self, hgvs: str) -> Tuple[str, str]:
        """
        Split HGVS into transcript and variant detail, resolving to versioned transcript.
        
        Args:
            hgvs: HGVS string in format "TRANSCRIPT:detail"
            
        Returns:
            Tuple of (resolved_transcript, variant_detail)
            
        Raises:
            ValueError: If HGVS format is invalid or transcript not found
        """
        parts = hgvs.split(":", 1)
        if len(parts) != 2:
            raise ValueError(f"Invalid HGVS format (expected TRANSCRIPT:detail): {hgvs}")
        
        transcript, detail = parts

        # Resolve transcript using repository
        transcript_versions = self._repository.resolve_transcripts(transcript.split(".")[0])
        available: List[str] = [t["reference"] for t in transcript_versions.get("transcripts", [])]
        
        if not available:
            raise ValueError(f"No transcripts found for prefix: {transcript}")

        # If transcript already has version, validate it exists
        if "." in transcript:
            if transcript not in available:
                raise ValueError(f"Transcript {transcript} not available")
            chosen = transcript
        else:
            # Find latest version
            versions = [v for v in available if v.startswith(f"{transcript}.")]
            if not versions:
                raise ValueError(f"No versioned transcripts for {transcript}")
            chosen = max(versions, key=self._extract_version_number)

        return chosen, detail

    @staticmethod
    def _extract_version_number(transcript_ref: str) -> int:
        """
        Extract version number from transcript reference.
        
        Args:
            transcript_ref: Reference like "NM_004992.4"
            
        Returns:
            Version number (e.g., 4) or -1 if parsing fails
        """
        try:
            return int(transcript_ref.split(".")[1])
        except Exception:
            return -1

    def create_gene_mutation_from_complex_variant(
        self,
        gene_assembly: GenomeAssembly,
        variant_description: str,
        target_assembly: str = "grch38",
        legacy_assembly: Optional[str] = "grch37"
    ) -> GeneMutation:
        """
        Create a GeneMutation object from a complex HGVS variant.
        
        Args:
            gene_assembly: GenomeAssembly containing build and refseq info
            variant_description: Complex HGVS variant description
            target_assembly: Primary genome assembly
            legacy_assembly: Optional legacy assembly for cross-reference
            
        Returns:
            GeneMutation object with genomic coordinates
            
        Raises:
            VariantValidatorNormalizationError: If normalization fails
        """
        # Step 1: Normalize the complex variant
        loci = self.normalize_complex_variant(
            assembly_build=gene_assembly.build,
            assembly_refseq=gene_assembly.refseq,
            hgvs_complex=variant_description
        )

        # Step 2: Build GenomicCoordinate objects using HgvsDescriptor
        genomic_coords: Dict[str, GenomicCoordinate] = {}
        
        # Primary assembly
        desc_primary = HgvsDescriptor(loci[target_assembly][0])
        genomic_coords[target_assembly] = GenomicCoordinate(
            assembly=target_assembly,
            hgvs=desc_primary.hgvs_string,
            start=desc_primary.start,
            end=desc_primary.end,
            size=desc_primary.size,
        )
        
        # Legacy assembly (if different and requested)
        if legacy_assembly and legacy_assembly != target_assembly:
            desc_legacy = HgvsDescriptor(loci[legacy_assembly][0])
            genomic_coords[legacy_assembly] = GenomicCoordinate(
                assembly=legacy_assembly,
                hgvs=desc_legacy.hgvs_string,
                start=desc_legacy.start,
                end=desc_legacy.end,
                size=desc_legacy.size,
            )

        return GeneMutation(
            genome_assembly=target_assembly,  # legacy field
            genomic_coordinate=genomic_coords[target_assembly].hgvs,
            genomic_coordinates=genomic_coords,
            variant_type=desc_primary.variant_type,
            primary_transcript=None,
            secondary_transcript=None,
        )

    def create_gene_mutation_from_transcript_variant(
        self,
        hgvs_string: str,
        gene_symbol: str,
        target_assembly: str = "grch38",
        legacy_assembly: Optional[str] = "grch37"
    ) -> GeneMutation:
        """
        Create a complete GeneMutation object from a transcript-level HGVS variant.
        
        Args:
            hgvs_string: HGVS variant description on transcript
            gene_symbol: Gene symbol for transcript lookup
            target_assembly: Primary genome assembly
            legacy_assembly: Optional legacy assembly for cross-reference
            
        Returns:
            GeneMutation object with genomic coordinates and transcript annotations
            
        Raises:
            ValueError: If gene symbol is unknown
            VariantValidatorNormalizationError: If normalization fails
        """
        # Step 1: Get gene information from registry
        gene = registry.get_gene(gene_symbol)
        if not gene:
            raise ValueError(f"Unknown gene symbol: {gene_symbol}")

        target_primary_transcript = gene.primary_transcript.mrna
        target_secondary_transcript = (
            gene.secondary_transcript.mrna if gene.secondary_transcript else None
        )

        # Step 2: Normalize to genomic coordinates on both assemblies
        loci = self.normalize_variant_to_assemblies(
            hgvs_string=hgvs_string,
            target_assembly=target_assembly,
            legacy_assembly=legacy_assembly
        )

        # Step 3: Get transcript and protein annotations
        annotations = self.get_transcript_and_protein_annotations(
            genomic_hgvs=loci[target_assembly][0],
            primary_transcript=target_primary_transcript,
            secondary_transcript=target_secondary_transcript
        )

        # Step 4: Build TranscriptMutation objects
        primary_tm = self._build_transcript_mutation(annotations[target_primary_transcript])
        secondary_tm = (
            self._build_transcript_mutation(annotations[target_secondary_transcript])
            if target_secondary_transcript else None
        )

        # Step 5: Build GenomicCoordinate objects using HgvsDescriptor
        genomic_coords: Dict[str, GenomicCoordinate] = {}
        
        # Primary assembly
        desc_primary = HgvsDescriptor(loci[target_assembly][0])
        genomic_coords[target_assembly] = GenomicCoordinate(
            assembly=target_assembly,
            hgvs=desc_primary.hgvs_string,
            start=desc_primary.start,
            end=desc_primary.end,
            size=desc_primary.size,
        )
        
        # Legacy assembly (if different and requested)
        if legacy_assembly and legacy_assembly != target_assembly:
            desc_legacy = HgvsDescriptor(loci[legacy_assembly][0])
            genomic_coords[legacy_assembly] = GenomicCoordinate(
                assembly=legacy_assembly,
                hgvs=desc_legacy.hgvs_string,
                start=desc_legacy.start,
                end=desc_legacy.end,
                size=desc_legacy.size,
            )

        # Step 6: Return the complete GeneMutation
        return GeneMutation(
            genomic_coordinate=genomic_coords[target_assembly].hgvs,
            genomic_coordinates=genomic_coords,
            genome_assembly=target_assembly,  # legacy field
            variant_type=desc_primary.variant_type,
            primary_transcript=primary_tm,
            secondary_transcript=secondary_tm,
        )

    def _build_transcript_mutation(self, annotation_data: Dict[str, Any]) -> TranscriptMutation:
        """
        Build a TranscriptMutation object from annotation data.
        
        Args:
            annotation_data: Mapped annotation data from formatter response
            
        Returns:
            TranscriptMutation object
        """
        return TranscriptMutation(
            gene_id=annotation_data["gene_id"],
            transcript_id=annotation_data["transcript_id"],
            hgvs_transcript_variant=annotation_data["hgvs_transcript_variant"],
            protein_consequence_tlr=annotation_data["predicted_protein_consequence_tlr"],
            protein_consequence_slr=annotation_data["predicted_protein_consequence_slr"],
        )
