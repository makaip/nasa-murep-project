import csv
import requests
import os
import argparse

DEFAULT_TOKEN = "eyJ0eXAiOiJKV1QiLCJvcmlnaW4iOiJFYXJ0aGRhdGEgTG9naW4iLCJzaWciOiJlZGxqd3RwdWJrZXlfb3BzIiwiYWxnIjoiUlMyNTYifQ.eyJ0eXBlIjoiVXNlciIsInVpZCI6ImpwaW5kZWxsMjAyMiIsImV4cCI6MTczMTAzMTMxOSwiaWF0IjoxNzI1ODQ3MzE5LCJpc3MiOiJodHRwczovL3Vycy5lYXJ0aGRhdGEubmFzYS5nb3YifQ.zNWL8nygB75YgpfKaQVeIGQ_npLww2THf9cfYQifhQIONeo9K9E9pUR4N855RbANzBxdG3dH0AoCy-MFteSht9zN-LmHNqKcvx4ou168dY95-wWPd2gOh3tRhHlxOmatsKdbWL1fpSb7r-F2KSpKl1kowvBOJilC4A4LrD1feBNK5g_FUxFnOz2msiOPB0quzV-nRxoWXBalPne8m372laa6Ynd3LT-HcR2N3WaFZyDI2xgu8NZMZzGwPuCLMe6yeQb-J24xAHMyoJ_fzsHW6WxwqX9bcE1_YLovSYDcHaJTUWvxO-Vz12wUiVVutfZWbsdl3R1CHQw8AavJYWMtkQ"

def download_file(url, destination_folder, token):
    file_name = url.split('/')[-1]
    file_path = os.path.join(destination_folder, file_name)
    os.makedirs(destination_folder, exist_ok=True)
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    try:
        print(f"Downloading {file_name} from {url}...")
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()

        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)

    except requests.exceptions.RequestException as e:
        print(f"Failed to download {file_name}. Error: {e}")

def download_files_from_csv(csv_file_path, destination_folder, token):
    with open(csv_file_path, mode='r') as csvfile:
        for row in csv.DictReader(csvfile):
            full_url = f"https://ladsweb.modaps.eosdis.nasa.gov{row['fileUrls for custom selected']}"
            download_file(full_url, destination_folder, token)

def parse_arguments(): 
    parser = argparse.ArgumentParser(description="Download files from URLs specified in a CSV file.")
    parser.add_argument("csv_file", help="Path to the CSV file containing the file URLs.")
    parser.add_argument("download_folder", help="Path to the folder where files will be downloaded.")
    parser.add_argument("--token", default=DEFAULT_TOKEN, help="Bearer token for authentication (optional, defaults to token in script).")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    download_files_from_csv(args.csv_file, args.download_folder, args.token)
