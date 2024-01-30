import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode
from bibtexparser.bibdatabase import BibDatabase

import sys
import re

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
	entries.sort(key=lambda x: x.get('year', 0), reverse=True)

	html_list = ""

	current_year = None
	for entry in entries:
		#print(entry)
		year = entry.get('year', 'Unknown')
		if year != current_year:
			if current_year is not None:
				html_list += "        </ul>\n"
			html_list += f"\n<h3 style=\"text-align: left;\">{year}</h3>\n"
			html_list += "        <ul>\n"
			current_year = year

		html_list += "          <li>\n"
		html_list += f"            <img class=\"thumbnail\" src=\"{entry.get('thumbnail_src', './data/dummy_thumb.png')}\" alt=\"{entry.get('thumbnail_alt', 'Publication Thumbnail')}\">\n"
		html_list += "            <div>\n"
		html_list += f"                <paper_title>{entry.get('title', 'Unknown Title')}</paper_title><br>\n"
		html_list += f"                <paper_authors>{entry.get('author', 'Unknown Authors')}</paper_authors><br>\n"
		html_list += f"                <paper_publisher>{entry.get('booktitle', 'Unknown booktitle')}</paper_publisher><br>\n"
		html_list += "            </div>\n"
		html_list += "          </li>\n"
	
	html_list += "        </ul>\n"

	return html_list

if __name__ == "__main__":
	bib_file_path = "./data/citations.bib"  # Replace with your BibTeX file path
	entries = parse_bib_file(bib_file_path)

	html_list = convert_to_html_list(entries)

	with open("output.html", "w", encoding="utf-8") as output_file:
		output_file.write(html_list)

	print("Conversion complete. HTML list saved to output.html")
