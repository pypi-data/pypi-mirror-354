"""
Mutation Validator Service

This service provides a clean interface for validating RawMutation objects
and converting them into GeneMutation objects. It acts as a facade over
the variant validation system, providing a simpler API for the pipeline.
"""

import logging
from typing import Any, Dict, List, Optional
from rettxmutation.models.gene_models import RawMutation, GeneMutation
from rettxmutation.services.variant_validator_service import VariantValidatorService
from rettxmutation.repositories import VariantValidatorNormalizationError
from rettxmutation.config import RettxConfig, validate_config_fields

logger = logging.getLogger(__name__)


class MutationValidator:
    """
    Generic service for validating mutations. This provides a clean interface
    that can be easily swapped with other validation services in the future.
    
    This service validates its configuration on initialization and follows Azure
    best practices for error handling and resource management.    """
    
    def __init__(self, config: RettxConfig, variant_validator_service: Optional[VariantValidatorService] = None):
        """
        Initialize the mutation validator with configuration.
        
        Args:
            config: Configuration object implementing RettxConfig protocol
            variant_validator_service: Optional VariantValidatorService instance. If None, creates a new one.
            
        Raises:
            ValueError: If required configuration fields are missing or invalid
        """
        # Note: MutationValidator doesn't currently require external config,
        # but we validate the config parameter for consistency and future extensibility
        # If it needs external services in the future (e.g., variant databases), 
        # the config validation can be updated accordingly
        
        # For now, just store the config - no specific validation needed
        self._config = config
        
        # Initialize the variant validator service
        try:
            if variant_validator_service is None:
                from rettxmutation.repositories import VariantValidatorRepository
                repository = VariantValidatorRepository()
                self.variant_validator_service = VariantValidatorService(repository)
            else:
                self.variant_validator_service = variant_validator_service
            logger.debug("MutationValidator initialized with VariantValidatorService")
        except Exception as e:
            logger.error(f"Failed to initialize VariantValidatorService: {e}")
            raise ValueError(f"MutationValidator initialization failed: {e}") from e

    def close(self):
        """Clean up resources."""
        if self.variant_validator_service:
            self.variant_validator_service.close()

    async def validate_mutations(
        self, 
        raw_mutations: List[RawMutation]
    ) -> List[GeneMutation]:
        """
        Validate a list of RawMutation objects and convert them to GeneMutation objects.
        
        Args:
            raw_mutations: List of RawMutation objects from the extraction agent
            genome_assembly: Target genome assembly for validation
            
        Returns:
            List[GeneMutation]: List of validated GeneMutation objects
        """
        validated_mutations = []

        for raw_mutation in raw_mutations:
            try:
                logger.info(f"Validating mutation: {raw_mutation.mutation}")

                gene_mutation = self.variant_validator_service.create_gene_mutation_from_transcript_variant(
                    hgvs_string=raw_mutation.mutation,
                    gene_symbol="MECP2",
                    target_assembly="grch38",
                    legacy_assembly="grch37"
                )

                validated_mutations.append(gene_mutation)
                logger.info(f"Successfully validated mutation: {raw_mutation.mutation}")
            except VariantValidatorNormalizationError as e:
                logger.warning(f"Failed to validate mutation '{raw_mutation.mutation}': {e}")
                continue

            except Exception as e:
                logger.error(f"Unexpected error validating mutation '{raw_mutation.mutation}': {e}")
                continue

        logger.info(f"Validated {len(validated_mutations)} out of {len(raw_mutations)} mutations")
        return validated_mutations

    def validate_mutations(
        self,
        gene_mutation: GeneMutation,
        gene_symbol: str = "MECP2",
        target_assembly: str = "grch38",
        legacy_assembly: str = "grch37"
    ) -> Dict[str, Any]:
        """
        Validate a GeneMutation object by comparing it with a freshly validated version.
        
        This method takes a GeneMutation object, extracts the primary transcript HGVS,
        validates it through the VariantValidator service, and compares all properties
        between the input mutation and the validated mutation.
        
        Args:
            gene_mutation: The GeneMutation object to validate
            gene_symbol: Gene symbol for validation (default: "MECP2")
            target_assembly: Primary genome assembly (default: "grch38")
            legacy_assembly: Legacy assembly for cross-reference (default: "grch37")
            
        Returns:
            Dict containing:
                - is_valid: bool indicating if mutations match
                - input_mutation: original GeneMutation
                - validated_mutation: validated GeneMutation from service
                - differences: dict of differing fields
                - error: error message if validation failed
        """
        logger.info(f"Validating GeneMutation using primary transcript for gene: {gene_symbol}")
        
        result = {
            "is_valid": False,
            "input_mutation": gene_mutation,
            "validated_mutation": None,
            "differences": {},
            "error": None
        }
        
        try:
            # Extract primary transcript HGVS from the input mutation
            if not gene_mutation.primary_transcript:
                result["error"] = "Missing primary transcript information"
                logger.error("Cannot validate mutation: missing primary transcript")
                return result
            
            primary_hgvs = gene_mutation.primary_transcript.hgvs_transcript_variant
            if not primary_hgvs:
                result["error"] = "Missing HGVS transcript variant in primary transcript"
                logger.error("Cannot validate mutation: missing HGVS transcript variant")
                return result
            
            logger.info(f"Using primary transcript HGVS: {primary_hgvs}")
            
            # Validate using VariantValidatorService
            validated_gene_mutation = self.variant_validator_service.create_gene_mutation_from_transcript_variant(
                hgvs_string=primary_hgvs,
                gene_symbol=gene_symbol,
                target_assembly=target_assembly,
                legacy_assembly=legacy_assembly
            )
            
            result["validated_mutation"] = validated_gene_mutation
            logger.info(f"Successfully obtained validated mutation")
            
            # Compare the two GeneMutation objects
            differences = self._compare_gene_mutations(gene_mutation, validated_gene_mutation)
            result["differences"] = differences
            result["is_valid"] = len(differences) == 0
            
            if result["is_valid"]:
                logger.info("Mutation validation successful - objects match")
            else:
                logger.warning(f"Mutation validation completed with {len(differences)} differences")
                for field, diff in differences.items():
                    logger.debug(f"Difference in {field}: {diff}")
            
            return result
            
        except VariantValidatorNormalizationError as e:
            result["error"] = f"Variant validation failed: {e}"
            logger.error(f"Variant validation failed for {primary_hgvs}: {e}")
            return result
            
        except Exception as e:
            result["error"] = f"Unexpected error during validation: {e}"
            logger.error(f"Unexpected error validating mutation: {e}")
            return result

    def _compare_gene_mutations(self, mutation1: GeneMutation, mutation2: GeneMutation) -> Dict[str, Any]:
        """
        Compare two GeneMutation objects and return differences.
        
        Args:
            mutation1: First GeneMutation object
            mutation2: Second GeneMutation object
            
        Returns:
            Dict containing field names as keys and difference details as values
        """
        differences = {}
        
        # Get dictionaries for comparison (excluding None values)
        dict1 = mutation1.model_dump(exclude_none=True)
        dict2 = mutation2.model_dump(exclude_none=True)
        
        # Compare all fields
        all_fields = set(dict1.keys()) | set(dict2.keys())
        
        for field in all_fields:
            value1 = dict1.get(field)
            value2 = dict2.get(field)
            
            if value1 != value2:
                differences[field] = {
                    "input_value": value1,
                    "validated_value": value2
                }
        
        return differences
