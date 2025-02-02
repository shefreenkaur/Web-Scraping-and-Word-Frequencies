import os #Provides functions to interact with the operating system
import easyocr #OCR library to extract text from images
import pandas as pd #to create and manage the DataFrame of word frequencies
from collections import Counter #to count the words
import re #regular expressions, used for text cleaning
import fitz #PyMuPDF library, used to work with PDF files and convert PDF pages to images
import numpy as np #numerical processing library, used to convert images into arrays that can be processed by EasyOCR

def clean_text(text):
    """In this part, I am:
    1. converting uppercase to lowercase (this will prevent duplication)
    2. removing any special characters or numbers, keeping only alphabets
    3. then I filter out single character words like a or I"""
    if not text:
        return []
    
    #lowercase and remove special characters/numbers
    text = text.lower()
    #re is used for text cleaning
    text = re.sub(r'[^a-z\s]', ' ', text)
    
    #normalize whitespace and split into words
    words = text.split()
    
    #keep only words with length > 1
    return [word for word in words if len(word) > 1]

def process_text(text):
    """
    here we will first get the cleaned words from the previous function
    then, we will count only those cleaned words
    """
    words = clean_text(text)
    return Counter(words)

def extract_text_with_easyocr(pdf_path):
    """
    Extract text from PDF images using EasyOCR.
    This function will:
    1. convert each PDF page to a high-resolution image
    2. use EasyOCR to extract text from each page
    3. combine and clean the extracted text
    """
    print(f"\nProcessing PDF: {os.path.basename(pdf_path)}")
    
    try:
        #initializing easyocr in english language (en)
        reader = easyocr.Reader(['en'])
        
        #use PyMuPDF to open pdf files
        doc = fitz.open(pdf_path)
        full_text = ""
        
        #process each page
        for page_num in range(len(doc)) :
            #gives us the 'pageNum / total pages'
            print(f"Processing page {page_num + 1}/{len(doc)}")
            
            #the matrix argument (2,2) makes the image into a high resolution image
            page = doc[page_num]
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            
            #easyOcr requires numpy to process, which is why I am converting these to an numpy array using np.frombuffer

            """A numpy array is a grid of values, all of the same type, 
            and is indexed by a tuple of nonnegative integers. 
            The number of dimensions is the rank of the array; 
            the shape of an array is a tuple of integers giving the size of the array along each dimension"""

            img_array = np.frombuffer(pix.samples, dtype=np.uint8).reshape(
                pix.height, pix.width, pix.n
            )
            
            #extracts text from the page, passes image to imageOCR
            results = reader.readtext(img_array)
            page_text = " ".join([result[1] for result in results])
            #append the text extracted from each page to full text
            full_text += page_text + "\n"
            
            print(f"Extracted {len(page_text)} characters from page {page_num + 1}")
        
        #Display extraction statistics
        print(f"Total characters extracted: {len(full_text)}")
        if full_text:
            print("Sample of extracted text:")
            print(full_text[:200] + "...\n")
        
        return full_text
        
    except Exception as e:
        print(f"Error during text extraction: {str(e)}")
        return ""

def create_word_frequency_csv(pdf_files, data_folder):
    """Create a CSV file containing word frequencies from all PDFs.
    This function:
    1. Processes each PDF to extract text
    2. Counts word frequencies in each document
    3. Creates a DataFrame with word frequencies
    4. Adds total counts and sorts results """

    "this will store all the frequencies of a particular word"
    all_frequencies = {}
    " set of all unique words across all PDFs"
    all_words = set()
    
    #Process each PDF
    for pdf_file in pdf_files:
        pdf_path = os.path.join(data_folder, pdf_file)
        text = extract_text_with_easyocr(pdf_path)
        
        if text:
            frequencies = process_text(text)
            all_frequencies[pdf_file] = frequencies
            all_words.update(frequencies.keys())
            print(f"Found {len(frequencies)} unique words in {pdf_file}")
        else:
            print(f"No text extracted from {pdf_file}")
            all_frequencies[pdf_file] = Counter()

    #create DataFrame with sorted words
    df = pd.DataFrame(index=sorted(all_words))
    
    #add columns for each PDF
    for pdf_file, frequencies in all_frequencies.items():
        df[pdf_file] = df.index.map(frequencies)
    
    #add total counts column
    df['Total'] = df.sum(axis=1)
    
    #Sort by total frequency
    df = df.sort_values('Total', ascending=False)
    
    #Add totals row
    df.loc['TOTAL'] = df.sum()
    
    return df

def main():
    """ Main function to coordinate the PDF processing and word frequency analysis.
    This function:
    1. Sets up the working environment
    2. Processes all PDFs in the data folder
    3. Creates and saves the word frequency CSV
    4. Displays a sample of the results """
    current_dir = os.getcwd()
    data_folder = os.path.join(current_dir, 'data')
    
    #list of PDF files
    pdf_files = [f for f in os.listdir(data_folder) if f.endswith('.pdf')]
    print(f"Found {len(pdf_files)} PDF files in {data_folder}")
    
    #frequency DataFrame
    df = create_word_frequency_csv(pdf_files, data_folder)
    
    #Save to CSV
    output_path = os.path.join(current_dir, 'word_frequencies.csv')
    df.to_csv(output_path)
    print(f"\nWord frequencies saved to: {output_path}")
    
    #display sample of results
    print("\nSample of word frequencies (top 10 words):")
    print(df.head(10))

if __name__ == "__main__":
    main()