"""
Tests for VariantValidatorService

This module tests the variant validation service with mocked API responses
from VariantValidator, including intergenic and gene-based variants.
"""

import pytest
from unittest.mock import Mock, patch
from rettxmutation.services.variant_validator_service import VariantValidatorService
from rettxmutation.repositories.variant_validator_repository import VariantValidatorRepository
from rettxmutation.models.gene_assembly import GenomeAssembly


class TestVariantValidatorServiceMocked:
    """Test VariantValidatorService with mocked API responses."""

    @pytest.fixture
    def mock_repository(self):
        """Create a mock repository."""
        return Mock(spec=VariantValidatorRepository)

    @pytest.fixture
    def variant_service(self, mock_repository):
        """Create VariantValidatorService with mock repository."""
        return VariantValidatorService(mock_repository)

    @pytest.fixture
    def intergenic_variant_response(self):
        """Mock response for intergenic variant (like the actual API response we received)."""
        return {
            "flag": "intergenic",
            "intergenic_variant_1": {
                "alt_genomic_loci": [
                    {
                        "grch37": {
                            "hgvs_genomic_description": "NW_003871103.3:g.1465305G>A",
                            "vcf": {
                                "alt": "A",
                                "chr": "HG1497_PATCH",
                                "pos": "1465305",
                                "ref": "G"
                            }
                        }
                    },
                    {
                        "hg19": {
                            "hgvs_genomic_description": "NW_003871103.3:g.1465305G>A",
                            "vcf": {
                                "alt": "A",
                                "chr": "NW_003871103.3",
                                "pos": "1465305",
                                "ref": "G"
                            }
                        }
                    }
                ],
                "annotations": {},
                "gene_ids": {},
                "gene_symbol": "",
                "genome_context_intronic_sequence": "",
                "hgvs_lrg_transcript_variant": "",
                "hgvs_lrg_variant": "",
                "hgvs_predicted_protein_consequence": {
                    "lrg_slr": "",
                    "lrg_tlr": "",
                    "slr": "",
                    "tlr": ""
                },
                "hgvs_refseqgene_variant": "",
                "hgvs_transcript_variant": "",
                "lovd_corrections": None,
                "lovd_messages": None,
                "primary_assembly_loci": {
                    "grch38": {
                        "hgvs_genomic_description": "NC_000023.11:g.154031326G>A",
                        "vcf": {
                            "alt": "A",
                            "chr": "X",
                            "pos": "154031326",
                            "ref": "G"
                        }
                    },
                    "hg38": {
                        "hgvs_genomic_description": "NC_000023.11:g.154031326G>A",
                        "vcf": {
                            "alt": "A",
                            "chr": "chrX",
                            "pos": "154031326",
                            "ref": "G"
                        }
                    }
                },
                "reference_sequence_records": "",
                "refseqgene_context_intronic_sequence": "",
                "rna_variant_descriptions": None,
                "selected_assembly": "GRCh38",
                "submitted_variant": "NC_000023.11:g.154031326G>A",
                "transcript_description": "",
                "validation_warnings": [
                    "None of the specified transcripts ([\"NC_000023.11\"]) fully overlap the described variation in the genomic sequence. Try selecting one of the default options"
                ],
                "variant_exonic_positions": None
            },
            "metadata": {
                "variantvalidator_hgvs_version": "2.2.1.dev7+g59392c5",
                "variantvalidator_version": "3.0.2.dev102+g3ba73a1",
                "vvdb_version": "vvdb_2025_3",
                "vvseqrepo_db": "VV_SR_2025_02/master",
                "vvta_version": "vvta_2025_02"
            }
        }

    @pytest.fixture
    def gene_variant_response(self):
        """Mock response for gene-based variant."""
        return {
            "flag": "gene",
            "NM_004992.4": {
                "alt_genomic_loci": [
                    {
                        "grch37": {
                            "hgvs_genomic_description": "NC_000023.10:g.153296777C>T",
                            "vcf": {
                                "alt": "T",
                                "chr": "X",
                                "pos": "153296777",
                                "ref": "C"
                            }
                        }
                    }
                ],
                "annotations": {
                    "chromosome": "X",
                    "db_xref": {
                        "CCDS": "CCDS14606.1",
                        "ensemblgene": "ENSG00000169057",
                        "hgnc": "HGNC:6990",
                        "ncbigene": "4204",
                        "select": "MANE"
                    },
                    "ensembl_select_transcript": "ENST00000303391.12",
                    "mane_plus_clinical": "NM_004992.4",
                    "mane_select": "NM_004992.4",
                    "map": "Xq28",
                    "note": "methyl CpG binding protein 2",
                    "refseq_select": "NM_004992.4",
                    "strand": "-1"
                },
                "gene_ids": {
                    "ccds_ids": ["CCDS14606"],
                    "ensembl_gene_id": "ENSG00000169057",
                    "entrez_gene_id": "4204",
                    "hgnc_id": "HGNC:6990",
                    "omim_id": ["300005"],
                    "orphanet": ["77"],
                    "ucsc_id": "uc004frn.4"
                },
                "gene_symbol": "MECP2",
                "genome_context_intronic_sequence": "",
                "hgvs_lrg_transcript_variant": "",
                "hgvs_lrg_variant": "",
                "hgvs_predicted_protein_consequence": {
                    "lrg_slr": "",
                    "lrg_tlr": "",
                    "slr": "NP_004983.1:p.(Arg168Ter)",
                    "tlr": "NP_004983.1:p.(Arg168*)"
                },
                "hgvs_refseqgene_variant": "",
                "hgvs_transcript_variant": "NM_004992.4:c.502C>T",
                "lovd_corrections": None,
                "lovd_messages": None,
                "primary_assembly_loci": {
                    "grch38": {
                        "hgvs_genomic_description": "NC_000023.11:g.154031326C>T",
                        "vcf": {
                            "alt": "T",
                            "chr": "X",
                            "pos": "154031326",
                            "ref": "C"
                        }
                    },
                    "hg38": {
                        "hgvs_genomic_description": "NC_000023.11:g.154031326C>T",
                        "vcf": {
                            "alt": "T",
                            "chr": "chrX",
                            "pos": "154031326",
                            "ref": "C"
                        }
                    }
                },
                "reference_sequence_records": "",
                "refseqgene_context_intronic_sequence": "",
                "rna_variant_descriptions": None,
                "selected_assembly": "GRCh38",
                "submitted_variant": "NM_004992.4:c.502C>T",
                "transcript_description": "Homo sapiens methyl CpG binding protein 2 (MECP2), transcript variant 1, mRNA",
                "validation_warnings": [],
                "variant_exonic_positions": {
                    "NC_000023.11": {
                        "end_exon": "4",
                        "start_exon": "4"
                    }
                }
            },
            "metadata": {
                "variantvalidator_hgvs_version": "2.2.1.dev7+g59392c5",
                "variantvalidator_version": "3.0.2.dev102+g3ba73a1",
                "vvdb_version": "vvdb_2025_3",
                "vvseqrepo_db": "VV_SR_2025_02/master",
                "vvta_version": "vvta_2025_02"
            }
        }

    def test_normalize_complex_variant_intergenic(self, variant_service, mock_repository, intergenic_variant_response):
        """Test normalization of intergenic complex variant."""
        # Setup mock
        mock_repository.normalize_variant.return_value = intergenic_variant_response
        
        # Test
        result = variant_service.normalize_complex_variant(
            assembly_build="GRCh38",
            assembly_refseq="NC_000023.11",
            hgvs_complex="NC_000023.11:g.154031326G>A"
        )
        
        # Verify the result structure
        assert "grch38" in result
        assert "grch37" in result
        assert result["grch38"][0] == "NC_000023.11:g.154031326G>A"  # Returns tuple (hgvs, pos)
        assert result["grch37"][0] == "NW_003871103.3:g.1465305G>A"
          # Verify repository was called correctly
        mock_repository.normalize_variant.assert_called_once_with(
            genome_build="GRCh38",
            variant_description="NC_000023.11:g.154031326G>A",
            select_transcripts="NC_000023.11"
        )
        
    def test_normalize_complex_variant_gene_based(self, variant_service, mock_repository, gene_variant_response):
        """Test normalization of gene-based complex variant."""
        # Setup mock
        mock_repository.normalize_variant.return_value = gene_variant_response
        
        # Test
        result = variant_service.normalize_complex_variant(
            assembly_build="GRCh38",
            assembly_refseq="NC_000023.11",
            hgvs_complex="NM_004992.4:c.502C>T"
        )
        
        # Verify the result structure
        assert "grch38" in result
        assert "grch37" in result
        assert result["grch38"][0] == "NC_000023.11:g.154031326C>T"  # Returns tuple (hgvs, pos)
        assert result["grch37"][0] == "NC_000023.10:g.153296777C>T"

    def test_create_gene_mutation_from_complex_variant_intergenic(
        self, variant_service, mock_repository, intergenic_variant_response
    ):
        """Test creating GeneMutation from intergenic complex variant."""
        # Setup mock
        mock_repository.normalize_variant.return_value = intergenic_variant_response
        
        # Create test gene assembly
        gene_assembly = GenomeAssembly(
            build="GRCh38",
            chromosome="chrX",
            refseq="NC_000023.11"
        )
        
        # Test
        result = variant_service.create_gene_mutation_from_complex_variant(
            gene_assembly=gene_assembly,
            variant_description="NC_000023.11:g.154031326G>A",
            target_assembly="grch38",
            legacy_assembly="grch37"
        )
        
        # Verify the result
        assert result is not None
        assert result.genomic_coordinates is not None
        assert "GRCh38" in result.genomic_coordinates
        assert result.genomic_coordinates["GRCh38"].hgvs == "NC_000023.11:g.154031326G>A"
        
        # Check if legacy assembly data is also available
        if "GRCh37" in result.genomic_coordinates:
            assert result.genomic_coordinates["GRCh37"].hgvs == "NW_003871103.3:g.1465305G>A"

    def test_create_gene_mutation_from_complex_variant_gene_based(
        self, variant_service, mock_repository, gene_variant_response
    ):
        """Test creating GeneMutation from gene-based complex variant."""
        # Setup mock
        mock_repository.normalize_variant.return_value = gene_variant_response
        
        # Create test gene assembly
        gene_assembly = GenomeAssembly(
            build="GRCh38",
            chromosome="chrX",
            refseq="NC_000023.11"
        )
        
        # Test
        result = variant_service.create_gene_mutation_from_complex_variant(
            gene_assembly=gene_assembly,
            variant_description="NM_004992.4:c.502C>T",
            target_assembly="grch38",
            legacy_assembly="grch37"
        )
          # Verify the result
        assert result is not None
        assert result.genomic_coordinates is not None
        assert "GRCh38" in result.genomic_coordinates
        
        # Check the GRCh38 genomic coordinate
        grch38_coord = result.genomic_coordinates["GRCh38"]
        assert grch38_coord is not None
        assert grch38_coord.hgvs == "NC_000023.11:g.154031326C>T"
        assert grch38_coord.assembly == "GRCh38"
          # Check primary transcript if available
        if result.primary_transcript:
            assert result.primary_transcript.hgvs_transcript_variant == "NM_004992.4:c.502C>T"


if __name__ == "__main__":
    pytest.main([__file__])
