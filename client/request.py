import requests as rq
from pathlib import Path
import json
from os.path import isfile, isdir
import os

ROOT = Path(__file__).resolve().parent.parent

def file_from_link(file_name='file_downloaded.pdf', URL=None):

    if URL:
        file_name = f"{ROOT}/media/{file_name}.pdf"
        response = rq.get(URL)
        if response.status_code == 200:
            with open(file_name, "wb") as file:
                file.write(response.content)

        # raise ValueError(response.status_code)


if __name__ == "__main__":
    with open(f"{ROOT}/client/www.json", "rb") as file:
        pdf = json.load(file)
        # files = [file for file in os.listdir(f"{ROOT}/media/") if not isfile(file)]
        for e in pdf:
            file_from_link(f"{e["name"]}",e["url"])