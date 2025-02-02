# Word Frequency Analysis of BC Legislative Documents
This project analyzes word frequencies in BC Legislative documents using Stanford CoreNLP and Python. The program extracts text from PDF documents, processes it using natural language processing techniques, and generates a comprehensive word frequency analysis.

## Requirements

### Python Libraries
Install the following Python libraries using pip:
```bash
pip install easyocr        # For OCR text extraction from PDFs
pip install PyMuPDF        # For PDF processing
pip install pandas         # For data manipulation
pip install numpy          # For array operations
pip install pycorenlp      # For Stanford CoreNLP 
```

## Integration

Stanford CoreNLP Setup

1. Download Stanford CoreNLP from the official Stanford website
2. Extract the downloaded zip file
3. Navigate to the extracted folder

**Start the CoreNLP server using:**

```bash
java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000
```

## Program Execution

1. Ensure the Stanford CoreNLP server is running
2. Place your PDF documents in a folder named 'data' in the project directory
3. Run the program:

```bash
python word-count.py
```
## **PDF Documents**
The following PDF documents from BC Legislative Public Statutes and Regulations were analyzed:

1. Act1(AccessibleBritishColumbia).pdf (10 pages)

	Source: Accessible British Columbia Act


2. Act2(EscheatAct).pdf (11 pages)

	Source: Escheat Act


3. Act3(FamilyLawPart1).pdf (4 pages)

	Source: Family Law Act: Part 1 (Interpretation)



## **Output**
The program generates a CSV file named 'word_frequencies.csv' containing:

- First column: Unique words in vocabulary (lexicographic order)
- Second column: Total word counts across all documents
- Additional columns: Word counts for each individual PDF document
- Final row: Total counts for each column

**Important Notes**

- The program uses OCR (Optical Character Recognition) to extract text from PDFs, so processing might take some time depending on your computer's specifications.
- Ensure all PDFs are in the 'data' directory before running the program.
- The Stanford CoreNLP server must be running on port 9000 before executing the program.
- The program requires an active internet connection for the first run to download EasyOCR models.

## **Technical Implementation Details**

1. OCR is implemented using EasyOCR for reliable text extraction from PDF documents
2. Text processing includes cleaning, tokenization, and word frequency analysis
3. Word counting excludes numbers and special characters, focusing on alphabetic words
4. Results are sorted alphabetically and include comprehensive frequency statistics

## **Troubleshooting**
If you encounter any issues:

1. Verify that Stanford CoreNLP server is running (default port: 9000)
2. Check that all required Python libraries are installed
3. Ensure PDF documents are properly placed in the 'data' directory
4. Verify that the PDFs are readable and not corrupted
