import fitz
import csv
import sys
from pathlib import Path
import unicodedata


def extract_tables_from_pdf(pdf_path, output_csv=None):
    """Extract table data from PDF using PyMuPDF"""
    if not Path(pdf_path).exists():
        print(f"Error: PDF file '{pdf_path}' not found")
        return
    
    doc = fitz.open(pdf_path)
    
    # Ensure proper text extraction with Unicode support
    fitz.TOOLS.set_small_glyph_heights(True)
    all_tables = []
    
    print(f"Processing {len(doc)} pages...")
    
    for page_num in range(0,5):
        page = doc.load_page(page_num)
        
        # Find tables on the page
        tables = page.find_tables()
        table_list = list(tables)
        
        if table_list:
            print(f"Found {len(table_list)} table(s) on page {page_num + 1}")
            
            for table_num, table in enumerate(table_list):
                # Extract table data
                table_data = table.extract()
                
                # Add page and table info to each row with proper Unicode handling
                for row in table_data:
                    # Normalize Unicode characters to handle Croatian letters properly
                    normalized_row = []
                    for cell in row:
                        if isinstance(cell, str):
                            # Clean control characters and normalize Unicode
                            cleaned_cell = ''.join(char for char in cell if unicodedata.category(char)[0] != 'C' or char in '\t\n\r')
                            normalized_cell = unicodedata.normalize('NFC', cleaned_cell)
                            normalized_row.append(normalized_cell)
                        else:
                            normalized_row.append(cell)
                    all_tables.append([page_num + 1, table_num + 1] + normalized_row)
    
    doc.close()
    
    if not all_tables:
        print("No tables found in the PDF")
        return
    
    # Save to CSV
    if output_csv is None:
        output_csv = Path(pdf_path).stem + "_extracted_tables_0_5.csv"
    
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Page', 'Table', 'Column1', 'Column2', 'Column3', 'Column4', 'Column5'])  # Adjust headers as needed
        writer.writerows(all_tables)
    
    print(f"Extracted {len(all_tables)} rows from tables")
    print(f"Data saved to: {output_csv}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <pdf_file> [output_csv]")
        print("Example: python main.py document.pdf extracted_data.csv")
        return
    
    pdf_file = sys.argv[1]
    output_csv = sys.argv[2] if len(sys.argv) > 2 else None
    
    extract_tables_from_pdf(pdf_file, output_csv)


if __name__ == "__main__":
    main()
