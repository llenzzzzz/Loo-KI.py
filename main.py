import argparse
import sys
import re
import file_hash
import url
import export_csv

REG_HASH = r'[a-fA-F0-9]'
REG_URL = r'^(https?://)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(/.*)?$'
REG_IP = r''

def parseArguments():
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        '-f',
        '--file',
        help="Input Filename",
        type=str
    )
    
    parser.add_argument(
        '-i',
        '--input',
        help="String Input",
        type=str
    )
    
    return parser.parse_args()

def process_hash(item):
    vt_data = file_hash.virustotal(item)
    ha_data = file_hash.hybridanalysis(item)
    if vt_data or ha_data:
        export_csv.save_hash(vt_data, ha_data, f"Hash_Lookups.csv")

def process_url(item):
    url_data = url.who_is(item)
    if whois_data:
        export_csv.save_url(url_data, f"URL_Lookups.csv")

def main():
    args = parseArguments()

    if args.file and args.input:
        sys.exit("Error: You can either provide a file or a string input, not both.")
    if not args.file and not args.input:
        sys.exit("Error: No input provided. Please provide a file or string input.")

    regex_hash = re.compile(REG_HASH)
    regex_url = re.compile(REG_URL)

    if args.file:
        with open(args.file, "r") as file:
            itemList = file.readlines()

        for item in itemList:
            item = item.strip()
            if regex_hash.match(item):
                process_hash(item)
            elif regex_url.match(item):
                process_url(item)

    elif args.input:
        input_data = args.input.strip()
        
        if regex_hash.match(input_data):
            process_hash(input_data)
        elif regex_url.match(input_data):
            process_url(input_data)

if __name__ == "__main__":
    main()
