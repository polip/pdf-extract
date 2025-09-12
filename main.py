import fitz
import csv
import sys
from pathlib import Path


def extract_tables_from_pdf(pdf_path, output_csv=None):
    """Extract table data from PDF using PyMuPDF"""
    if not Path(pdf_path).exists():
        print(f"Error: PDF file '{pdf_path}' not found")
        return
    
    doc = fitz.open(pdf_path)
    all_tables = []
    
    print(f"Processing {len(doc)} pages...")
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        
        # Find tables on the page
        tables = page.find_tables()
        table_list = list(tables)
        
        if table_list:
            print(f"Found {len(table_list)} table(s) on page {page_num + 1}")
            
            for table_num, table in enumerate(table_list):
                # Extract table data
                table_data = table.extract()
                
                # Add page and table info to each row
                for row in table_data:
                    all_tables.append([page_num + 1, table_num + 1] + row)
    
    doc.close()
    
    if not all_tables:
        print("No tables found in the PDF")
        return
    
    # Save to CSV
    if output_csv is None:
        output_csv = Path(pdf_path).stem + "_extracted_tables.csv"
    
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
