import requests
from bs4 import BeautifulSoup

# Step 1: Fetch the SWAPI documentation page
def fetch_swapi_documentation():
    url = "https://swapi.dev/documentation#starships"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text  # Return the HTML content
    else:
        raise Exception(f"Failed to fetch documentation: {response.status_code}")

# Step 2: Parse the HTML and extract the starship attributes and descriptions
def extract_metadata(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Locate the starship attributes section
    # Find the <h3> tag that contains the text "Starship"
    starship_header = None
    for h3 in soup.find_all("h3"):
        if "Starship" in h3.text:
            starship_header = h3
            break
    
    if not starship_header:
        raise Exception("Could not find the 'Starship' section in the documentation.")
    
    # Find the next <table> after the <h3> tag
    starship_table = starship_header.find_next("temp1")
    
    if not starship_table:
        raise Exception("Could not find the starship attributes table.")
    
    # Extract rows from the table
    rows = starship_table.find_all("tr")
    
    # Create a metadata table
    metadata_table = []
    for row in rows[1:]:  # Skip the header row
        columns = row.find_all("td")
        if len(columns) >= 2:
            attribute = columns[0].text.strip()
            description = columns[1].text.strip()
            metadata_table.append({
                "Attribute": attribute,
                "Description": description
            })
    
    return metadata_table

# Step 3: Output the metadata table
def print_metadata_table(metadata_table):
    print("| Attribute          | Description                                                                 |")
    print("|--------------------|-----------------------------------------------------------------------------|")
    for entry in metadata_table:
        print(f"| {entry['Attribute']:18} | {entry['Description']:75} |")

# Main function
def main():
    # Fetch the SWAPI documentation page
    html_content = fetch_swapi_documentation()
    
    # Extract metadata from the HTML
    metadata_table = extract_metadata(html_content)
    
    # Print the metadata table
    print_metadata_table(metadata_table)

if __name__ == "__main__":
    main()