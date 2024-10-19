import httpx
import time
import xml.dom.minidom

# Define constants
PAPER_DOI = "10.1016/j.surfin.2024.104682"
API_KEY = "890a2c153b09210cea2748119fe33b58"

def get_full_xml(paper_doi, apikey):
    """
    Fetch full XML content for a paper from Scopus API.
    
    :param paper_doi: DOI of the paper
    :param apikey: API key for Scopus
    :return: XML content as string
    """
    headers = {
        "X-ELS-APIKey": apikey,
        "Accept": 'text/xml'
    }
    timeout = httpx.Timeout(10.0, connect=60.0)
    
    with httpx.Client(timeout=timeout, headers=headers) as client:
        url = f"https://api.elsevier.com/content/article/doi/{paper_doi}?view=FULL"
        try:
            response = client.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes
            return response.text
        except httpx.HTTPStatusError as e:
            print(f"HTTP Error: {e}")
            print(f"Response content: {e.response.text}")
        except Exception as e:
            print(f"An error occurred: {e}")
    return None

# Call the function and process the result
xml_content = get_full_xml(PAPER_DOI, API_KEY)

if xml_content:
    # Save the XML content to a file
    with open("full_paper.xml", "w", encoding="utf-8") as f:
        f.write(xml_content)
    print("Full XML content has been saved to 'full_paper.xml'")
    
    # Pretty print the first 1000 characters of the XML for preview
    try:
        dom = xml.dom.minidom.parseString(xml_content)
        pretty_xml = dom.toprettyxml()
        print("\nPreview of the XML content:")
        print(pretty_xml[:1000] + "...")
    except Exception as e:
        print(f"Failed to pretty print XML: {e}")
        print("\nFirst 1000 characters of raw XML:")
        print(xml_content[:1000] + "...")
else:
    print("Failed to retrieve XML content")
