import argparse
import json
import PIL
import pytesseract
import re
import requests

def parse_certificate_with_ipfs_template(document_path: str, cid: str):
    document = dict()
    
    document_text = pytesseract.image_to_string(PIL.Image.open(document_path))
    ipfs_json_response = requests.get(f'https://ipfs.io/ipfs/{cid}').json()

    for chunk in ipfs_json_response["chunks"]:
        regex_pattern = re.compile(chunk)
        match = regex_pattern.search(document_text)

        if match is not None:
            document.update(match.groupdict())

    return document

if __name__ == '__main__':
    argument_parser = argparse.ArgumentParser(description='Parse a text document image using a template.')
    argument_parser.add_argument('document_path', type=str, help='a path to the certificate image.')
    argument_parser.add_argument('cid', type=str, help='an IPFS Content Identifiers (CID).')

    args = argument_parser.parse_args()
    document = parse_certificate_with_ipfs_template(args.document_path, args.cid)
    print(json.dumps(document, indent=4, sort_keys=True))
