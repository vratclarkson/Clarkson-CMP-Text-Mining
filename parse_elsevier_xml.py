import xml.etree.ElementTree as ET
import csv

def parse_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Define the namespace
    ns = {'ja': 'http://www.elsevier.com/xml/ja/dtd'}

    # Extract sections
    sections = {}
    for section in root.findall('.//ja:ce:sections/ja:ce:section', ns):
        title = section.find('ja:ce:section-title', ns).text
        content = ' '.join([p.text for p in section.findall('.//ja:ce:para', ns) if p.text])
        sections[title] = content

    # Extract title and abstract
    title = root.find('.//ja:ce:title', ns).text
    abstract = ' '.join([p.text for p in root.findall('.//ja:ce:abstract//ja:ce:simple-para', ns) if p.text])

    # Add title and abstract to sections
    sections['Title'] = title
    sections['Abstract'] = abstract

    return sections

def write_to_csv(data, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Section', 'Content'])  # Header
        for section, content in data.items():
            writer.writerow([section, content])

def write_output(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("Parsed XML Data:\n\n")
        for section, content in data.items():
            f.write(f"{section}:\n{content}\n\n")

if __name__ == "__main__":
    input_file = "full_paper.xml"
    csv_file = "Cerium_Oxide_01.csv"
    output_file = "parsed_output.txt"
    
    sections = parse_xml(input_file)
    write_to_csv(sections, csv_file)
    write_output(sections, output_file)
    
    print(f"CSV file '{csv_file}' and output file '{output_file}' have been created successfully.")
