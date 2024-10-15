# Apk_Url_Grep
APK URL Extractor is a Python tool that extracts URLs, APIs, and important links from APK files. It scans through the APK's contents, categorizing links into distinct sections: "Important Links," "APIs," and "URLs." This tool is useful for security analysis, debugging, and reviewing network communications in APKs.


# APK URL Extractor

**APK URL Extractor** is a tool designed to extract and categorize URLs, APIs, and important links from APK files. Whether you're analyzing network communication, security protocols, or general external references in an APK, this tool organizes the extracted information into a structured format for easy review.

## Features
- Extracts URLs from APK files.
- Identifies API endpoints.
- Classifies important links.
- Outputs the results in a structured format with sections for "Important Links," "APIs," and "URLs."

## Installation
**Apktool**
Need to Install APK tool on your Linux 
**Follow This**
Linux
Download the Repo 
Move apktool and apktool.jar file to /usr/local/bin/ directory by using 
Move both apktool.jar and apktool to /usr/local/bin. (root needed) 
Make sure both files are executable. (chmod +x)
( sudo cp apktool apktool.jar /usr/local/bin/. )

Try running apktool via CLI.

To use this tool, ensure you have Python installed on your machine. You can install the required dependencies using `pip`.

Install Required Dependencies 

pip install -r requirements.txt

after that run the tool 

Apk_Url_Grep.py <apk file> output.txt

