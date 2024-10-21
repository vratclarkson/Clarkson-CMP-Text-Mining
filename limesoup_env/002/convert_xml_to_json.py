import os
import lxml.etree as ET
import json
from collections import OrderedDict

# Function to extract sections from XML file using lxml
def extract_sections_from_xml(xml_file):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        paper_data = OrderedDict()

        # Extract metadata
        doi = root.xpath(".//article-id[@pub-id-type='doi']/text()")
        title = root.xpath(".//article-title/text()")
        paper_data['DOI'] = doi[0] if doi else 'Not available'
        paper_data['Title'] = title[0] if title else 'Not available'

        # Sections to extract
        sections = ['Abstract', 'Keywords', 'Introduction', 'Methods', 'Results', 'Discussion', 'Conclusion', 'References']
        
        for section in sections:
            content = root.xpath(f".//sec[title='{section}']//p/text()")
            paper_data[section] = "\n".join(content) if content else "Not available"

        return paper_data

    except Exception as e:
        print(f"Error processing file {xml_file}: {str(e)}")
        return None

# Function to convert extracted data to JSON and save
def save_json(data, output_path):
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Saved JSON to {output_path}")
    except Exception as e:
        print(f"Error saving JSON file: {str(e)}")

# Function to iterate over all XML files and process them
def process_all_xml_files():
    current_folder = os.getcwd()  # Get the current directory where the script is located
    output_folder = os.path.join(current_folder, "output_json")  # Save the JSON files in an "output_json" folder

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in os.listdir(current_folder):
        if file_name.endswith(".xml"):
            input_path = os.path.join(current_folder, file_name)
            output_path = os.path.join(output_folder, file_name.replace(".xml", ".json"))

            # Extract sections from the XML
            paper_data = extract_sections_from_xml(input_path)
            if paper_data:
                save_json(paper_data, output_path)

# Main driver function
if __name__ == "__main__":
    # Process all XML files in the current folder
    process_all_xml_files()
