import requests
import os
from zipfile import ZipFile
#import validators

url = [
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip",
]

def is_url_valid(url):
    try:
        response = requests.head(url, timeout = 5)
        return response.status_code == 200
    except requests.RequestException as e:
        print(f" Url is not valid: {url}: {e}")
        return False

def download_files(urls, download_dir):
    for link in urls:
        if is_url_valid(link):
            try:
                response = requests.get(link) 
                response.raise_for_status()
                filename = link.split('/')[-1]

                file_path = os.path.join(download_dir, filename)
                with open(file_path, "wb") as f:
                    f.write(response.content)
                print(f"downloaded files: {filename}")
                
                with ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(download_dir)
                os.remove(file_path)
                print(f" Extracted and removed:{filename}")

            except requests.exceptions.RequestException as e:
                print(f"Error {link}: {e}")
        else:
            print(f" skipped URL: {link}")

def main():
    download_dir = os.path.join(os.path.dirname(__file__), "downloads")
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    download_files(url, download_dir)

if __name__ == "__main__":
    main()


