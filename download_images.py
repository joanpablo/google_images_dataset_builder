# Downlod images from URL loaded from a json file
# python .\download_images.py --input ./json/bottle.json --output ./images/bottles

# import required packages
from io import BytesIO
from PIL import Image
from tqdm import tqdm
import argparse
import requests
import json
import os


# create argument parser and parse arguments
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--input', required=True,
                help='the path to the json input file')
ap.add_argument('-o', '--output', required=True,
                help='the path to the output directory')
args = vars(ap.parse_args())

# declaring proxies for requests
proxies = {
    'http': 'http://localhost:3128',
    'https': 'http://localhost:3128',
}

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

progress_bar = tqdm(total=len(json_data))
# loop over images data and download them to file system
print('[INFO] iterating over images in json file')
for image in json_data:
    # check if image is URL type
    if image['type'] == 'url':
        url = image['src']
        filename = os.path.sep.join(
            [args['output'], '{}.jpg'.format(count)])
        try:
            response = requests.get(url, proxies=proxies)
            image = Image.open(BytesIO(response.content))
            if image.mode != 'RGB':
                image = image.convert('RGB')
            image.save(filename)
        except Exception as e:
            if os.path.exists(filename):
                os.remove(filename)
            print('[ERROR] failed to download image {} . Message: {}'.format(
                url, str(e)))
            print('')

            if count > 0:
                count -= 1

    count += 1
    progress_bar.update(1)

progress_bar.close()
