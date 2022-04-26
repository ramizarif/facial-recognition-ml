import requests
import os
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse

def isUrlValid(url): 
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def getAllImages(url): 
    soup = bs(requests.get(url).content, "html.parser")
    count = 0
    urls = []
    for img in tqdm(soup.find_all("img"), "Extracting Images"):
        img_url = img.attrs.get("src")
        if not img_url:
            continue
        img_url = urljoin(url, img_url)
        try:
            pos = img_url.index("?")
            img_url = img_url[:pos]
        except ValueError:
            pass

        if isUrlValid(img_url):
            urls.append(img_url)
            count+=1
            if (count == 10):
                break
    
    return urls

def download(url, pathname): 
    # if path doesn't exist, make that path dir
    if not os.path.isdir(pathname):
        os.makedirs(pathname)
    # download the body of response by chunk, not immediately
    response = requests.get(url, stream=True)
    # get the total file size
    file_size = int(response.headers.get("Content-Length", 0))
    # get the file name
    filename = os.path.join(pathname, url.split("/")[-1])
    # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
    progress = tqdm(response.iter_content(1024), f"Downloading {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        for data in progress.iterable:
            # write data read to the file
            f.write(data)
            # update the progress bar manually
            progress.update(len(data))

def main(url, path):
    imgs = getAllImages(url)
    for img in imgs: 
        download(img, path)
main("https://louisville.edu/", "Images/scrapetest")
    