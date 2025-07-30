"""
Hardcoded prompts for Azure Function deployment workaround.
This module contains all prompt templates that were previously loaded from .skprompt.txt files.
"""

# Validation prompt template
VALIDATION_PROMPT = """You are an expert in genetics. Evaluate the following text to decide if it is a valid mutation report describing explicit MECP2 cDNA mutations. Consider the following context: {{$regex_context}} Take into account the language of the document, which is {{$language}}. Output a single line exactly in the following format: 'True, confidence=X' if it is valid, or 'False, confidence=X' if it is not, where X is a float between 0 and 1 representing your confidence.

Text to evaluate:
{{$document_text}}
"""

# Mutation extraction prompt template
EXTRACTION_PROMPT = """You are an expert in genetics. You must only extract MECP2 cDNA mutations explicitly mentioned in the provided text.
These mutations are typically in a format like c.916C>T, c.1035A>G or c.1140_1160del.
If you find more than one mutation, list each on a new line in the format:
transcript:gene_variation;confidence=score

Examples:
1) NM_004992.4:c.916C>T;confidence=1.0
2) NM_001110792.1:c.538C>T;confidence=0.8
3) NM_004992.4:c.1035A>G;confidence=0.6
4) NM_004992.4:c.1152_1195del;confidence=1.0
5) NM_004992.4:c.378-2A>G;confidence=0.9
6) NM_001110792.2:c.414-2A>G;confidence=0.7

If the text only describes a deletion of exons (or no explicit cDNA nomenclature), then output 'No mutation found'.

Priority MUST be given to the following mutations:
{{$variant_list}}.

Guidelines:
1) Do NOT fabricate or infer cDNA variants from exon-level deletions. If cDNA notation is not present, respond with 'No mutation found'.
2) Use only the transcripts provided in the keywords. If no transcript is provided, default to NM_004992.4.
3) Confidence score must be between 0 and 1.
4) Provide no extra commentary beyond the specified format.

Input text:
{{$document_text}}

Identify any cDNA mutations (e.g., c.XXXXC>T, c.XXXX_XXXXdel) related to MECP2 in the text using only the transcripts found in the keywords. If no valid cDNA mutation is present, return 'No mutation found'.
"""

# Summarization prompt template
SUMMARIZATION_PROMPT = """You are an expert at summarizing genetic clinical reports.
Output a concise summary focusing on any mention of the MECP2 gene, transcripts (e.g., NM_004992, NM_001110792), and variants (e.g., c.538C>T).
Ignore unrelated text.
You will be provided with a list of keywords to guide your summary. PRIORITY MUST BE GIVEN TO THE KEYWORDS PROVIDED.

Text to Summarize:
{{$document_text}}

Keywords:
{{$keywords}}

Focus on:
- Mentions of MECP2 gene
- Mentions of transcripts (NM_...)
- Mentions of variants (c.XXX...>XXX...)
- Key statements that connect them

Return 1-3 paragraphs, no more than 300 words total.
"""

# Correction prompt template
CORRECTION_PROMPT = """You are an expert in finding and correcting mistakes in genetic clinical reports. Your goal is to correct any errors in the provided summary, not to rewrite it. You will be provided with a summary of a genetic report, a list of keywords to guide the summary, and the results of text analytics. Look for any mistakes in the summary and correct them. You can use the keywords and text analytics results to guide your corrections. If you detect a mutation incorrectly spelled, correct it (e.g., c538CT -> c.538C>T, c.808C->T -> c.808C>T). Some mistakes are related with OCR errors (e.g., c.8080>T -> c.808C>T, mutations need to have nucleotide changes or deletions). For transcripts, use the provided list of transcripts to validate the format: {{$latest_transcripts}}.

Summary:
{{$document_text}}

Keywords:
{{$keywords}}

Text Analytics:
{{$text_analytics}}

Focus on:
- Mentions of transcripts (NM_...)
- Mentions of variants (c.XXX...>XXX...)

Return the same text, with any corrections made.
"""

# Prompt template mapping for easy access
PROMPT_TEMPLATES = {
    "validation/validate_document.skprompt.txt": VALIDATION_PROMPT,
    "extraction/extract_mutations.skprompt.txt": EXTRACTION_PROMPT,
    "summarization/summarize_report.skprompt.txt": SUMMARIZATION_PROMPT,
    "summarization/correct_summary_mistakes.skprompt.txt": CORRECTION_PROMPT,
}
