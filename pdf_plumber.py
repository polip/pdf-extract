import pdfplumber as pdf
from pathlib import Path



with pdf.open("https://eenergetskicertifikat.mpgi.hr/api/reports/public/izvadakIzBazeCertifikata") as pdf:
    first_page = pdf.pages[0]
    print(first_page.chars[0])
