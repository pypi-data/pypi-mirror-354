# rettxmutation - RettX Mutation Analysis Library

## Purpose
- **Analyze genetic documents systematically** to:
  - Extract and identify MECP2 mutations.
  - Normalize mutation data for downstream applications.
- **Output structured results** with confidence scores for decision-making.

## Features
### 1. Flexible Workflow
With this library you can cover different use cases.
- **Batch Processing**: Process multiple files in a single run.
- **Single File Analysis**: Handle individual files, triggered by:
  - File uploads.
  - Scheduled tasks.
  - API calls.
- **Input Types**:
  - Images (preprocessed to optimize OCR results).
  - PDF documents (direct text extraction).

### 2. Systematic Workflow
- **Preprocessing** (for images):
  - Binarization, sharpening, and contrast adjustment.
  - Enhances image quality for better OCR accuracy.
- **Text Extraction**:
  - OCR applied to extract raw text.
  - Text cleaned to remove artifacts and standardize formatting.
- **Keyword Detection**:
  - Identify MECP2-related terms and gene variants.
  - Assign confidence scores to detected keywords.
- **Summarization and Correction**:
  - Generate concise summaries using OpenAI.
  - Validate and correct summaries with Azure Cognitive Services (Text Analytics for Health).
- **Mutation Extraction**:
  - Extract potential mutations and assign confidence scores.
  - Filter mutations based on user-defined thresholds.
- **Data Enrichment**:
  - Query Ensembl.org for detailed mutation information.
  - Map mutations to transcripts and protein variants.

### 3. Integration-Ready Outputs
- **Models**: Built with Pydantic v2 for seamless data validation.
- **Output Formats**:
  - JSON (structured data).
  - Objects ready for database storage (e.g., CosmosDB).
- **Confidence Scores**:
  - Provided as-is for users to interpret and filter based on needs.

## Limitations
- **Basic Retry Mechanisms**:
  - The library includes a retry policy for specific external calls:
    - **Ensembl**: Retries API requests for fetching variations when encountering:
      - HTTP errors.
      - Connection issues.
      - Timeout errors.
    - **OpenAI**: Similar retry logic ensures stability in mutation summarization and extraction tasks.
  - Retries are implemented using exponential backoff (up to 5 attempts).
- **Error Handling Beyond Retries**:
  - If all retry attempts fail, the library does not provide fallback mechanisms.
  - Invalid results or unhandled errors must be managed by the caller.
- **MECP2 Priority**:
  - Current version focuses exclusively on MECP2 mutations.
  - Extension to other genes or conditions is possible but not yet implemented.

## Workflow Summary
1. **Input**:
   - Accept image or PDF files.
2. **Preprocessing**:
   - Enhance image quality if the input is an image.
3. **Text Analysis**:
   - Extract, clean, and summarize text (using OpenAI and Text Analytics for Health)
4. **Mutation Detection**:
   - Identify potential mutations with confidence scores.
5. **Enrichment**:
   - Fetch detailed data for detected mutations from Ensembl.org.
6. **Output**:
   - Provide structured results for integration with databases or other systems.

## Use Cases
- **Patient Registries**:
  - Populate genetic information for research or clinical databases.
- **Research Tools**:
  - Provide insights for studies on Rett Syndrome and related conditions.
- **Custom Applications**:
  - Integrate with applications using flexible workflows and output formats.

## Design Highlights
- **High Flexibility**:
  - Modular design supports various workflows (batch, single-file, triggered).
- **Separation of Concerns**:
  - Focused on analysis; storage is left to external systems.
- **Pydantic Models**:
  - Facilitate easy integration with databases like CosmosDB.

## Future Enhancements
- Add support for fallback mechanisms to handle errors gracefully.
- Extend functionality to detect mutations in other genes or conditions.
- Implement additional preprocessing for specialized input types (e.g., handwritten documents).
- Enable multilingual text analysis for broader applicability (pending to validate with an extended dataset)