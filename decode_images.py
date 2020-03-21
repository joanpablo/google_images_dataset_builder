# Decode base64 images loaded from a json file
# python .\decode_images.py --input ./json/bottle.json --output ./images/bottles

# import required packages
import argparse
import base64
import json
import os

# create argument parser and parse arguments
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--input', required=True,
                help='the path to the json input file')
ap.add_argument('-o', '--output', required=True,
                help='the path to the output directory')
args = vars(ap.parse_args())

# check if output directory exist, otherwise create it
print('[INFO] checking output directory')
if not os.path.exists(args['output']):
    os.makedirs(args['output'])

# open json file and load data
print('[INFO] opening json file')
input_file = open(args['input'], encoding='utf8')
json_data = json.load(input_file)
input_file.close()

# initialize the images counter
count = 1
# if output directory not empty, initialize counter
# with max number in files name
files = os.listdir(args['output'])
if len(files) > 0:
    numbers = map(lambda path: int(
        os.path.basename(path).split('.')[0]), files)
    count = max(numbers) + 1

# loop over images data, decode base64 images
# and save them to output directory
print('[INFO] iterating over images in json file')
for image in json_data:
    # check if image is base 64 string
    if image['type'] == 'base64':
        # extract base 64 string data from image
        str_data = data = image['src'].split(',')[1]
        # decode image a save it to disc
        image_data = base64.b64decode(str_data, validate=True)
        filename = os.path.sep.join(
            [args['output'], '{}.jpg'.format(count)])
        image_file = open(filename, 'wb')
        image_file.write(image_data)
        image_file.close()
    count += 1

print('[INFO] images read successfully')
