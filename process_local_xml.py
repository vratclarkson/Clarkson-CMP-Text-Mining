import xml.etree.ElementTree as ET
import csv
import os

def parse_xml(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # Define the namespace
        ns = {'ja': 'http://www.elsevier.com/xml/ja/dtd'}

        # Extract sections
        sections = {}
        for section in root.findall('.//ja:ce:sections/ja:ce:section', ns):
            title = section.find('ja:ce:section-title', ns)
            title = title.text if title is not None else "Untitled Section"
            content = ' '.join([p.text for p in section.findall('.//ja:ce:para', ns) if p is not None and p.text])
            sections[title] = content

        # Extract title and abstract
        title = root.find('.//ja:ce:title', ns)
        title = title.text if title is not None else "No Title"
        abstract = ' '.join([p.text for p in root.findall('.//ja:ce:abstract//ja:ce:simple-para', ns) if p is not None and p.text])

        # Add title and abstract to sections
        sections['Title'] = title
        sections['Abstract'] = abstract

        return sections
    except Exception as e:
        print(f"An error occurred while parsing XML file {file_path}: {e}")
    return None

def write_to_csv(data, output_file):
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['File', 'Section', 'Content'])  # Header
            for file, sections in data.items():
                for section, content in sections.items():
                    writer.writerow([file, section, content])
        print(f"CSV file '{output_file}' has been created successfully.")
    except Exception as e:
        print(f"An error occurred while writing to CSV: {e}")

def process_xml_files(file_list):
    all_data = {}
    for file in file_list:
        print(f"Processing file: {file}")
        sections = parse_xml(file)
        if sections:
            all_data[file] = sections
            print(f"Successfully processed file: {file}")
        else:
            print(f"Failed to parse XML file: {file}")
    return all_data

if __name__ == "__main__":
    xml_files = ['full_paper.xml', 'full_paper_2.xml']
    output_file = "processed_papers_local.csv"
    
    print("Starting XML processing")
    all_data = process_xml_files(xml_files)
    write_to_csv(all_data, output_file)
    
    print("XML processing completed")
    print(f"Processing completed. Results written to '{output_file}'.")

    # Write a summary to a log file
    with open("process_summary.txt", "w") as log_file:
        log_file.write("XML Processing Summary:\n")
        for file in xml_files:
            if file in all_data:
                log_file.write(f"- {file}: Successfully processed\n")
            else:
                log_file.write(f"- {file}: Failed to process\n")
        log_file.write(f"\nOutput file created: {output_file}\n")

print("Script execution completed. Please check 'process_summary.txt' for a summary of the processing.")
