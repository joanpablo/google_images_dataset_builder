# This scripts parse HTML files extracted from the search results of Google Images
# and create a JSON file with all the url to the images for downloading.
# Usage: python .\convert_html_to_json.py --input ./htmls/bottles.html --output ./json/bottle.json

# import required packages
import json
import argparse
from utils import CustomHtmlParser

# create argument parser and parse arguments
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--input', required=True, help='the input XML file to parse')
ap.add_argument('-o', '--output', required=True, help='the path to the output JSON file for storing URL of images')
args = vars(ap.parse_args())

# parse HTML input file
print('[INFO] parsing HTML file: {}'.format(args['input']))
parser = CustomHtmlParser()
html_file = open(args['input'], encoding='utf8')
parser.feed(html_file.read())
html_file.close()

# save created json to filesystem
print('[INFO] saving json generated file')
json = json.dumps(parser.json)
output = open(args['output'], 'w', encoding='utf8')
output.write(json)
output.close()
