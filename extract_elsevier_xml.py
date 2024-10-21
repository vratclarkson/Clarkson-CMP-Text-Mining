import json
import sys
from lxml import etree

def extract_elsevier_xml(xml_content):
    # Parse the XML content
    parser = etree.XMLParser(recover=True)
    root = etree.fromstring(xml_content.encode('utf-8'), parser=parser)
    
    # Get the actual namespaces from the XML
    namespaces = root.nsmap
    
    print(f"Root tag: {root.tag}", file=sys.stderr)
    print(f"Namespaces: {namespaces}", file=sys.stderr)
    
    # Extract journal, doi, and title
    coredata = root.find('coredata')
    print(f"Coredata found: {coredata is not None}", file=sys.stderr)
    
    journal = coredata.find('prism:publicationName', namespaces) if coredata is not None else None
    doi = coredata.find('prism:doi', namespaces) if coredata is not None else None
    title = coredata.find('dc:title', namespaces) if coredata is not None else None
    
    print(f"Journal element found: {journal is not None}", file=sys.stderr)
    print(f"DOI element found: {doi is not None}", file=sys.stderr)
    print(f"Title element found: {title is not None}", file=sys.stderr)

    # Extract keywords
    keywords = root.findall('.//ce:keywords/ce:keyword', namespaces)
    print(f"Number of keywords found: {len(keywords)}", file=sys.stderr)

    # Extract abstract
    abstract = root.find('.//ce:abstract/ce:abstract-sec/ce:simple-para', namespaces)
    print(f"Abstract found: {abstract is not None}", file=sys.stderr)

    # Extract sections
    sections = root.findall('.//ce:section', namespaces)
    print(f"Number of sections found: {len(sections)}", file=sys.stderr)

    # Organize the extracted information into a JSON structure
    json_data = {
        "journal": journal.text if journal is not None else None,
        "doi": doi.text if doi is not None else None,
        "title": title.text if title is not None else None,
        "keywords": [keyword.text for keyword in keywords],
        "abstract": abstract.text if abstract is not None else None,
        "sections": [
            {
                "name": section.find('ce:section-title', namespaces).text,
                "content": section.find('ce:para', namespaces).text
            }
            for section in sections
            if section.find('ce:section-title', namespaces) is not None and section.find('ce:para', namespaces) is not None
        ]
    }

    return json_data

def main():
    input_file = "paper_01.xml"
    output_file = "extracted_paper_01.json"
    debug_file = "debug_output.txt"

    try:
        # Redirect stderr to the debug file
        sys.stderr = open(debug_file, 'w')

        # Read the XML file
        with open(input_file, 'r', encoding='utf-8') as file:
            xml_content = file.read()

        print("XML content read successfully", file=sys.stderr)

        # Extract and process the XML content
        json_data = extract_elsevier_xml(xml_content)

        # Write the JSON output to a file
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(json_data, file, indent=2, ensure_ascii=False)

        print(f"Extraction complete. Results saved in '{output_file}'", file=sys.stderr)
        
        # Print debug information
        print("\nExtracted Data:", file=sys.stderr)
        print(f"Journal: {json_data['journal']}", file=sys.stderr)
        print(f"DOI: {json_data['doi']}", file=sys.stderr)
        print(f"Title: {json_data['title']}", file=sys.stderr)
        print(f"Keywords: {json_data['keywords']}", file=sys.stderr)
        print(f"Abstract: {json_data['abstract'][:100] if json_data['abstract'] else 'None'}...", file=sys.stderr)
        print(f"Number of sections: {len(json_data['sections'])}", file=sys.stderr)
        
    except Exception as e:
        print(f"An error occurred: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
    finally:
        # Reset stderr
        sys.stderr.close()
        sys.stderr = sys.__stderr__

if __name__ == "__main__":
    main()
