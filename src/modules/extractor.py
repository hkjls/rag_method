from unstructured.partition.pdf import partition_pdf
from pathlib import Path
import os
from os.path import isfile, isdir
import base64
from PIL import Image
from io import BytesIO

class extractor:
    def __init__(self):
        self._chunks = None
        self._tt = None
        self._images = None

    @property
    def chunks(self):
        return self._chunks
    
    @chunks.setter
    def chunks(self, file_name):
        try:
            self._chunks = partition_pdf(
                filename=file_name,
                infer_table_structure=True,    #allow to extract the tables in the document
                strategy="hi_res",             #cause we activate the infer_table_structure (true)
                extract_image_block_types=["Image"], # Add Table to list extract image of tables
                extract_image_block_output_dir=True, # If None, images and tables will saved in base64

                extract_image_block_to_payload=True, # If true, will extract base64 for API usage

                chunking_strategy="by_title", # or'basic'
                max_characters=1000,
                combine_text_under_n_chars=200,
                new_after_n_chars=6000
                # extract_images_in_pdf=True
            )
        except TypeError as e:
            print(e)
            

    @property
    def tt(self):
        return self._tt

    @tt.setter
    def tt(self, chunks=None):
        data = {
            "texts":[],
            "tables":[]
        }
        if chunks:
            for chunk in chunks:
                if "Table" in str(type(chunk)):
                    data["tables"].append(chunk)

                if "CompositeElement" in str(type(chunk)):
                    data["texts"].append(chunk)

            self._tt = data

    @property
    def images(self):
        return self._images

    @images.setter
    def images(self, chunks=None): #base64
        image64 = []
        for chunk in chunks:
            if "CompositeElement" in str(type(chunk)):
                chunks_els = chunk.metadata.orig_elements
                
                for el in chunks_els:
                    if "Image" in str(type(el)):
                        image64.append(el.metadata.image_base64)
        
        self._images = image64


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent.parent
    files = [f"{root}/media/{file}" for file in os.listdir(f"{root}/media") if not isfile(file)]

    data_file = extractor()
    data_file.chunks = files[0]

    data_file.tt = data_file.chunks
    data_file.images = data_file.chunks

    for image in data_file.images:

        image_data = base64.b64decode(image)
        image_bytes = BytesIO(image_data)
        img = Image.open(image_bytes)

        img.show()

