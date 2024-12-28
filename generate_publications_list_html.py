import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode
from bibtexparser.bibdatabase import BibDatabase

import os
import sys
import re
import math


additional_info_map = 	{	'chalmers2023real':[	['DOI', 'https://dl.acm.org/doi/10.1145/3610539.3630250'],
													['Event Page', 'https://asia.siggraph.org/2023/presentation/?id=real_110&sess=sess210'],
													['Video', 'https://youtu.be/lcLjtdlc-7k?feature=shared']],
							'rhee2023real':[		['DOI', 'https://dl.acm.org/doi/10.1145/3588430.3597245'],
													['Event Page', 'https://s2023.siggraph.org/presentation/?id=real_106&sess=sess258'], 
													['Video', 'https://youtu.be/OvC_Wwo6LXU?feature=shared'], 
													['Audience Choice Award', '']],
							'rhee2022teleport':[	['DOI', 'https://dl.acm.org/doi/10.1145/3550453.3570123'],
													['Event Page', 'https://sa2022.siggraph.org/en/presentation/?id=real_107&sess=sess143'],
													['Video', 'https://youtu.be/WoJE1uS8SAo?feature=shared']],
							'suppan2021neural':[	['Best Conference Paper Award', '']],
							'welsford2021spectator':[['Video', 'https://www.youtube.com/watch?v=hmOa0vGOnYE&ab_channel=ACMSIGCHI']],
							#'chalmers2020reconstructing':[['Video', 'https://www.youtube.com/watch?v=TahPGWyMY20&ab_channel=AndrewChalmers']],
							'chalmers2022illumination':[['Video', 'https://www.youtube.com/watch?v=ITHvP2uv1cE&ab_channel=AndrewChalmers']],
							'chalmers2020illumination':[['Video', 'https://www.youtube.com/watch?v=ITHvP2uv1cE&ab_channel=AndrewChalmers']],
							'chalmers2018illumination':[['Video', 'https://www.youtube.com/watch?v=ITHvP2uv1cE&ab_channel=AndrewChalmers']],
							'thompson2019real-caustics':[	['Poster', '']],
							'rhee2018mr360':[		['Second Place Award', '']],
							'chen2024neural':[		['Poster', '']],
							'weir2024full':[		['Poster', ''], ['Slides', '']]
						}


def get_file_size(file_path):
	if os.path.exists(file_path):
		fileSize = os.path.getsize(file_path) / (1024 * 1024)
		return str(math.ceil(fileSize))+"MB"
	return None

def parse_bib_file(file_path):
	bibtex_str = ""
	with open(file_path, 'r', encoding='utf-8') as file:
		bibtex_str = file.read()

	entries = []
	current_entry = None

	# Regular expressions for BibTeX entry types and fields
	entry_pattern = re.compile(r'@(\w+){(.*?),', re.DOTALL)
	field_pattern = re.compile(r'\s*(\w+)\s*=\s*{(.*?)}')

	for line in bibtex_str.split('\n'):
		# Match BibTeX entry
		entry_match = entry_pattern.match(line)
		if entry_match:
			if current_entry:
				entries.append(current_entry)

			entry_type = entry_match.group(1)
			entry_key = entry_match.group(2)
			current_entry = {'entry_type': entry_type, 'entry_key': entry_key}
		elif current_entry:
			# Match fields within the entry
			field_match = field_pattern.match(line)
			if field_match:
				field_name = field_match.group(1)
				field_value = field_match.group(2)
				current_entry[field_name] = field_value

	# Add the last entry
	if current_entry:
		entries.append(current_entry)

	return entries

def convert_to_html_list(entries):
	entries.sort(key=lambda x: int(x.get('year', 0)), reverse=True)
	
	html_list = """
<!DOCTYPE html>
<html>
<head>
	<title>ANDREW CHALMERS</title>
	<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=PT+Sans+Narrow&display=swap">
	<style>
		/* Add some basic CSS for layout */
		body {
			font-family: Arial, sans-serif;
			margin: 0;
			padding: 0;
			background-color: #fff; /* Set background color to white for the entire body */
		}
		.container {
			max-width: 800px;
			margin: 0 auto; /* Center the container */
			padding: 20px; /* Add margin around the container */
			background-color: #fff; /* Add a white background to the container */
			box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1); /* Add a box shadow for a card effect */
		}
		header {
			background-color: #fff; /* Add white background to the header */
			color: #333; /* Change text color for better contrast */
			padding: 10px;
			display: flex;
			justify-content: space-between;
			align-items: center; /* Vertically center content */
			border-bottom: 1px solid #333; /* Add a horizontal line */
			font-family: 'PT Sans Narrow', sans-serif; /* Apply PT Sans Narrow to the header */
		}
		header h1 {
			margin: 0;
			font-family: 'PT Sans Narrow', sans-serif; /* Change the font family */
		}
		nav ul {
			list-style-type: none;
			padding: 0;
			margin: 0;
		}
		nav ul li {
			display: inline;
			margin-right: 20px;
			padding-right: 20px;
		}
		nav ul li:last-child {
			margin-right: 0;
			padding-right: 0;
		}
		/* Change tab text color to black and make it bold */
		nav ul li a {
			color: #000;
			font-weight: normal;
			text-decoration: none; /* Remove underlines */
		}
		/* Style for active tab */
		nav ul li.active a {
			font-weight: bold;
		}
		main .content {
			display: block; /* Single-column layout */
			padding-right: 20px;
		}
		main .content .text {
			margin-top: 20px; /* Add margin to create space between text and header line */
		}
		img {
			max-width: 100%;
			height: auto;
		}

		h2 {
		  text-align: center;
		  position: relative;
		}

		h2::after {
		  content: '';
		  display: block;
		  position: absolute;
		  bottom: 0;
		  left: 50%;
		  width: 100%;
		  transform: translateX(-50%);
		  height: 1px;
		  background-color: #333; 
		}

		paper_title {
			font-weight: bold;
			color: #2980b9;
			font-size: 14px;
		}

		paper_authors {
			font-size: 12px;
		}

		paper_publisher {
			font-size: 12px;
		}

		

		/* Style for the list */
		ul {
			list-style: none;
			padding: 0;
			margin: 0;
		}

		/* Style for each list item */
		li {
			margin-bottom: 20px;
			overflow: hidden;
			display: flex;
			align-items: center;
		}

		/* Style for thumbnail image */
		img {
			width: 100px;
			height: auto;
			margin-right: 10px;
			border: 1px solid black;
			padding: 5px;
			border-radius: 5px;
		}

		/* Style for text */
		.item-text {
			margin-top: 0;
		}

		/* Style for the button */
		.button-main {
		  padding: 1px 5px;
		  font-size: 12px;
		  background-color: #3498db; 
		  color: #fff; 
		  border: none;
		  border-radius: 5px;
		  cursor: pointer;
		}

		.button-main:hover {
		  background-color: #2980b9; 
		}

		.button-other {
		  padding: 1px 5px;
		  font-size: 12px;
		  background-color: #cf7f30; 
		  color: #fff; 
		  border: none;
		  border-radius: 5px;
		  cursor: pointer;
		}

		.button-other:hover {
		  background-color: #b97129; 
		}

		.button-award {
		  padding: 1px 5px;
		  font-size: 12px;
		  background-color: #cca300; 
		  color: #fff; 
		  border: none;
		  border-radius: 5px;
		  cursor: pointer;
		}

		.button-award:hover {
			background-color: #cca300;
			cursor: auto; /* Explicitly set cursor to default arrow */
		}

	</style>
</head>
<body>
	<div class="container"> <!-- Added a container div for centering -->
		<header>
			<h1>ANDREW CHALMERS</h1>
			<nav>
				<ul>
					<li><a href="index.html">Home</a></li>
					<li class="active"><a href="research.html"><b>Research</b></a></li>
				</ul>
			</nav>
		</header>
		<!-- Add a horizontal line below the header -->
		<hr style="border: none; border-top: 1px solid #333; margin: 0;">

		<main>
			<h2>Research</h2> <!-- Centered "Research" text with Roboto font -->
			<div class="content">
				<!-- Add your research content here -->
				<!-- Add any research-related images here -->
				<img src="images/research-banner.png" alt="Research Banner" style="width: 100%;">
				<h2>Publications</h2>
"""

	# TODO add bibtex entry for copy/paste
	
	current_year = None
	for entry in entries:
		entry_key = entry.get('entry_key', 'Unknown')
		year = entry.get('year', 'Unknown')
		if year != current_year:
			if current_year is not None:
				html_list += "        </ul>\n"
			html_list += f"\n<h3 style=\"text-align: left;\">{year}</h3>\n"
			html_list += "        <ul>\n"
			current_year = year
			print(current_year)

		title = entry.get('title', 'Unknown Title')
		publisher = refine_html_journal(entry.get('booktitle', entry.get('journal', 'Misc.')))

		entry_key, publisher = handle_special_cases(title, entry_key, publisher)

		title = refine_html_title(title)

		link_thumbnail = './thumbnails/'+entry_key+'-thumbnail.jpg'

		link_pdf = './papers/'+entry_key+'.pdf'
		link_pdf_compressed = './papers-compressed/'+entry_key+'-compressed.pdf'
		link_pdf_appendix = './papers/'+entry_key+'-appendix.pdf'
		if not os.path.exists(link_pdf_appendix):
			link_pdf_appendix = None


		additional_info = []
		if entry_key in additional_info_map:
			additional_info = additional_info_map[entry_key]
		
		#print(year, entry.get('title'))
		if publisher!='Misc.':
			html_list += "          <li>\n"
			html_list += f"            <img src=\"{link_thumbnail}\" alt=\"{entry.get('thumbnail_alt', 'Thumbnail')}\">\n"
			html_list += "            <div class=\"item-text\">\n"
			html_list += f"                <paper_title>{title}</paper_title><br>\n"
			html_list += f"                <paper_authors>{entry.get('author', 'Unknown Authors')}</paper_authors><br>\n"
			html_list += f"                <paper_publisher>{publisher}, {year}</paper_publisher><br>\n"
			html_list += f"                <button class=\"button-main\" onclick=\"window.open(\'{link_pdf}\', \'_blank\')\">PDF {get_file_size(link_pdf)}</button>"
			if get_file_size(link_pdf_compressed)!=None and get_file_size(link_pdf_compressed)!="1MB":
				html_list += f"                <button class=\"button-main\" onclick=\"window.open(\'{link_pdf_compressed}\', \'_blank\')\">PDF {get_file_size(link_pdf_compressed)}</button>\n"
			if link_pdf_appendix:
				html_list += f"                <button class=\"button-other\" onclick=\"window.open(\'{link_pdf_appendix}\', \'_blank\')\">Appendix {get_file_size(link_pdf_appendix)}</button>\n"				
			for item in additional_info:
				button_style = "button-main"

				# Button style
				if item[0]=='Video' or item[0]=='Poster' or item[0]=='Slides' or item[0]=='DOI' or item[0]=='Event Page':
					button_style = "button-other"
				elif 'Award' in item[0]:
					button_style = "button-award"

				#
				if item[0]=='Poster':
					item[1] = './papers/'+entry_key+'-poster.pdf'
				elif item[0]=='Slides':
					item[1] = './slides/'+entry_key+'.pptx'

				#
				if item[1]=='':
					html_list += f"                <button class=\"{button_style}\"\">{item[0]}</button>\n"
				else:
					html_list += f"                <button class=\"{button_style}\" onclick=\"window.open(\'{item[1]}\', \'_blank\')\">{item[0]}</button>\n"
			
			html_list += "            </div>\n"
			html_list += "          </li>\n"
	html_list += "        </ul>\n"

	html_list = refine_html(html_list)

	html_list +="""
			</main>
		</div>

	</body>
</html>
"""

	return html_list

def replace_substring_ignore_case(original_string, old_substring, new_substring):
	return re.sub(re.escape(old_substring), new_substring, original_string, flags=re.IGNORECASE)

def refine_html(html_list):
	html_list = html_list.replace("Chalmers, Andrew", "<b>Chalmers, Andrew</b>")
	html_list = html_list.replace("\\&", "&")
	html_list = html_list.replace("Rhee, Tae Hyun", "Rhee, Taehyun")
	html_list = replace_substring_ignore_case(html_list, "Pacific Graphics Short Papers, Posters, and Work-in-Progress Papers", "Pacific Graphics")
	html_list = html_list.replace("PG (Short Papers)", "Pacific Graphics")
	html_list = html_list.replace("PG", "Pacific Graphics")
	html_list = html_list.replace("and others", "and Rhee, Taehyun")
	html_list = html_list.replace("{\\\"", "")

	return html_list

def capitalize_string(x):
	connecting_words = ["a", "an", "on", "the", "and", "of", "to", "for", "in", "through", "using", "from"]
	words = x.split()
	updated_words = [word if word.isupper() else word.capitalize() if word.lower() not in connecting_words or i == 0 else word.lower() for i, word in enumerate(words)]
	x = ' '.join(updated_words)
	
	capitalize_after_chars = ['-', ':']
	x_list = list(x)
	for c in capitalize_after_chars:
		indices = [index for index, char in enumerate(x_list) if char == c]
		for idx in indices:
			if idx<len(x) and idx>=0:
				if x_list[idx+1]==' ':
					x_list[idx+2] = x_list[idx+2].upper()
				else:
					x_list[idx+1] = x_list[idx+1].upper()
	x = ''.join(x_list)
	return x.strip()

def handle_special_cases(title, entry_key, publisher):
	# Special case, paper has same ID as the poster
	if title=='Real-time underwater caustics for mixed reality 360° videos':
		entry_key = entry_key+'-caustics'
		publisher += ' (Poster)'
	return entry_key, publisher

def refine_html_title(title_info):
	title_info = capitalize_string(title_info)
	title_info = title_info.replace("Mr360", "MR360")
	title_info = title_info.replace("dof", "DoF")
	title_info = title_info.replace("Hmd", "HMD")
	if title_info[-1]=='.':
		title_info = title_info[:-1]
	return title_info

def refine_html_journal(journal_info):
	# Define a regular expression pattern to match four consecutive digits
	digit_pattern = re.compile(r'\d{4}')

	# Find all matches of four consecutive digits in the input string
	digit_matches = digit_pattern.findall(journal_info)

	# Remove the four consecutive digits from the input string
	output_string = re.sub(digit_pattern, '', journal_info)

	# Define a regular expression pattern to match text within brackets ()
	bracket_pattern = re.compile(r'\([^)]*\)')

	# Remove text within brackets from the output string
	output_string = re.sub(bracket_pattern, '', output_string)

	# Remove any double white spaces
	output_string = re.sub(r'\s+', ' ', output_string)

	return capitalize_string(output_string)


if __name__ == "__main__":
	bib_file_path = "citations.bib" 
	bib_file_path_additional = "citations_additional.bib" 

	entries = parse_bib_file(bib_file_path)+parse_bib_file(bib_file_path_additional)

	html_list = convert_to_html_list(entries)

	output_html_filename = "research.html" 
	with open(output_html_filename, "w", encoding="utf-8") as output_file:
		output_file.write(html_list)

	print("Conversion complete. HTML list saved to "+output_html_filename)
