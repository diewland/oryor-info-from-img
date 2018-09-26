import io
import re
import json
import requests
from google.cloud import vision

def find_oryor_no_from_img(path):
    client = vision.ImageAnnotatorClient()

    # extract text from image
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    # find oryor no from text
    for text in texts:
        match = re.search(r'\d+-\d-\d+-\d-\d+', text.description)
        if match is not None:
            found = match.group()
            match = re.search(r'\d{2}-\d-\d{5}-\d-\d{4}', found)
            if match is not None:
                return { # perfect oryor no
                    'found': True,
                    'oy_no': match.group()
                }
            else:
                return { # look like oryor no
                    'found': False,
                    'oy_no': found
                }
    return { # not found oryor no
        'found': False,
        'oy_no': None
    }

def query_oryor_no_info(oryor_no):
    url = 'https://oryor.com/oryor2015/ajax-check-product.php'
    r = requests.post(url, data= { 'number_src': oryor_no })
    obj = json.loads(r.text[3:]) # skip 3-bytes UTF-8 BOM
    return obj['output'][0]

def query_oryor_info_from_img(path):
    result = find_oryor_no_from_img(path)
    if result['found']:
        oy_no = result['oy_no']
        return {
            'success': True,
            'oy_no': oy_no,
            'data': query_oryor_no_info(oy_no),
        }
    elif result['oy_no'] is not None:
        return {
            'success': False,
            'oy_no': result['oy_no'],
            'data': None,
        }
    else: # not found
        return {
            'success': False,
            'oy_no': None,
            'data': None,
        }

if __name__ == "__main__":

    import sys
    from pprint import pprint as pp

    path = sys.argv[1]
    result = query_oryor_info_from_img(path)
    pp(result)
