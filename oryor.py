import io
import re
import json
import requests
from google.cloud import vision

def find_oryor_no_from_img(path):
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    for text in texts:
        match = re.search(r'\d{2}-\d-\d{5}-\d-\d{4}', text.description)
        if match is not None:
            return match.group()
    return None

def query_oryor_no_info(oryor_no):
    url = 'https://oryor.com/oryor2015/ajax-check-product.php'
    r = requests.post(url, data= { 'number_src': oryor_no })
    obj = json.loads(r.text[3:]) # skip 3-bytes UTF-8 BOM
    return obj['output'][0]

def query_oryor_info_from_img(path):
    oryor_no = find_oryor_no_from_img(path)
    if oryor_no is not None:
        return query_oryor_no_info(oryor_no)
    return None

if __name__ == "__main__":

    import sys
    from pprint import pprint as pp

    path = sys.argv[1]
    result = query_oryor_info_from_img(path)
    pp(result)
