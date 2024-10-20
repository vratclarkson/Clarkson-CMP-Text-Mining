import urllib.request
import xml.etree.ElementTree as ET
import csv
import sys

def log(message):
    with open("process_log.txt", "a") as log_file:
        log_file.write(message + "\n")

def fetch_xml(doi):
    url = f"https://api.elsevier.com/content/article/doi/{doi}?httpAccept=text/xml"
    headers = {
        "X-ELS-APIKey": "b2b74324bf927a84a18b896f5e67a978",
        "Accept": "text/xml"
    }
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        log(f"An error occurred while fetching XML for DOI {doi}: {e}")
    return None

def parse_xml(xml_content):
    try:
        root = ET.fromstring(xml_content)
        
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
        log(f"An error occurred while parsing XML: {e}")
    return None

def write_to_csv(data, output_file):
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['DOI', 'Section', 'Content'])  # Header
            for doi, sections in data.items():
                for section, content in sections.items():
                    writer.writerow([doi, section, content])
        log(f"CSV file '{output_file}' has been created successfully.")
    except Exception as e:
        log(f"An error occurred while writing to CSV: {e}")

def process_dois(dois):
    all_data = {}
    for doi in dois:
        log(f"Processing DOI: {doi}")
        xml_content = fetch_xml(doi)
        if xml_content:
            sections = parse_xml(xml_content)
            if sections:
                all_data[doi] = sections
                log(f"Successfully processed DOI: {doi}")
            else:
                log(f"Failed to parse XML for DOI: {doi}")
        else:
            log(f"Failed to fetch XML for DOI: {doi}")
    return all_data

if __name__ == "__main__":
    dois = [
        "10.1016/j.colsurfa.2011.07.039",
        "10.1016/j.apsusc.2015.03.170",
        "10.1016/j.mssp.2022.107043",
        "10.1016/8978-0-12-821791-7.00002-2",
        "10.1016/j.apsusc.2015.09.149",
        "10.1016/j.solidstatesciences.2009.08.014",
        "10.1016/j.jcrysgro.2013.03.011",
        "10.1016/j.mssp.2021.106280",
        "10.1016/j.ijheatmasstransfer.2014.07.020",
        "10.1016/j.ceramint.2022.10.037"
    ]
    
    output_file = "processed_papers.csv"
    
    log("Starting DOI processing")
    all_data = process_dois(dois)
    write_to_csv(all_data, output_file)
    
    log("DOI processing completed")
    log(f"Processing completed. Results written to '{output_file}'. Please check 'process_log.txt' for details.")

print("Script execution completed. Please check 'process_log.txt' for details.")
