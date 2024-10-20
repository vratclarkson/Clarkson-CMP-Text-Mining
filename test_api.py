import urllib.request
import json

def log(message):
    with open("api_test_log.txt", "a") as log_file:
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
            log(f"Response status: {response.status}")
            log(f"Response headers: {json.dumps(dict(response.headers))}")
            return response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        log(f"HTTP Error {e.code}: {e.reason}")
        log(f"Error headers: {json.dumps(dict(e.headers))}")
    except Exception as e:
        log(f"An error occurred while fetching XML for DOI {doi}: {str(e)}")
    return None

if __name__ == "__main__":
    log("Starting API test")
    test_doi = "10.1016/j.colsurfa.2011.07.039"
    xml_content = fetch_xml(test_doi)
    
    if xml_content:
        with open("test_output.xml", "w", encoding="utf-8") as f:
            f.write(xml_content)
        log(f"XML content for DOI {test_doi} has been saved to test_output.xml")
        log(f"First 100 characters of XML content: {xml_content[:100]}")
    else:
        log(f"Failed to fetch XML for DOI {test_doi}")

    log("Script execution completed.")

print("Script execution completed. Please check api_test_log.txt for details.")
