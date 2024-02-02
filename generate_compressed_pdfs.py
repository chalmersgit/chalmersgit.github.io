#!/usr/bin/env python3
# Author: Theeko74
# Contributor(s): skjerns
# Oct, 2021
# MIT license -- free to use as you want, cheers.

# Modified by Andrew Chalmers

"""
Simple python wrapper script to use ghoscript function to compress PDF files.

Compression levels:
    0: default - almost identical to /screen, 72 dpi images
    1: prepress - high quality, color preserving, 300 dpi imgs
    2: printer - high quality, 300 dpi images
    3: ebook - low quality, 150 dpi images
    4: screen - screen-view-only quality, 72 dpi images

Dependency: Ghostscript.
On MacOSX install via command line `brew install ghostscript`.
"""

import argparse
import os.path
import shutil
import subprocess
import sys
import glob

def get_pdfs_in_subfolder(folder_path):
    pdf_files = glob.glob(f"{folder_path}/**/*.pdf", recursive=True)
    # Exclude files with "-compressed.pdf" in their names
    pdf_files = [file for file in pdf_files if "-compressed.pdf" not in file]
    return pdf_files

def compress(input_file_path, output_file_path, power=0):
    """Function to compress PDF via Ghostscript command line interface"""
    quality = {
        0: "/default",
        1: "/prepress",
        2: "/printer",
        3: "/ebook",
        4: "/screen"
    }

    # Basic controls
    # Check if valid path
    if not os.path.isfile(input_file_path):
        print("Error: invalid path for input PDF file.", input_file_path)
        sys.exit(1)

    # Check compression level
    if power < 0 or power > len(quality) - 1:
        print("Error: invalid compression level, run pdfc -h for options.", power)
        sys.exit(1)

    # Check if file is a PDF by extension
    if input_file_path.split('.')[-1].lower() != 'pdf':
        print(f"Error: input file is not a PDF.", input_file_path)
        sys.exit(1)

    gs = get_ghostscript_path()
    print("Compress PDF...")
    initial_size = os.path.getsize(input_file_path)
    subprocess.call(
        [
            gs,
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel=1.4",
            "-dPDFSETTINGS={}".format(quality[power]),
            "-dNOPAUSE",
            "-dQUIET",
            "-dBATCH",
            "-sOutputFile={}".format(output_file_path),
            input_file_path,
        ]
    )
    final_size = os.path.getsize(output_file_path)
    ratio = 1 - (final_size / initial_size)
    print("Compression by {0:.0%}.".format(ratio))
    print("Final file size is {0:.5f}MB".format(final_size / 1000000))
    print("Done.")


def get_ghostscript_path():
    gs_names = ["gs", "gswin32", "gswin64c"] # gswin64 to gswin64c to suppress window
    for name in gs_names:
        if shutil.which(name):
            return shutil.which(name)
    raise FileNotFoundError(
        f"No GhostScript executable was found on path ({'/'.join(gs_names)})"
    )

def compress_file(fileNameInput, compression_level=1, delete_compressed=False):
    directory, file_name = os.path.split(fileNameInput)
    base_name, extension = os.path.splitext(file_name)
    new_file_name = f"{base_name}-compressed{extension}"
    outDir = directory + "-compressed"
    fileNameOutput = os.path.join(outDir, new_file_name)

    if not os.path.exists(outDir):
        os.makedirs(outDir)

    if not os.path.exists(fileNameOutput):
        if not delete_compressed:
            compress(fileNameInput, fileNameOutput, power=compression_level)
    else:
        print("Compressed version already exists:", fileNameOutput)
        if delete_compressed:
            os.remove(fileNameOutput) # delete


def compress_single():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("input", help="Relative or absolute path of the input PDF file")
    parser.add_argument("-c", "--compress", type=int, help="Compression level from 0 to 4")
    args = parser.parse_args()

    # In case no compression level is specified, default is 2 '/ printer'
    if not args.compress:
        args.compress = 1

    compress_file(args.input, args.compress)

def compress_folder():
    print("Compress folder...")

    subfolder_path = './papers/'
    pdf_files_list = get_pdfs_in_subfolder(subfolder_path)
    numPDFs = len(pdf_files_list)

    print("PDF Files in Subfolder:")
    delete_compressed = False
    compression_level = 2
    count = 1
    for pdf_file in pdf_files_list:
        print(count,'/',numPDFs)
        if 'compressed.pdf' in pdf_file:
            print("File is already compressed:", pdf_file)
            #print(pdf_file)
            if delete_compressed:
                os.remove(pdf_file) # delete
        else:
            compress_file(pdf_file, compression_level, delete_compressed)
        count+=1

if __name__ == "__main__":
    print("Running...")
    #compress_single()
    compress_folder()

    print("Complete.")
