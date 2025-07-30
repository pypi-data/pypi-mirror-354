"""
Comprehensive tests for the validate_mutations method in MutationValidator.
"""

import pytest
from unittest.mock import Mock
from rettxmutation.models.gene_models import GeneMutation, TranscriptMutation, GenomicCoordinate
from rettxmutation.services.mutation_validator import MutationValidator
from rettxmutation.repositories import VariantValidatorNormalizationError
from rettxmutation.config import RettxConfig


class TestValidateMutations:
    """Test cases for the validate_mutations method."""
    
    @pytest.fixture
    def sample_input_mutation(self):
        """Create a sample input GeneMutation for testing."""
        return GeneMutation(
            variant_type="SNV",
            primary_transcript=TranscriptMutation(
                gene_id="MECP2",
                transcript_id="NM_004992.4",
                hgvs_transcript_variant="NM_004992.4:c.916C>T",
                protein_consequence_tlr="NP_004983.1:p.(Arg306Cys)",
                protein_consequence_slr="NP_004983.1:p.(R306C)"
            ),
            genomic_coordinates={
                "GRCh38": GenomicCoordinate(
                    assembly="GRCh38",
                    hgvs="NC_000023.11:g.154030912G>A",
                    start=154030912,
                    end=154030912,
                    size=1
                )
            }
        )
    
    @pytest.fixture
    def exact_match_validated_mutation(self):
        """Create a validated mutation that exactly matches the input."""
        return GeneMutation(
            variant_type="SNV",
            primary_transcript=TranscriptMutation(
                gene_id="MECP2",
                transcript_id="NM_004992.4",
                hgvs_transcript_variant="NM_004992.4:c.916C>T",
                protein_consequence_tlr="NP_004983.1:p.(Arg306Cys)",
                protein_consequence_slr="NP_004983.1:p.(R306C)"
            ),
            genomic_coordinates={
                "GRCh38": GenomicCoordinate(
                    assembly="GRCh38",
                    hgvs="NC_000023.11:g.154030912G>A",
                    start=154030912,
                    end=154030912,
                    size=1
                )
            }
        )
    
    @pytest.fixture
    def different_validated_mutation(self):
        """Create a validated mutation with differences from input."""
        return GeneMutation(
            variant_type="SNV",
            primary_transcript=TranscriptMutation(
                gene_id="MECP2",
                transcript_id="NM_004992.4",
                hgvs_transcript_variant="NM_004992.4:c.916C>T",
                protein_consequence_tlr="NP_004983.1:p.(Arg306Cys)",
                protein_consequence_slr="NP_004983.1:p.(R306C)"
            ),
            secondary_transcript=TranscriptMutation(
                gene_id="MECP2",
                transcript_id="NM_001110792.2",
                hgvs_transcript_variant="NM_001110792.2:c.952C>T",
                protein_consequence_tlr="NP_001104262.1:p.(Arg318Cys)",
                protein_consequence_slr="NP_001104262.1:p.(R318C)"
            ),
            genomic_coordinates={
                "GRCh38": GenomicCoordinate(
                    assembly="GRCh38",
                    hgvs="NC_000023.11:g.154030912G>A",
                    start=154030912,
                    end=154030912,
                    size=1
                ),
                "GRCh37": GenomicCoordinate(
                    assembly="GRCh37",
                    hgvs="NC_000023.10:g.153296363G>A",
                    start=153296363,
                    end=153296363,
                    size=1
                )
            }
        )
    
    @pytest.fixture
    def mock_validator_service(self):
        """Create a mock VariantValidatorService."""
        mock_service = Mock()
        mock_service.close = Mock()
        mock_service.create_gene_mutation_from_transcript_variant = Mock()
        return mock_service
    
    @pytest.fixture
    def mutation_validator(self, mock_validator_service):
        """Create a MutationValidator with mocked dependencies."""
        config = Mock(spec=RettxConfig)
        validator = MutationValidator(config, mock_validator_service)
        return validator
    
    def test_validate_mutations_exact_match(
        self, 
        mutation_validator, 
        sample_input_mutation, 
        exact_match_validated_mutation
    ):
        """Test validation when input and validated mutations match exactly."""
        # Setup mock to return exact match
        mutation_validator.variant_validator_service.create_gene_mutation_from_transcript_variant.return_value = exact_match_validated_mutation
        
        # Run validation
        result = mutation_validator.validate_mutations(sample_input_mutation)
        
        # Assertions for exact match
        assert result["is_valid"] is True
        assert result["error"] is None
        assert result["input_mutation"] == sample_input_mutation
        assert result["validated_mutation"] == exact_match_validated_mutation
        assert result["differences"] == {}
        
        # Verify the service was called correctly
        mutation_validator.variant_validator_service.create_gene_mutation_from_transcript_variant.assert_called_once_with(
            hgvs_string="NM_004992.4:c.916C>T",
            gene_symbol="MECP2",
            target_assembly="grch38",
            legacy_assembly="grch37"
        )
    
    def test_validate_mutations_with_differences(
        self, 
        mutation_validator, 
        sample_input_mutation, 
        different_validated_mutation
    ):
        """Test validation when input and validated mutations have differences."""
        # Setup mock to return different mutation
        mutation_validator.variant_validator_service.create_gene_mutation_from_transcript_variant.return_value = different_validated_mutation
        
        # Run validation
        result = mutation_validator.validate_mutations(sample_input_mutation)
        
        # Assertions for differences
        assert result["is_valid"] is False
        assert result["error"] is None
        assert result["input_mutation"] == sample_input_mutation
        assert result["validated_mutation"] == different_validated_mutation
        assert len(result["differences"]) > 0
        
        # Check specific differences
        differences = result["differences"]
        
        # Should have difference in secondary_transcript (None vs present)
        assert "secondary_transcript" in differences
        assert differences["secondary_transcript"]["input_value"] is None
        assert differences["secondary_transcript"]["validated_value"] is not None
        
        # Should have difference in genomic_coordinates (missing GRCh37)
        assert "genomic_coordinates" in differences
        input_coords = differences["genomic_coordinates"]["input_value"]
        validated_coords = differences["genomic_coordinates"]["validated_value"]
        assert "GRCh37" not in input_coords
        assert "GRCh37" in validated_coords
    
    def test_validate_mutations_missing_primary_transcript(self, mutation_validator):
        """Test validation failure when primary transcript is missing."""
        mutation_without_primary = GeneMutation(
            variant_type="SNV",
            genomic_coordinates={
                "GRCh38": GenomicCoordinate(
                    assembly="GRCh38",
                    hgvs="NC_000023.11:g.154030912G>A",
                    start=154030912,
                    end=154030912,
                    size=1
                )
            }
        )
        
        result = mutation_validator.validate_mutations(mutation_without_primary)
        
        assert result["is_valid"] is False
        assert result["error"] == "Missing primary transcript information"
        assert result["validated_mutation"] is None
        assert result["differences"] == {}
    
    def test_validate_mutations_missing_hgvs(self, mutation_validator):
        """Test validation failure when HGVS is missing from primary transcript."""
        mutation_without_hgvs = GeneMutation(
            variant_type="SNV",
            primary_transcript=TranscriptMutation(
                gene_id="MECP2",
                transcript_id="NM_004992.4",
                hgvs_transcript_variant="",  # Empty HGVS
                protein_consequence_tlr="NP_004983.1:p.(Arg306Cys)"
            ),
            genomic_coordinates={
                "GRCh38": GenomicCoordinate(
                    assembly="GRCh38",
                    hgvs="NC_000023.11:g.154030912G>A",
                    start=154030912,
                    end=154030912,
                    size=1
                )
            }
        )
        
        result = mutation_validator.validate_mutations(mutation_without_hgvs)
        
        assert result["is_valid"] is False
        assert result["error"] == "Missing HGVS transcript variant in primary transcript"
        assert result["validated_mutation"] is None
        assert result["differences"] == {}
    
    def test_validate_mutations_variant_validator_error(
        self, 
        mutation_validator, 
        sample_input_mutation
    ):
        """Test handling of VariantValidatorNormalizationError."""
        # Setup mock to raise VariantValidatorNormalizationError
        mutation_validator.variant_validator_service.create_gene_mutation_from_transcript_variant.side_effect = VariantValidatorNormalizationError("Invalid HGVS format")
        
        result = mutation_validator.validate_mutations(sample_input_mutation)
        
        assert result["is_valid"] is False
        assert "Variant validation failed" in result["error"]
        assert "Invalid HGVS format" in result["error"]
        assert result["validated_mutation"] is None
        assert result["differences"] == {}
    
    def test_validate_mutations_unexpected_error(
        self, 
        mutation_validator, 
        sample_input_mutation
    ):
        """Test handling of unexpected errors."""
        # Setup mock to raise unexpected error
        mutation_validator.variant_validator_service.create_gene_mutation_from_transcript_variant.side_effect = Exception("Unexpected error")
        
        result = mutation_validator.validate_mutations(sample_input_mutation)
        
        assert result["is_valid"] is False
        assert "Unexpected error during validation" in result["error"]
        assert "Unexpected error" in result["error"]
        assert result["validated_mutation"] is None
        assert result["differences"] == {}
    
    def test_validate_mutations_custom_parameters(
        self, 
        mutation_validator, 
        sample_input_mutation, 
        exact_match_validated_mutation
    ):
        """Test validation with custom gene symbol and assembly parameters."""
        # Setup mock
        mutation_validator.variant_validator_service.create_gene_mutation_from_transcript_variant.return_value = exact_match_validated_mutation
        
        # Run validation with custom parameters
        result = mutation_validator.validate_mutations(
            sample_input_mutation,
            gene_symbol="CDKL5",
            target_assembly="grch37",
            legacy_assembly="grch38"
        )
        
        # Verify custom parameters were passed
        mutation_validator.variant_validator_service.create_gene_mutation_from_transcript_variant.assert_called_once_with(
            hgvs_string="NM_004992.4:c.916C>T",
            gene_symbol="CDKL5",
            target_assembly="grch37",
            legacy_assembly="grch38"
        )
        
        assert result["is_valid"] is True
    
    def test_compare_gene_mutations_exact_match(self, mutation_validator, sample_input_mutation):
        """Test _compare_gene_mutations method with exact match."""
        differences = mutation_validator._compare_gene_mutations(
            sample_input_mutation, 
            sample_input_mutation
        )
        
        assert differences == {}
    
    def test_compare_gene_mutations_with_differences(
        self, 
        mutation_validator, 
        sample_input_mutation, 
        different_validated_mutation
    ):
        """Test _compare_gene_mutations method with differences."""
        differences = mutation_validator._compare_gene_mutations(
            sample_input_mutation, 
            different_validated_mutation
        )
        
        assert len(differences) > 0
        assert "secondary_transcript" in differences
        assert "genomic_coordinates" in differences
        
        # Check structure of differences
        for field, diff in differences.items():
            assert "input_value" in diff
            assert "validated_value" in diff
    
    def test_compare_gene_mutations_variant_type_difference(self, mutation_validator):
        """Test _compare_gene_mutations with different variant types."""
        mutation1 = GeneMutation(
            variant_type="SNV",
            primary_transcript=TranscriptMutation(
                hgvs_transcript_variant="NM_004992.4:c.916C>T"
            ),
            genomic_coordinates={
                "GRCh38": GenomicCoordinate(
                    assembly="GRCh38",
                    hgvs="NC_000023.11:g.154030912G>A",
                    start=154030912,
                    end=154030912,
                    size=1
                )
            }
        )
        
        mutation2 = GeneMutation(
            variant_type="deletion",
            primary_transcript=TranscriptMutation(
                hgvs_transcript_variant="NM_004992.4:c.916C>T"
            ),
            genomic_coordinates={
                "GRCh38": GenomicCoordinate(
                    assembly="GRCh38",
                    hgvs="NC_000023.11:g.154030912G>A",
                    start=154030912,
                    end=154030912,
                    size=1
                )
            }
        )
        
        differences = mutation_validator._compare_gene_mutations(mutation1, mutation2)
        
        assert "variant_type" in differences
        assert differences["variant_type"]["input_value"] == "SNV"
        assert differences["variant_type"]["validated_value"] == "deletion"


class TestValidateMutationsIntegration:
    """Integration tests that demonstrate real-world usage patterns."""
    
    def test_quality_assurance_workflow(self):
        """Test using validate_mutations for quality assurance."""
        # This would be a more realistic test with actual data
        # For now, we'll mock it to show the pattern
        
        input_mutation = GeneMutation(
            variant_type="SNV",
            primary_transcript=TranscriptMutation(
                gene_id="MECP2",
                hgvs_transcript_variant="NM_004992.4:c.916C>T"
            ),
            genomic_coordinates={
                "GRCh38": GenomicCoordinate(
                    assembly="GRCh38",
                    hgvs="NC_000023.11:g.154030912G>A",
                    start=154030912,
                    end=154030912,
                    size=1
                )
            }
        )
        
        # Mock the validator
        mock_service = Mock()
        mock_service.close = Mock()
        
        # Create a more complete validated mutation
        validated_mutation = GeneMutation(
            variant_type="SNV",
            primary_transcript=TranscriptMutation(
                gene_id="MECP2",
                transcript_id="NM_004992.4",
                hgvs_transcript_variant="NM_004992.4:c.916C>T",
                protein_consequence_tlr="NP_004983.1:p.(Arg306Cys)",
                protein_consequence_slr="NP_004983.1:p.(R306C)"
            ),
            secondary_transcript=TranscriptMutation(
                gene_id="MECP2",
                transcript_id="NM_001110792.2",
                hgvs_transcript_variant="NM_001110792.2:c.952C>T",
                protein_consequence_tlr="NP_001104262.1:p.(Arg318Cys)",
                protein_consequence_slr="NP_001104262.1:p.(R318C)"
            ),
            genomic_coordinates={
                "GRCh38": GenomicCoordinate(
                    assembly="GRCh38",
                    hgvs="NC_000023.11:g.154030912G>A",
                    start=154030912,
                    end=154030912,
                    size=1
                )
            }
        )
        
        mock_service.create_gene_mutation_from_transcript_variant.return_value = validated_mutation
        
        validator = MutationValidator(Mock(spec=RettxConfig), mock_service)
        
        result = validator.validate_mutations(input_mutation)
        
        # Quality assurance checks
        assert result["is_valid"] is False  # Should have differences
        assert result["validated_mutation"] is not None
        assert len(result["differences"]) > 0
        
        # Check that we got enriched data
        differences = result["differences"]
        assert "secondary_transcript" in differences
        
        # The validated mutation should have more complete information
        assert result["validated_mutation"].secondary_transcript is not None
        assert result["input_mutation"].secondary_transcript is None


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])
