import re
import pytesseract

from PIL import Image
from prettytable import PrettyTable
from difflib import SequenceMatcher

from DBHandler import DBHandler
from BlockchainHandler import BlockchainHandler
import StringConstants

db = DBHandler()
blockchain = BlockchainHandler()

def get_similarity_ratio(a, b):
    return SequenceMatcher(None, a, b).ratio()

def main():
    print(StringConstants.DOUBLE_LINE)
    print("VERIFIERA DOCUMENT VERIFIER")
    print(StringConstants.DOUBLE_LINE)

    print("ISSUERS")
    print(StringConstants.SINGLE_LINE)
    issuers = db.get_issuers()
    for issuer in issuers:
        print("%d - %s" %(issuer["id"], issuer["name"]))
    print(StringConstants.SINGLE_LINE)
    issuer_id = input("Select Issuer: ")
    print(StringConstants.DOUBLE_LINE)

    print("DOCUMENT TYPES")
    print(StringConstants.SINGLE_LINE)
    document_types = db.get_document_types(1)
    for document_type in document_types:
        print("%d - %s" %(document_type["id"], document_type["name"]))
    print(StringConstants.SINGLE_LINE)
    document_type_id = input("Select Type: ")
    print(StringConstants.DOUBLE_LINE)

    template_chunks = db.get_document_template(issuer_id, document_type_id)
    certificate_path = "Certificate.jpg"

    certificate_image = Image.open(certificate_path)
    certificate_text = pytesseract.image_to_string(certificate_image)

    globalDict = dict()
    for chunk in template_chunks:
        pattern = re.compile(chunk)
        match = pattern.search(certificate_text)

        if match is not None:
            globalDict.update(match.groupdict())

    actual_certificate = blockchain.get_certificate()
    tbl = PrettyTable(["ID", "Scanned", "Actual", "Similarity (percentage)"])
    for key in globalDict.keys():
        scanned_value = globalDict[key]
        try:
            actual_value = actual_certificate[key]
            similarity_percentage = get_similarity_ratio(scanned_value, actual_value) * 100
            similarity = ("%.2f %%" % (similarity_percentage))
        except KeyError:
            actual_value = similarity = "NOT VERIFIED"
        tbl.add_row([key, scanned_value, actual_value, similarity])
    print(tbl)


if __name__ == "__main__":
    main()