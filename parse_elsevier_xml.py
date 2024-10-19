import sys
from LimeSoup.ElsevierSoup_XML import ElsevierXMLSoup

def parse_elsevier_xml(xml_file_path):
    # Read the XML file
    with open(xml_file_path, 'r', encoding='utf-8') as file:
        xml_content = file.read()

    # Parse the XML content using ElsevierXMLSoup
    parsed_data = ElsevierXMLSoup.parse(xml_content)

    # Print the extracted information
    print("Journal:", parsed_data.get('Journal'))
    print("DOI:", parsed_data.get('DOI'))
    print("Title:", parsed_data.get('Title'))
    print("Keywords:", ', '.join(parsed_data.get('Keywords', [])))
    
    print("\nSections:")
    for section in parsed_data.get('Sections', []):
        if isinstance(section, dict):
            print(f"\n{section['name']}:")
            print(section['content'])
        else:
            print(section)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python parse_elsevier_xml.py <path_to_full_paper.xml>")
        sys.exit(1)

    xml_file_path = sys.argv[1]
    parse_elsevier_xml(xml_file_path)
