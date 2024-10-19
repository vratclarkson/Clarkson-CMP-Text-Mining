import json
from LimeSoup.ElsevierSoup_XML import ElsevierXMLSoup

def extract_elsevier_xml(file_path):
    try:
        # Read the XML file
        with open(file_path, 'r', encoding='utf-8') as f:
            xml_content = f.read()
        
        # Parse the XML content using ElsevierXMLSoup
        parsed_data = ElsevierXMLSoup.parse(xml_content)
        
        # Print the parsed data
        print(json.dumps(parsed_data, indent=4, ensure_ascii=False))
        
        print("Extraction complete.")
    except Exception as e:
        print(f"An error occurred during parsing: {str(e)}")

def main():
    xml_file_path = "full_paper.xml"
    extract_elsevier_xml(xml_file_path)

if __name__ == "__main__":
    main()
