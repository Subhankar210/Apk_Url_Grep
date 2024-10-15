import re
import os
import zipfile
import argparse
import requests
import tempfile
from urllib.parse import urlparse

# URL regex pattern for extracting general URLs
url_regex = re.compile(
    r'https?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

# Regex pattern to match URLs that look like API endpoints
api_regex = re.compile(r'https?://[^/]+/[^/]*(?:api|v[0-9])/[^ ]*')

# Regex pattern for any additional important links (you can adjust this as needed)
important_link_regex = re.compile(r'https?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))*')

# Function to extract URLs and categorize them as general, API, or important links
def extract_urls(file_content):
    urls = set(re.findall(url_regex, file_content))  # Use sets to avoid duplicates
    apis = set(re.findall(api_regex, file_content))  # APIs should be a subset of URLs
    important_links = set([url for url in urls if re.match(important_link_regex, url)])

    # Remove APIs from the general URL list
    urls -= apis
    # Remove important links from the general URL list (if they overlap)
    urls -= important_links

    return urls, apis, important_links

# Function to handle APKs either locally or from a remote URL
def handle_apk(apk_path_or_url):
    if apk_path_or_url.startswith(('http://', 'https://')):
        print(f"Downloading APK from URL: {apk_path_or_url}")
        response = requests.get(apk_path_or_url)
        if response.status_code == 200:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(response.content)
                temp_apk_path = temp_file.name
            return temp_apk_path
        else:
            raise Exception(f"Failed to download APK. HTTP status code: {response.status_code}")
    else:
        if os.path.exists(apk_path_or_url):
            return apk_path_or_url
        else:
            raise FileNotFoundError(f"APK file not found: {apk_path_or_url}")

# Function to unzip APK and extract URLs, APIs, and important links from contained files
def unzip_and_grep(apk_path, output_file):
    with zipfile.ZipFile(apk_path, 'r') as zip_ref:
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_ref.extractall(temp_dir)

            # Open the output file in write mode (overwrite each time)
            with open(output_file, 'w') as outfile:
                # Recursively go through all files in the extracted APK
                all_urls = set()
                all_apis = set()
                all_important_links = set()

                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                urls, apis, important_links = extract_urls(content)

                                all_urls.update(urls)
                                all_apis.update(apis)
                                all_important_links.update(important_links)

                        except Exception as e:
                            print(f"Could not read file {file_path}: {str(e)}")

                # Write the found items into separate sections in the output file
                if all_important_links:
                    outfile.write("[Important Links]\n")
                    for link in all_important_links:
                        outfile.write(f"{link}\n")
                    outfile.write("\n")

                if all_apis:
                    outfile.write("[APIs]\n")
                    for api in all_apis:
                        outfile.write(f"{api}\n")
                    outfile.write("\n")

                if all_urls:
                    outfile.write("[URLs]\n")
                    for url in all_urls:
                        outfile.write(f"{url}\n")
                    outfile.write("\n")

# Main function to parse arguments and invoke the script
def main():
    parser = argparse.ArgumentParser(description='Extract URLs, APIs, and important links from an APK file and store in an output file.')
    parser.add_argument('apk', help='Path to APK file or URL of APK')
    parser.add_argument('output_file', help='File to save found URLs, APIs, and important links')
    args = parser.parse_args()

    apk_path = handle_apk(args.apk)
    unzip_and_grep(apk_path, args.output_file)

if __name__ == '__main__':
    main()
