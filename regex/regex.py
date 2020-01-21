import re
import json
import pprint

def main():
    data = None
    response = None
    globalDict = dict()
    prettyPrinter = pprint.PrettyPrinter(indent=4)

    with open("data.txt", "r") as dataFile:
        data = dataFile.read()

    with open("response.json", "r") as responseFile:
        response = json.loads(responseFile.read())

    if data is None or response is None:
        print("Could not read from data or response")
        exit(1)

    for chunk in response["chunks"]:
        pattern = re.compile(chunk)
        match = pattern.search(data)

        if match is not None:
            globalDict.update(match.groupdict())

    prettyPrinter.pprint(globalDict)

if __name__ == "__main__":
    main()