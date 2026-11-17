import os
import sys
import glob
import json
import requests

# Configuration: Set your Zenodo API token in your environment variables:
# export ZENODO_TOKEN="your_actual_token_here"
ACCESS_TOKEN = os.getenv("ZENODO_TOKEN")

if not ACCESS_TOKEN:
    print("Error: ZENODO_TOKEN environment variable is not set.")
    print("Run: export ZENODO_TOKEN='your_token' before running this script.")
    sys.exit(1)

# Base URL for Zenodo API (use sandbox.zenodo.org/api for testing if preferred)
BASE_URL = "https://zenodo.org/api/deposit/depositions"
HEADERS = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

# Find the latest generated archive
archive_files = glob.glob("csv_power_law_zenodo_*.tar.gz")
if not archive_files:
    print("Error: No archive matching 'csv_power_law_zenodo_*.tar.gz' found.")
    sys.exit(1)

archive_path = sorted(archive_files)[-1]
print(f"Found archive for upload: {archive_path}")

# Step 1: Create a new deposition
print("Creating new Zenodo deposition...")
response = requests.post(BASE_URL, headers=HEADERS, json={})
if response.status_code != 201:
    print(f"Failed to create deposition: {response.status_code} - {response.text}")
    sys.exit(1)

deposition = response.json()
deposition_id = deposition["id"]
bucket_url = deposition["links"]["bucket"]
print(f"Deposition created successfully. ID: {deposition_id}")

# Step 2: Upload the archive file to the bucket URL
print(f"Uploading {archive_path} to Zenodo bucket...")
with open(archive_path, "rb") as fp:
    file_upload_url = f"{bucket_url}/{archive_path}"
    upload_response = requests.put(
        file_upload_url,
        data=fp,
        headers={**HEADERS, "Content-Type": "application/octet-stream"}
    )

if upload_response.status_code not in [200, 201]:
    print(f"Failed to upload file: {upload_response.status_code} - {upload_response.text}")
    sys.exit(1)
print("File uploaded successfully.")

# Step 3: Update metadata from zenodo.json if present
if os.path.exists("zenodo.json"):
    print("Updating deposition metadata from zenodo.json...")
    with open("zenodo.json", "r") as f:
        meta_data = json.load(f)
    
    meta_response = requests.put(
        f"{BASE_URL}/{deposition_id}",
        headers={**HEADERS, "Content-Type": "application/json"},
        json=meta_data
    )
    if meta_response.status_code == 200:
        print("Metadata updated successfully.")
    else:
        print(f"Warning: Failed to update metadata: {meta_response.status_code} - {meta_response.text}")

print(f"\nUpload complete! Deposition ID {deposition_id} is saved as a draft on Zenodo.")
print(f"Manage it at: https://zenodo.org/deposit/{deposition_id}")
