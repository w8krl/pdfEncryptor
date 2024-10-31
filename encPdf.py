# Encrypts pdf using standard encryption
# Author: karl.webster@kptv8.com, https://github.com/w8krl, +44 (0) 7456 300 303 31/10/24
# Dependencies: PyPDF2, dotenv (pip install python-dotenv PyPDF2)
#
# Instructions:
# 0) place unencrypted pdfs in the 'input' folder
# 1) Run: python encPdf.py - lists all pdfs in the current directory and prompts for selection
# 2) Enter the index of the pdf to encrypt or type 'all' to encrypt all PDFs (password is loaded from .env file)
# 3) Each encrypted pdf is saved in the 'output' folder as <filename>_protected.pdf (overwrites existing file if it exists)
# 4) Have fun!

import os
from PyPDF2 import PdfReader, PdfWriter
from dotenv import load_dotenv

load_dotenv()

password = os.getenv("PDF_PASSWORD", "defaultPassword")

# List files
def listPdfFiles(directory="./input"):
    pdfFiles = [f for f in os.listdir(directory) if f.endswith(".pdf")]
    for index, file in enumerate(pdfFiles, start=1):
        print(f"{index}. {file}")
    return pdfFiles

# Add pwd encryption to PDF
def addPassword(inputPdf, outputPdf, password):
    pdfReader = PdfReader(inputPdf)
    pdfWriter = PdfWriter()

    # check if enc already
    if pdfReader.is_encrypted:
        print(f"{os.path.basename(outputPdf)} - skipping (already encrypted).")
        return False

    for pageNum in range(len(pdfReader.pages)):
        pdfWriter.add_page(pdfReader.pages[pageNum])

    pdfWriter.encrypt(password)

    # Write encrypted PDF to output
    with open(outputPdf, 'wb') as f:
        pdfWriter.write(f)
    print(f"{os.path.basename(outputPdf)} - encrypted.")
    return True

# main
def main():
    pdfFiles = listPdfFiles()
    if not pdfFiles:
        print("No PDF files found in the current directory.")
        return

    # create dir if not exists
    outputDir = "output"
    os.makedirs(outputDir, exist_ok=True)

    # Get user input
    selection = input("Enter the number of the PDF file to encrypt or type 'all' to encrypt all PDFs: ").strip().lower()

    if selection == "all":
        for pdfFile in pdfFiles:
            outputPdf = os.path.join(outputDir, f"{os.path.splitext(pdfFile)[0]}_protected.pdf")
            addPassword(pdfFile, outputPdf, password)
    else:
        try:
            selectedIndex = int(selection) - 1
            if selectedIndex < 0 or selectedIndex >= len(pdfFiles):
                print("Invalid selection.")
                return
            inputPdf = pdfFiles[selectedIndex]
            outputPdf = os.path.join(outputDir, f"{os.path.splitext(inputPdf)[0]}_protected.pdf")
            addPassword(inputPdf, outputPdf, password)
        except ValueError:
            print("Invalid input. Please enter a number or 'all'.")

# call main program
if __name__ == "__main__":
    main()
