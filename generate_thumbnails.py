import glob
import fitz

import cv2
import numpy as np
import sys
import os

# crop_params = top left corner, and size, expressed as ratio

cases = {	'chalmers2024avatar360':(0,((0.2,0.6),(0.35,0.35))),
			'chen2024neural':(4,((0.15,0.05),(0.45,0.8))),
			'rhee2023real':(0,((0.3,0.42),(0.34,0.34))),
			'chalmers2023real':(0,((0.36,0.7),(0.1,0.1))),
			'zaman2023mrmac':(0,((0.15,0.31),(0.25,0.25))),
			'chalmers2023motion':(0,((0.45,0.59),(0.15,0.15))),
			'zhao2023deep':(0,((0.26,0.57),(0.2,0.2))),
			'o2023simulating':(0,((0.16,0.5),(0.3,0.3))),
			'weir2023lighting':(0,((0.25,0.5),(0.54,0.54))),
			'chalmers2022illumination':(1,((0.08,0.15),(0.4,0.7))),
			'chen2022casual':(1,((0.05,0.05),(0.17,0.25))),
			'weir2022deep':(1,((0.15,0.345),(0.2,0.2))),
			'rhee2022teleport':(0,((0.34,0.61),(0.15,0.18))),
			'zhao2021adaptive':(0,((0.17,0.125),(0.34,0.25))),
			'suppan2021neural':(1,((0.11,0.7),(0.18,0.18))),
			'chalmers2020reconstructing':(1,((0.05,0.8),(0.13,0.13))),
			'chalmers2020illumination':(0,((0.3,0.05),(0.28,0.9))),
			'thompson2019real':(0,((0.15,0.5),(0.26,0.5))),
			'thompson2019underwater':(1,((0.05,0.05),(0.3,0.45))),
			'thompson2019real-caustics':(0,((0.2,0.54),(0.27,0.4))),
			'chalmers2018illumination':(32,((0.43,0.2),(0.5,0.9))),
			'petikam2021art':(0,((0.26,0.11),(0.25,0.25))),
			'welsford2021spectator':(0,((0.34,0.2),(0.25,0.25))),
			'welsford2020asymmetric':(1,((0.2,0.13),(0.15,0.134))),
			'rhee2020augmented':(2,((0.05,0.08),(0.35,0.387))),
			'chalmers2020shadow':(2,((0.3,0.08),(0.15,0.4))),
			'chalmers2020illumination':(3,((0.35,0.05),(0.2,0.3))),
			'petikam2018visual':(6,((0.05,0.05),(0.14,0.24))),
			'rhee2018mixed':(0,((0.25,0.05),(0.45,0.45))),
			'rhee2018mr360':(0,((0.3,0.65),(0.14,0.25))),
			'dean2018magic':(3,((0.65,0.05),(0.2,0.4))),
			'rhee2017mr360':(0,((0.13,0.26),(0.2,0.24))),
			'dodgson2017designing':(3,((0.1,0.5),(0.35,0.4))),
			'ma2015synthesising':(5,((0.54,0.63),(0.18,0.3))),
			'chalmers2014perceptually':(0,((0.25,0.695),(0.2,0.25))),
			'chalmers2014sky':(0,((0.48,0.1),(0.15,0.27))),
			'chalmers2013perceptually':(4,((0.51,0.5),(0.3,0.5)))
		}

def remove_whitespace(image_array):
    # Find indices of non-white pixels along rows and columns
    non_white_rows = np.any(image_array != 255, axis=1)
    non_white_cols = np.any(image_array != 255, axis=0)

    # Find the bounding box of the non-white region
    min_row, max_row = np.where(non_white_rows)[0][[0, -1]]
    min_col, max_col = np.where(non_white_cols)[0][[0, -1]]

    # Crop the image_array based on the bounding box
    cropped_image_array = image_array[min_row:max_row+1, min_col:max_col+1]

    return cropped_image_array

def crop_image_by_ratio(image, top_left_ratio, size_ratio, do_remove_whitespace=True):
    height, width, _ = image.shape

    y_ratio, x_ratio = top_left_ratio
    h_ratio, w_ratio = size_ratio

    y = int(y_ratio * height)
    x = int(x_ratio * width)
    h = int(h_ratio * width) # instead of height, do it relative to width
    w = int(w_ratio * width)

    cropped_image = image[y:y+h, x:x+w, :]

    if do_remove_whitespace:
	    cropped_image = remove_whitespace(cropped_image)

    return cropped_image

def applyBorder(img, T=5):
	img[:,:T,:] = 0
	img[:,img.shape[1]-1-T:img.shape[1]-1,:] = 0
	img[:T,:,:] = 0
	img[img.shape[1]-1-T:img.shape[1]-1,:,:] = 0
	return img

def extract_and_save_page_as_image(pdf_path, page_number, crop_params, base_name, save_folder):
	thumbnail_filename = f"{save_folder}/{base_name}-thumbnail.jpg"
	target_resolution = (300,300)

	# Open the PDF file
	pdf_document = fitz.open(pdf_path)

	# Check if the specified page number is valid
	if page_number < pdf_document.page_count:
		# Get the specified page
		page = pdf_document[page_number]
		pix = page.get_pixmap(dpi=200)  # render page to an image
		img = cv2.imdecode(np.frombuffer(pix.tobytes("ppm"), np.uint8), cv2.IMREAD_COLOR)
		if crop_params is not None:
			img = crop_image_by_ratio(img,crop_params[0],crop_params[1])
		img = pad_into_square(img)
		img = cv2.resize(img, target_resolution, interpolation=cv2.INTER_AREA)
		#img = applyBorder(img)

		cv2.imwrite(thumbnail_filename, img)

		# Close the PDF file
		pdf_document.close()
	else:
		print(f"Invalid page number: {page_number}")

def pad_into_square(image_array):
	# Get the height and width of the image
	height, width, _ = image_array.shape

	# Determine the padding needed to make the image square
	if height < width:
		pad_size = width - height
		top_pad = pad_size // 2
		bottom_pad = pad_size - top_pad
		padded_image = np.pad(image_array, ((top_pad, bottom_pad), (0, 0), (0, 0)), mode='constant', constant_values=255)
	elif width < height:
		pad_size = height - width
		left_pad = pad_size // 2
		right_pad = pad_size - left_pad
		padded_image = np.pad(image_array, ((0, 0), (left_pad, right_pad), (0, 0)), mode='constant', constant_values=255)
	else:
		# Image is already square, no padding needed
		padded_image = image_array.copy()

	return padded_image

def get_pdfs_in_subfolder(folder_path):
	pdf_files = glob.glob(f"{folder_path}/**/*.pdf", recursive=True)
	# Exclude files with "-compressed.pdf" in their names
	pdf_files = [file for file in pdf_files if "-compressed.pdf" not in file]
	return pdf_files

def process_img(pdf_document, image_index, base_name, save_folder): 
	target_resolution = (300,300)

	# Get the image data
	image_data = pdf_document.extract_image(image_index)
	image_bytes = image_data["image"]

	# Convert image data to NumPy array
	img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
	img = pad_into_square(img)
	img = cv2.resize(img, target_resolution, interpolation=cv2.INTER_AREA)

	# Save the image to the "thumbnails" subfolder
	thumbnail_filename = f"{save_folder}/{base_name}-thumbnail.jpg"
	#print("Writing:",thumbnail_filename)
	cv2.imwrite(thumbnail_filename, img)

def generate_thumb(pdf_path):
	# Open the PDF file
	pdf_document = fitz.open(pdf_path)
	base_name = os.path.splitext(os.path.basename(pdf_path))[0]
	save_folder = 'thumbnails'

	if not os.path.exists(save_folder):
		os.makedirs(save_folder)

	page_number, crop_params = 0, None
	try:
		page_number, crop_params = cases[base_name]
	except:
		pass

	if crop_params is None:
		return
	extract_and_save_page_as_image(pdf_path, page_number, crop_params, base_name, save_folder)
	return

	## Iterate through pages
	#for page_number in range(pdf_document.page_count):
	#	page = pdf_document[page_number]
	#	# Get the first image on the page
	#	images = page.get_images(full=True)
	#	if images:
	#		first_image = images[img_index]
	#		process_img(pdf_document, first_image[0], base_name, save_folder)
	#		pdf_document.close()
	#		return

	# No images found in the PDF
	print("No images found in the PDF:",pdf_path)
	thumbnail_filename = f"{save_folder}/{base_name}-thumbnail.jpg"
	#print("Writing:",thumbnail_filename)
	cv2.imwrite(thumbnail_filename, np.ones((50,50,3))*255)

def generate_thumbs():
	print("Generating thumbs...")

	subfolder_path = './papers/'
	pdf_files_list = get_pdfs_in_subfolder(subfolder_path)
	numPDFs = len(pdf_files_list)

	print("PDF Files in Subfolder:")
	count = 1
	for pdf_file in pdf_files_list:
		print(count,'/',numPDFs, pdf_file)
		generate_thumb(pdf_file)
		count+=1

if __name__ == "__main__":
	print("Running...")
	generate_thumbs()
	print("Complete.")
