"""
Hardcoded YAML configurations for Azure Function deployment.
This file contains all the YAML configurations that would normally be loaded from files.
"""

# Validation YAML configurations
VALIDATION_YAML_CONFIGS = {
    "validate_document.yaml": {
        "name": "validate_document",
        "description": "Validate if document is a valid MECP2 mutation report",
        "input": {
            "document_text": "The document text to validate",
            "regex_context": "Context from regex-based validation",
            "language": "The document language"
        },
        "execution_settings": {
            "default": {
                "temperature": 0.1,
                "max_tokens": 50
            }
        }
    }
}

# Extraction YAML configurations
EXTRACTION_YAML_CONFIGS = {
    "extract_mutations.yaml": {
        "name": "extract_mutations",
        "description": "Extract MECP2 mutations from genetic reports",
        "input": {
            "document_text": "The cleaned document text",
            "mecp2_keywords": "Detected MECP2-related keywords",
            "variant_list": "Detected variant patterns"
        },
        "execution_settings": {
            "default": {
                "temperature": 0.1,
                "max_tokens": 500
            }
        }
    }
}

# Summarization YAML configurations
SUMMARIZATION_YAML_CONFIGS = {
    "summarize_report.yaml": {
        "name": "summarize_report",
        "description": "Summarize genetic clinical reports focusing on MECP2",
        "input": {
            "document_text": "The cleaned document text",
            "keywords": "Keywords to guide the summary"
        },
        "execution_settings": {
            "default": {
                "temperature": 0.1,
                "max_tokens": 1000
            }
        }
    },
    
    "correct_summary_mistakes.yaml": {
        "name": "correct_summary_mistakes",
        "description": "Correct mistakes in genetic report summaries",
        "input": {
            "document_text": "The summary text to correct",
            "keywords": "Keywords that guided the original summary",
            "text_analytics": "Results from text analytics",
            "latest_transcripts": "Latest transcript version information"
        },
        "execution_settings": {
            "default": {
                "temperature": 0.1,
                "max_tokens": 1000
            }
        }
    }
}

# Shared data
SHARED_DATA = {
    "latest_transcripts.json": {
        "ENST00000303391": "11",
        "ENST00000369957": "5",
        "ENST00000407218": "5",
        "ENST00000415944": "4",
        "ENST00000453960": "7",
        "ENST00000486506": "5",
        "ENST00000628176": "2",
        "ENST00000630151": "3",
        "ENST00000637917": "2",
        "ENST00000674996": "2",
        "ENST00000675526": "2",
        "ENST00000713611": "1",
        "NM_001110792": "2",
        "NM_001316337": "2",
        "NM_001369391": "2",
        "NM_001369392": "2",
        "NM_001369393": "2",
        "NM_001369394": "2",
        "NM_001386137": "1",
        "NM_001386138": "1",
        "NM_001386139": "1",
        "NM_004992": "5",
        "XM_006719272": "4",
        "XM_006719273": "3",
        "XM_006719274": "3",
        "XM_006719275": "4",
        "XM_011529844": "4",
        "XM_017011493": "3",
        "XM_017011494": "3",
        "XM_017011495": "3",
        "XM_017011496": "3",
        "XM_024447709": "2",
        "XM_024447710": "2",
        "XM_024447711": "2",
        "XM_024447712": "2",
        "XM_024447713": "2"
    }
}

def get_yaml_config(config_path: str) -> dict:
    """
    Get hardcoded YAML configuration by path.
    
    Args:
        config_path: Path to the YAML config (e.g., "validation/validate_document.yaml")
        
    Returns:
        Dictionary containing the YAML configuration
        
    Raises:
        FileNotFoundError: If the config path is not found in hardcoded configs
    """
    # Extract filename from path
    filename = config_path.split('/')[-1] if '/' in config_path else config_path
    
    # Check validation configs
    if filename in VALIDATION_YAML_CONFIGS:
        return VALIDATION_YAML_CONFIGS[filename]
    
    # Check extraction configs
    if filename in EXTRACTION_YAML_CONFIGS:
        return EXTRACTION_YAML_CONFIGS[filename]
    
    # Check summarization configs
    if filename in SUMMARIZATION_YAML_CONFIGS:
        return SUMMARIZATION_YAML_CONFIGS[filename]
    
    # Check shared data
    if filename in SHARED_DATA:
        return SHARED_DATA[filename]
    
    # If not found, raise error
    raise FileNotFoundError(f"YAML config not found: {config_path}")
