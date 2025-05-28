from PyPDF4 import PdfFileReader, PdfFileWriter

input_path = "./papers/nguyen2025interaction.pdf"
output_path = "output.pdf"

with open(input_path, "rb") as input_file:
    reader = PdfFileReader(input_file)
    writer = PdfFileWriter()

    # Add all pages except the first (page 0)
    for i in range(1, reader.getNumPages()):
        writer.addPage(reader.getPage(i))

    with open(output_path, "wb") as output_file:
        writer.write(output_file)
