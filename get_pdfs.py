'''
This is a short script for downloading PDFs from web URLs and extracting text (when possible).
it can be paired with a parser to analyze the text and convert it into useful data or with a 
crawler to automatically scrape URLs, but I haven't written them yet. 
   
In order to function, this script requires three Python libaries: requests, PyPDF2 and BeautifulSoup4.
Each of these libraries can be easily installed using Python's pip utility. It also uses the built-in
library StringIO to read PDFs as a binary stream.
   
Basic usage is as follows:
  
web_pdf_to_text(YOUR_URL, YOUR_SAVE_FILE)
   
The script will stream the PDF from the URL and save it as a .txt file (so make sure to include ".txt" 
in the file suffix) at the location you indicate. I've also created functionality for just downloading a
PDF without extracting text. If you include the "as_pdf=True" flag, the script will download and save the 
PDF in addition to the text file, replacing ".txt" with ".pdf" for the file suffix. This feature is 
recommended when you aren't sure if the PDF includes machine-readable text.
'''
   
import requests, PyPDF2
from bs4 import BeautifulSoup
from StringIO import StringIO

def download_pdf(url, out_file):
'''Use this if all you want to do is download the PDF, without any text extraction
   or processing. Usage is the same as web_pdf_to_text, except you should replace
   ".txt"  with ".pdf" as the file suffix.'''
    r = requests.get(url)
    with open(out_file, 'wb') as f:
        for chunk in r.iter_content(chunk_size=128):
            f.write(chunk)

def get_pdf(url):
'''Helper function for web_pdf_to_text; converts HTTP response into binary stream that
   can be read through the PyPDF2.PdfFileReader interface.'''
    r = requests.get(url)
    return PyPDF2.PdfFileReader(StringIO(r.content))


def web_pdf_to_text(url, out_file, as_pdf=False):
'''Main function
    reader = get_pdf(url)
    with open(out_file, 'w') as f:
        for page in reader.pages:
            text = page.extractText()
            f.write(text)
    if as_pdf:
        pdf_out_file = outfile[:-3] + 'pdf'
        with open(pdf_out_file, 'wb') as f:
            writer = PyPDF2.PdfFileWriter()
            writer.cloneDocumentFromReader(reader)
            writer.write(f)


'''
The code below allows you to run this script from the command-line, using the following
format: python get_pdfs.py YOUR_URL YOUR_SAVE_FILE OPTIONAL_FLAG.

Use the optional flags ("t" for True and "f" for False) to signify whether to use the 
as_pdf flag in the web_pdf_to_text function call.

To access the functions above as a library, simply use "import" from the interactive 
interpreter or from another script.
'''

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 3:
        url, outfile = sys.argv[1:]
        web_pdf_to_text(url, outfile)
    elif len(sys.argv) == 4:
        url, outfile, flag = sys.argv[1:]
        if flag == "f":
            web_pdf_to_text(url, outfile, as_pdf=False)
        elif flag == "t":
            web_pdf_to_text(url, outfile, as_pdf=False)
        else:
            raise Exception('Invalid flag argument. Use "f" or "t" for False or True.')
     else:
         num_args = len(sys.argv)
         raise Exception('''Invalid number of arguments. 
                            get_pdfs take two or three arguments. 
                            %d arguments given.''' % num_args)
    
