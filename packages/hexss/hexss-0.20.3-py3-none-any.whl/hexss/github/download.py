from typing import Union
import os
from pathlib import Path

import hexss

hexss.check_packages('requests', 'tqdm', auto_install=True)

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from hexss.constants.terminal_color import *
from tqdm import tqdm

headers = hexss.get_config('headers')


def collect_file_tasks(api_url, dest_folder):
    """
    Recursively collects file download tasks from the GitHub API.
    """
    tasks = []
    os.makedirs(dest_folder, exist_ok=True)
    try:
        response = requests.get(api_url, headers=headers, proxies=hexss.proxies or {})
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"\n{RED}Error: Unable to fetch data from {api_url} - {e}{END}")
        return tasks

    try:
        data = response.json()
    except ValueError:
        print(f"\n{RED}Error: Invalid JSON response from {api_url}{END}")
        return tasks

    if not isinstance(data, list):
        print(f"\n{RED}Error: Expected a list of items from {api_url}{END}")
        return tasks

    for item in data:
        item_type = item.get('type')
        if item_type == 'file':
            file_name = item.get('name')
            download_url = item.get('download_url')
            file_path = os.path.join(dest_folder, file_name)
            tasks.append((download_url, file_path))
        elif item_type == 'dir':
            new_api_url = item.get('url')
            new_dest_folder = os.path.join(dest_folder, item.get('name'))
            tasks.extend(collect_file_tasks(new_api_url, new_dest_folder))
    return tasks


def download_file(download_url, file_path):
    """
    Downloads a single file using streaming and displays a file-level progress bar.
    """
    # Skip if file already exists
    if os.path.exists(file_path):
        return
    try:
        with requests.get(download_url, headers=headers, proxies=hexss.proxies or {}, stream=True) as r:
            r.raise_for_status()
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            total_length = r.headers.get('content-length')
            if total_length is None:
                # If no content-length header, simply write the content
                with open(file_path, 'wb') as f:
                    f.write(r.content)
            else:
                downloaded = 0
                with open(file_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)

    except requests.RequestException as e:
        print(f"\n{RED}Failed to download {os.path.basename(file_path)}: {e}{END}")


def download(owner=None, repo=None, path='', dest_folder: Union[Path, str] = '', max_workers=20, api_url=None):
    """
    Recursively downloads content from a GitHub API URL using multi-threaded file downloads.
    Uses an overall progress bar to track total file downloads.
    """
    if api_url is None:
        if not owner or not repo:
            raise ValueError("Both 'owner' and 'repo' must be specified if 'api_url' is not provided.")
        api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"

    if isinstance(dest_folder, str):
        dest_folder = Path(dest_folder)

    if not dest_folder.is_absolute():
        dest_folder = hexss.path.get_script_dir() / dest_folder

    tasks = collect_file_tasks(api_url, dest_folder)
    print(f"\n{CYAN}Found {len(tasks)} files to download in '{dest_folder}'.{END}")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        # Create a global progress bar for overall file download progress.
        with tqdm(total=len(tasks), desc="Overall Progress", unit="file") as pbar:
            for download_url, file_path in tasks:
                future = executor.submit(download_file, download_url, file_path)
                # Update the global progress bar as soon as a file download completes.
                future.add_done_callback(lambda p: pbar.update(1))
                futures.append(future)
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"\n{RED}Error in file download: {e}{END}")


if __name__ == "__main__":
    # dir is `<script_dir>\photos`
    download(
        'hexs', 'Image-Dataset', 'flower_photos', max_workers=200,
        dest_folder=Path('photos')
    )

    # dir is `C:\PythonProjects\data`
    download(
        'hexs', 'Image-Dataset', 'flower_photos', max_workers=200,
        dest_folder=Path(r'C:\PythonProjects\data')
    )

    # dir is `<script_dir>\data`
    download(
        'hexs', 'auto_inspection_data__QC7-7990-000-Example', max_workers=200,
        dest_folder=Path('data')
    )

    # dir is `C:\PythonProjects\data2`
    download(
        'hexs', 'auto_inspection_data__QC7-7990-000-Example', max_workers=200,
        dest_folder=Path(r'C:\PythonProjects\data2')
    )
