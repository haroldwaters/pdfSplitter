import os
import time
from PyPDF2 import PdfFileWriter, PdfFileReader

# The directory where we will find our input files
input_dir = "./input"

# The directory where we will output our files
output_dir = "./output"

# The directory where we will move processed PDFs
processed_dir = "./processed"

# The extension for a PDF file
pdf_extension = ".pdf"


def check_dirs():
    # Before proceeding, make sure that our dirs all exists, and and make them if they don't
    for dir in [input_dir, output_dir, processed_dir]:
        if not os.path.isdir(dir):
            os.mkdir(dir)


def main():

    # An infinite loop. Typically this is Very Bad, but it's okay to use for event loops
    while True:
        # Get a list of each file in the inpurt directory
        files = os.scandir(input_dir)

        # Iterate through each of the files in the dir
        for file in files:
            # Find the last '.' in the name, this should corrospond with the start of the extention
            # rfind searchs starting at the right, so we know for sure that this is the last occurrence
            # of the search string
            file_extension_start = file.name.rfind('.')

            # Grab everything the last '.' onwards
            file_extension = file.name[file_extension_start:]

            # If the extension of the file is equal to pdf_extension then we have a PDF and should do PDF things to it
            if file_extension == pdf_extension:
                # Open the PDF with our PDF reader by passing the file path
                # "rb" here means "Read Binary", we do this because the library makes us because it is stupid
                input_pdf = PdfFileReader(open(file.path, "rb"))

                # Get the number of pages in this PDF
                num_pages = input_pdf.numPages

                # Loop through each page and do stuff
                # range() as called here returns a list from 0 to num_pages. If num_pages was 6, the list would
                # be: [0, 1, 2, 3, 4, 5]. The "i" here stands for index and will store the value for our current
                # postion in the list
                for i in range(num_pages):
                    # This is an object that we will use to write the PDF file for this page
                    output = PdfFileWriter()

                    # We're going to add the page equal to our index to the output PDF
                    output.addPage(input_pdf.getPage(i))

                    # TODO: Update this
                    # This construct here is a little more complicated: "with" is a failsafe way of opening a file handle using
                    # open(). The string being passed into open is the name of the file we're creating, which is being interpolated
                    # (your word of the day) with "%s" to include our current index. "wb" stands for "Write Binary", meaning that
                    # output_stream will receive a "stream" of 1s and 0s and write them to the destination file
                    with open(os.path.join(os.getcwd(), output_dir, "document-page%s.pdf" % i), "wb") as output_stream:
                        # Here's where the file actually gets written. We call output's "write" method to pass a write stream to
                        # output_stream and write the file. There's a number of reasons why streams are a Good Thing, but mostly it's
                        # because they're light on memory usage and very efficient for moving large files
                        output.write(output_stream)

            # Once we've processed a file, move it to the processed directory.
            os.rename(os.path.join(input_dir, file.name),
                      os.path.join(processed_dir, file.name))

        # It's important to close file system objects when you open them without "with"
        files.close()

        # Sleep the event loop
        time.sleep(10)


check_dirs()
main()
