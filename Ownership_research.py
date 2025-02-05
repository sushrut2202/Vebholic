import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time
from urllib.parse import quote_plus, urljoin

# Load the Excel file
file_path = r"C:\Users\DELL\Desktop\Ownershi_research1.xlsx"
df = pd.read_excel(file_path)

# Function to perform a web search using the project name and type
def search_project_owner(project_name, project_type):
    try:
        # Encode the project name and type for URL query
        query = f"{project_name} {project_type} owner"
        search_url = f"https://www.google.com/search?q={quote_plus(query)}"
        
        # Send GET request to Google search results page
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()

        # Parse the Google search results page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the first valid link from search results
        result_link = None
        for item in soup.find_all('a', href=True):
            link = item['href']
            # Skip any links that are JavaScript or script-related
            if 'http' in link and not link.startswith('/httpservice'):
                if link.startswith('/'):
                    # Handle relative URLs by joining with the base URL
                    result_link = urljoin('https://www.google.com', link)
                else:
                    result_link = link
                break

        # If a valid link was found, scrape the project page to find owner info
        if result_link:
            project_response = requests.get(result_link, headers=headers)
            project_response.raise_for_status()
            project_soup = BeautifulSoup(project_response.content, 'html.parser')

            # Example extraction logic for owner (you need to modify this based on the actual page)
            owner = None
            owner_tag = project_soup.find('a', href=re.compile(r'about|contact'))
            if owner_tag:
                owner = owner_tag.get_text(strip=True)
            
            return owner, result_link

    except Exception as e:
        print(f"Error searching for owner for {project_name}: {e}")
        return None, None

# Function to update the DataFrame with owner information
def update_project_ownership(df):
    owners = []
    sources = []

    # Loop through each project and extract owner info
    for index, row in df.iterrows():
        project_name = row['PROJECT_NAME']
        project_type = row['TYPE']

        # Skip rows with missing project names or types
        if pd.isna(project_name) or pd.isna(project_type):
            owners.append(None)
            sources.append(None)
            continue

        owner, source = search_project_owner(project_name, project_type)

        owners.append(owner)
        sources.append(source)

        # Adding a small delay to prevent overloading the server (you can adjust the delay as needed)
        time.sleep(2)

    # Update DataFrame with new owner and source columns
    df['Owner'] = owners
    df['Source'] = sources

    return df

# Update the DataFrame with the new ownership information
updated_df = update_project_ownership(df)

# Save the updated DataFrame to a new Excel file
updated_file_path = r"C:\Users\DELL\Desktop\Updated_Ownership_research1.xlsx"
updated_df.to_excel(updated_file_path, index=False)

print(f"Updated file saved at: {updated_file_path}")
