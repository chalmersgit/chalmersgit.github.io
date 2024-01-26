import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode

def parse_bib_file(bib_file_path):
    with open(bib_file_path, 'r', encoding='utf-8') as bib_file:
        parser = BibTexParser()
        parser.customization = convert_to_unicode
        bib_database = bibtexparser.load(bib_file, parser=parser)
    return bib_database.entries

def convert_to_html_list(entries):
    entries.sort(key=lambda x: x.get('year', 0), reverse=True)

    html_list = ""

    current_year = None
    for entry in entries:
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
        html_list += f"                <paper_authors><b>{entry.get('authors', 'Unknown Authors')}</b></paper_authors><br>\n"
        html_list += f"                <paper_publisher>{entry.get('publisher', 'Unknown Publisher')}</paper_publisher><br>\n"
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
