import pdfplumber as pdf
from pathlib import Path


def extract_table ():
    all_data = []
       
    with pdf.open("https://eenergetskicertifikat.mpgi.hr/api/reports/public/izvadakIzBazeCertifikata") as pdf:
        first_page = pdf.pages[0]
        table_settings = {'vertical_strategy' : 'lines', 
                           'horizontal_strategy' : 'lines'
                          }
        first_table = first_page.extract_table(table_settings)
        if first_table :
            header = first_table[0][0]
        all_data.extend(first_table[0][1:])
        


